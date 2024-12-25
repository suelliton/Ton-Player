import flet as ft
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import subprocess
import os
from models import Playlist, Music
import metadata.mutagen_mp3 as mutagen_mp3
from utils import sanitize_metadata, get_audio_duration
import time
from views.commons import show_notification, NotificationType
# Configuração do Spotify API
spotify = Spotify(auth_manager=SpotifyClientCredentials(
    client_id="2ec55646db0248a6b36927d60e0be092",
    client_secret="a62692951af14557832caebd28df63c5"
))

class DownloadView():
    _instance = None
    content_ui = None
    field_search_ui = None
    list_search_ui = None
    list_musics_album_ui = None
    container_collapse = None

    def __new__(cls,app, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DownloadView, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, app):
        if not hasattr(self, "_initialized"):
            print("Creating DownloadView")
            self.app = app      
            self.build()
    
    def list_files_in_directory(self, album_dir):
        try:
            files = os.listdir(album_dir)
            return files
        except Exception as e:
            print(f"Erro ao listar arquivos: {e}")
            return []
    
    def create_playlist(self, artist_name, album_name, coverart_album_url, album_dir):
        new_playlist, _ = Playlist.get_or_create(name=f'{artist_name} {album_name}', coverart=coverart_album_url)
        print(f'Adicionando musicas a playlist: {new_playlist.name}')
        time.sleep(2)
        print('Listando arquivos do album em ', album_dir)
        files = self.list_files_in_directory(album_dir)
        for filename in files:
            _complete_path =  os.path.join(album_dir, filename)
            print('mp3 path', filename)
            duration = str(get_audio_duration(_complete_path))
            metadata = mutagen_mp3.extract_mp3_metadata(_complete_path)
            metadata = sanitize_metadata(metadata)
            print('Metadata', metadata)
            #BABYMONSTER - Stuck In The Middle.mp3
            Music.create(
                title=filename.replace('.mp3',''), 
                path=_complete_path, 
                duration=duration, 
                artist = metadata['artist'],
                album = metadata['album'],
                genre = metadata['genre'],
                coverart = metadata['coverart_path'],
                playlist=new_playlist)
        try:
            self.app.left_view.update_playlists_ui()
        except Exception as e:
            print(f'Erro na atualização da lista de playlists: {e}')
        try:
            self.app.listen_view.update_list_musics_ui()
        except Exception as e:
            print(f'Erro na atualização da lista de musicas: {e}')

    def download_album(self, artist_name, album_name, coverart_album_url, download_url):
        show_notification(self.app, f"Starting download of album: {album_name}...")
        try:
            # Caminho para a pasta "Downloads" dentro do diretório atual
            downloads_dir = os.path.join(os.getcwd(), "downloads")
            
            # Verifica se a pasta "Downloads" existe, se não, cria
            if not os.path.exists(downloads_dir):
                os.makedirs(downloads_dir)
                print(f"Pasta 'downloads' criada em: {downloads_dir}")
            
            # Cria a pasta do álbum dentro de "Downloads"
            album_dir = os.path.join(downloads_dir, artist_name ,album_name)
            if not os.path.exists(album_dir):
                os.makedirs(album_dir)
                print(f"Pasta do álbum '{album_name}' criada em: {album_dir}")
            
            # Executa o comando "spotdl url_download" dentro da pasta do álbum
            command = ["spotdl", download_url]
            print(f"Executando comando: {' '.join(command)} na pasta {album_dir}")
            
            subprocess.run(command, cwd=album_dir, check=True)
            self.create_playlist(artist_name, album_name, coverart_album_url, album_dir)
            print(f"Download do álbum '{album_name}' concluído com sucesso!")
            show_notification(self.app, f"{album_name} downloaded successfully!", type=NotificationType.SUCCESS)
        
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar o comando: {e}")
        except Exception as e:
            print(f"Erro geral: {e}")

    def download(self, e, result):
        #print(result.keys())#['album_type', 'total_tracks', 'available_markets', 'external_urls', 'href', 'id', 'images', 'name', 'release_date', 'release_date_precision', 'type', 'uri', 'artists']
        print(result['artists'][0]['name'])
        print(result['external_urls']['spotify'])
        print('Images',result['images'][-2]['url'])        
        #out = subprocess.run(['spotdl', result['external_urls']['spotify']], capture_output=True, text=True)
        # print('Saída',out.stdout) 
        artist_name = result['artists'][0]['name']
        album_name = result['name'] 
        download_url = result['external_urls']['spotify'] 
        coverart_album_url = result['images'][-2]['url']#pega uma definição media de imagem
        self.app.page.run_thread(self.download_album,artist_name, album_name,coverart_album_url, download_url, )

    def search_spotify(self, query, tipo="album"):
        result = spotify.search(q=query, type=tipo, limit=5)
        return result[tipo + 's']['items']

    # def get_tracks(self, album_id):
    #     tracks = spotify.album_tracks(album_id)
    #     print('Tracks', tracks)
    #     return tracks
    def toggle_visibility_list_musics_album(self, e, album):
        collapses_containers = []
        for column in self.list_search_ui.controls:
            collapses_containers.append(column.controls[1].controls[0])

        icon_key = e.control.key
        container_key = icon_key.replace('icon','container')
        print('container key', container_key)
        container = [c for c in collapses_containers if c.key == container_key][0]

        if e.control.icon == ft.icons.KEYBOARD_ARROW_DOWN:
            # print('Keys',album.keys())
            # print(album)
            print('GET LIST MUSICS FROM SPOTIFY')
            musics = spotify.album_tracks(album['id'])['items']
            list_musics_album_ui = ft.ListView()
            list_musics_album_ui.controls.clear()
            list_musics_album_ui.controls = [
                ft.Container(
                    padding= ft.padding.all(10),                    
                    content=ft.Row(
                        controls=[
                            ft.Text(value=f'{i+1} - ',color=ft.colors.WHITE),
                            ft.Text(value=music['name'], color=ft.colors.WHITE)
                        ]
                    )
                ) for i, music in enumerate(musics)
            ]
            container.content = list_musics_album_ui
            container.visible = True
            container.update()
            list_musics_album_ui.update()
            container.update()
        else:
            container.visible = False
            container.update()

        # self.list_search_ui.update()
        # nonlocal is_visible  # Permite alterar a variável no escopo externo
        # is_visible = not is_visible
        # collapsible_container.visible = is_visible
        # collapsible_container.update()

        # Atualiza o ícone do botão
        e.control.icon = (
            ft.icons.KEYBOARD_ARROW_DOWN if e.control.icon == ft.icons.KEYBOARD_ARROW_UP else ft.icons.KEYBOARD_ARROW_UP
        )
        e.control.update()

    def search(self, e):
        search_text = self.field_search_ui.value
        print(search_text)
        self.list_search_ui.controls.clear()
        if search_text == '':
            self.list_search_ui.update()
            return
        type = 'album'
        results = self.search_spotify(search_text, type)        

        self.list_musics_album_ui = ft.ListView()
        self.container_collapse = ft.Container(visible=False, content=self.list_musics_album_ui)

        self.list_search_ui.controls = [
        ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,   
                    spacing=20,
                    controls=[
                        ft.Column(                  
                            controls=[
                                ft.Container(
                                    content=ft.Image(src=result['images'][-1]['url'] if result['images'][-1]['url'] else "default-playlist.jpg", fit=ft.ImageFit.COVER, height=80)
                                ),                        
                            ]
                        ),
                        ft.Column(                       
                            alignment=ft.CrossAxisAlignment.END,       
                            # width = 220 if self.app.is_sm else 500,                            
                            expand=True,
                            controls=[                        
                                ft.Container(
                                    padding=ft.padding.only(left = 5),
                                    margin=ft.margin.only(top=0, bottom=0),
                                    content=ft.Text(value=result['name'], overflow=ft.TextOverflow.ELLIPSIS,weight='bold',color=ft.colors.WHITE)
                                ), 
                                ft.Container(
                                    padding=ft.padding.only(left = 5, top=0, bottom=0),
                                    margin=ft.margin.only(top=0, bottom=0),
                                    content=ft.Text(value=f'{result['total_tracks']} musics', color=ft.colors.WHITE, size=10)
                                ),
                                ft.Container(
                                    padding=ft.padding.only(left = 5),
                                    margin=ft.margin.only(top=0, bottom=0),                                    
                                    content=ft.Text(value=result['artists'][0]['name'],color=ft.colors.WHITE)
                                ),       
                                # ft.Container(key=f'container_{result['id']}',visible=True)     
                            ]
                        ),
                        ft.Column(                 
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,                  
                            controls=[  
                                ft.IconButton(
                                    alignment=ft.alignment.center_right,
                                    icon=ft.icons.DOWNLOAD,
                                    icon_color=ft.colors.WHITE,
                                    on_click=lambda e, r=result: self.download(e, r)
                                ),                               
                                ft.Container(                       
                                    content=ft.IconButton(
                                                key=f'icon_{result['id']}',
                                                icon=ft.icons.KEYBOARD_ARROW_DOWN,
                                                icon_color= ft.colors.WHITE,
                                                on_click= lambda e, a=result : self.toggle_visibility_list_musics_album(e, a),
                                            )
                                )
                            ]
                        )
                    ]  
                ),
                ft.Row(
                    controls=[ft.Container(key=f'container_{result['id']}',visible=False)]
                )
                ]
            )for result in results
        ]
         
        self.list_search_ui.update()

    def build(self):
        self.field_search_ui = \
        ft.TextField(
            autofocus=True,
            border_radius=25,
            color=ft.colors.WHITE,
            border_color=ft.colors.WHITE,
            cursor_color=ft.colors.WHITE,
            value='',
            on_submit= lambda e: self.search(e),
            # on_change=lambda e: self.search(e)
        )
        self.list_search_ui = \
        ft.Column(
            controls=[

            ]
        )

        self.content = \
        ft.Container(            
            shadow=ft.BoxShadow(blur_radius=15,color=ft.colors.with_opacity(color=ft.colors.BLUE_400, opacity=0.3)),
            content=ft.Column(
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                border_radius=25,
                                padding=ft.padding.symmetric(vertical=20),
                                shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.BLACK12),
                                content=self.field_search_ui
                            ),                          
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Column(
                                scroll=ft.ScrollMode.ALWAYS,
                                height=500,
                                expand=True,                 
                                controls=[
                                    ft.Container(
                                        padding=ft.padding.all(20),
                                        content=self.list_search_ui
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        )