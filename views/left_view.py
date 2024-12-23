import flet as ft
from models import Playlist, Music
import asyncio
from threading import Thread
import time
from commons import show_notification

class LeftView():
    _instance = None
    app = None
    content_ui = None
    new_playlist_modal = None
    playlists_ui = None
    add_playlist_btn = None
    
    playlists = []
    selected_playlist = None

    def __new__(cls,app, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LeftView, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, app):
        # Certifique-se de que a inicialização ocorra apenas uma vez
        if not hasattr(self, "_initialized"):
            print("Creating LeftView")
            self._initialized = True
            self.app = app
            self.initialize()
            self.build()
    
    def initialize(self):
        self.playlists = self.get_playlists()
        self.selected_playlist = self.playlists[0] 

    def get_playlists(self):
        return Playlist.select().order_by(-Playlist.created)
    
    def open_new_playlist_dialog(self,e):        
        self.app.page.open(self.new_playlist_modal)
    
    def save_new_playlist(self, e):
        """Inicia o processo de salvar a nova playlist."""
        self.save_new_playlist_background()

    def show_notification_adding_playlist(self, name):
        message = f'Adding playlist... {name}'
        show_notification(self.app, message)
        
    
    def show_notification_remove_playlist(self, playlist):
        message = f'Removing playlist... {playlist.name}'
        show_notification(self.app, message)
      

    def save_new_playlist_background(self):
        """Executa o salvamento da playlist em segundo plano."""
        name = self.new_playlist_modal.content.value
        print('Name playlist:', name)

        if name.strip() == '':
            self.new_playlist_modal.content.error_text = "The name playlist is required."
            self.new_playlist_modal.content.update()
            return

        self.show_notification_adding_playlist(name)

        # Fechar o modal e limpar o campo
        self.app.page.close(self.new_playlist_modal)
        self.new_playlist_modal.content.value = ''
        self.new_playlist_modal.content.error_text = None
        self.new_playlist_modal.update()
        # self.app.page.close(self.app.drawer_ui)

        # Executa a criação da playlist em um thread separado
        def background_task():
            time.sleep(.1)
            Playlist.create(name=name.strip())
            # Atualiza a interface após o término
            self.update_playlists_ui()
            # self.app.page.add(ft.Text(f"Playlist '{name.strip()}' criada com sucesso!"))
            # self.app.page.update()

        self.app.page.run_thread(background_task)

    
    def remove_playlist(self, playlist):
        self.show_notification_remove_playlist(playlist)
        def background_task():
            try:
                time.sleep(0.1)
                Music.delete().where(Music.playlist == playlist).execute()
                playlist.delete_instance()
                print(f'Playlist {playlist.name} deleted')
            except:
                print('Error while deleting playlist')
            self.update_playlists_ui()

        self.app.page.run_thread(background_task)
    
    def select_playlist(self,e, playlist):
        self.selected_playlist = playlist
        self.app.listen_view.update_playlist_title(playlist)    
        self.update_playlists_ui()    
        self.app.listen_view.update_list_musics_ui() 
        
        if self.app.drawer_ui.open:
            self.app.page.close(self.app.drawer_ui)
    
    def update_playlists_ui(self):
        def highlight_item(e, p):       
            e.control.bgcolor = ft.colors.BLACK45 if e.data == "true" else ft.colors.BLACK45 if p == self.selected_playlist else ft.colors.BLACK12
            e.control.update()  # Atualiza o elemento

        self.playlists = Playlist.select().order_by(-Playlist.created)
        self.playlists_ui.controls.clear()

        # self.playlists_ui.controls = \
        # [
        # ft.Container(          
        #     bgcolor= ft.colors.BLACK45 if playlist == self.selected_playlist else ft.colors.BLACK12,
        #     border=ft.Border(
        #         bottom=ft.BorderSide(width=3,color=ft.colors.BLUE_400 if playlist == self.selected_playlist else ft.colors.BLACK12)  # Define a espessura e a cor da borda
        #     ),
        #     ink_color=ft.colors.WHITE,                             
        #     on_click=lambda e, p=playlist: self.select_playlist(e, p),  
        #     # on_hover=lambda e, p=playlist: highlight_item(e, p),
        #     content= 
        #         ft.Container(       
                          
        #             content=\
        #             ft.Row(
        #                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN,                
        #                 controls=[    
        #                     ft.Image(src=playlist.coverart, fit=ft.ImageFit.COVER,width=50),                                        
        #                     ft.Container(
        #                         # width=100,
        #                         expand=True,
        #                         content=ft.Text(
        #                             playlist.name,                            
        #                             text_align=ft.TextAlign.START,
        #                             overflow=ft.TextOverflow.ELLIPSIS,  # Adiciona o ellipsis
        #                             max_lines=1,                       # Garante que o texto ocupe uma única linha
        #                             color=ft.colors.WHITE if playlist == self.selected_playlist else ft.colors.WHITE
        #                         ),
        #                         # on_click=lambda e, p=playlist: self.select_playlist(e, p),
        #                     ),
        #                     ft.PopupMenuButton(
        #                         icon=ft.icons.MORE_VERT,  
        #                         icon_size=20,                                              
        #                         items=[
        #                             ft.PopupMenuItem(text="Edit"),
        #                             ft.PopupMenuItem(text="Remove", on_click=lambda e, p=playlist: self.remove_playlist(p)),
                                
        #                         ]
        #                     )
        #                 ]
        #             )
        #         )
        # ) for playlist in self.playlists                                
        # ]
        self.playlists_ui.controls = [                       
                ft.Container(
                    padding= ft.padding.all(10),
                    bgcolor=ft.colors.BLACK45 if playlist == self.selected_playlist else ft.colors.BLACK12,
                    border=ft.Border(
                        bottom=ft.BorderSide(
                            width=3,
                            color=ft.colors.BLUE_400 if playlist == self.selected_playlist else ft.colors.BLACK12
                        )
                    ),
                    ink_color=ft.colors.WHITE,
                    on_click=lambda e, p=playlist: self.select_playlist(e, p),
                    on_hover=lambda e, p=playlist: highlight_item(e, p),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Container(
                                padding= ft.padding.only(right=10),
                                content=ft.Image(
                                    src=playlist.coverart,
                                    fit=ft.ImageFit.COVER,
                                    width=50,                                    
                                )
                            ),
                            ft.Container(
                                expand=True,
                                content=ft.Text(
                                    playlist.name,
                                    text_align=ft.TextAlign.START,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                    max_lines=1,
                                    color=ft.colors.WHITE if playlist == self.selected_playlist else ft.colors.WHITE
                                )
                            ),
                            ft.PopupMenuButton(
                                icon=ft.icons.MORE_VERT,
                                icon_color=ft.colors.WHITE,
                                icon_size=20,
                                items=[
                                    ft.PopupMenuItem(text="Edit"),
                                    ft.PopupMenuItem(
                                        text="Remove",
                                        on_click=lambda e, p=playlist: self.remove_playlist(p)
                                    ),
                                ]
                            )
                        ]
                    )
                ) for playlist in self.playlists
            ]
        

    
        self.playlists_ui.update()
    
        
    def build(self):        
        self.new_playlist_modal = \
        ft.AlertDialog(
                        modal=True,
                        title=ft.Text(value='Playlist Name'),
                        content=ft.TextField(autofocus=True,label='Name'),
                        actions=[
                            ft.ElevatedButton(text='Cancel',color=ft.colors.WHITE, bgcolor=ft.colors.RED_300,on_click=lambda e: self.app.page.close(self.new_playlist_modal)),
                            ft.ElevatedButton(text='Save',color=ft.colors.WHITE, bgcolor=ft.colors.BLUE_300,on_click=lambda e: self.save_new_playlist(e)),
                        ]
                    )
        
        self.playlists_ui = ft.ListView(
                                expand=True,  # Para ajustar ao tamanho disponível
                                spacing=10,   # Espaçamento entre os itens
                                # padding=ft.padding.all(10),
                                controls=[]
                            )
        self.add_playlist_btn = \
        ft.ElevatedButton(
                        text='Playlist',
                        # width=150,
                        bgcolor=ft.colors.GREEN_500,
                        color=ft.colors.WHITE,
                        icon=ft.icons.ADD_OUTLINED,
                        on_click=lambda e: self.open_new_playlist_dialog(e)
        )

        self.content_ui = \
        ft.Column(
    horizontal_alignment="center",
    alignment=ft.MainAxisAlignment.CENTER,
    controls=[
        ft.Container(
            padding=ft.padding.only(top=20, left=20, right=20),
            height=580,
            content=ft.Column(
                controls=[
                    ft.Text(
                        value="Playlists",
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE,
                        text_align=ft.TextAlign.CENTER
                    ),
                    self.playlists_ui,
                    ft.Row(                        
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[self.add_playlist_btn]
                    ),
                    ft.Divider(),
                ]
            )
        )
    ],
)

