import flet as ft
from models import Music
from player_view import PlayerView
from left_view import LeftView
from download_view import DownloadView
from search_view import SearchView
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.id3 import ID3, APIC
import time
import metadata.shazam as shazam
import metadata.mutagen_mp3 as mutagen_mp3
from utils import sanitize_metadata, get_audio_duration
from commons import show_notification

class ListenView():
    _instance = None
    app = None
    content_ui = None
    playlist_title_ui = None
    header_list_musics_ui = None
    list_musics_ui = None
    list_musics = []
    add_music_btn = None
    file_picker = None
    search_view = None
    left_view = None


    def __new__(cls,app, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ListenView, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, app):
        if not hasattr(self, "_initialized"):
            print("Creating MainView")
            self.app = app          
            self.build()   
    
    def update_playlist_title(self, playlist):
        self.playlist_title_ui.value = playlist.name
        self.playlist_title_ui.update()

    def load_music(self,file_picker):
        file_picker.pick_files(allow_multiple=True)   
    
    def show_notification_remove_music(self, music):
        message = f'Removing music... {music.title}'
        show_notification(self.app, message)    

    def show_notification_adding_music(self):
        message = 'Adding musics...'
        show_notification(self.app, message)      

    def add_playlist_coverart(self, playlist, files):
        if len(files) >=1:
            metadata = mutagen_mp3.extract_mp3_metadata(files[0].path)
            metadata = sanitize_metadata(metadata)
            if 'default-music' in metadata['coverart_path'] : 
                playlist.coverart = 'default-playlist.png'
            else:
                playlist.coverart = metadata['coverart_path']
            playlist.save()
 
    def add_music_to_playlist(self,files, selected_playlist):
        self.show_notification_adding_music()
        async def background_task():
            print('Selected', selected_playlist.name)
            time.sleep(0.1)
            self.add_playlist_coverart(selected_playlist, files)
            if files:
                for file in files:
                    duration = str(get_audio_duration(file.path))
                    metadata = mutagen_mp3.extract_mp3_metadata(file.path)
                    metadata = sanitize_metadata(metadata)
                    print('Metadata', metadata)
                    
                    Music.create(
                        title=file.name.replace('.mp3',''), 
                        path=file.path, 
                        duration=duration, 
                        artist = metadata['artist'],
                        album = metadata['album'],
                        genre = metadata['genre'],
                        coverart = metadata['coverart_path'],
                        playlist=selected_playlist)
                self.update_list_musics_ui()
        self.app.page.run_task(background_task)

    def remove_music(self, music):
        self.show_notification_remove_music(music)
        def background_task():
            try:
                music.delete_instance()
                print(f"Músic '{music.title}' removed sucessfully.")
            except Exception as e:
                print(f"Error while remove music: {e}")        
            self.update_list_musics_ui()
        self.app.page.run_thread(background_task)    

    def update_metadata_playlist(self, e):   
        show_notification(self.app, "Updating all musics metadata")
        shazam.update_metadata_playlist( self.app, self.app.left_view.selected_playlist)
    
    def save_metadata_playlist_for_mp3_files(self, e):
        show_notification(self.app, "Saving all metadatas for mp3 files")
        # mutagen_mp3.task_update_mp3_files_playlist(self.app.left_view.selected_playlist)
        mutagen_mp3.update_mp3_files_playlist(self.app.left_view.selected_playlist)

    def update_list_musics_ui(self):   
        print('Update_list_musics_ui')
        self.list_musics = Music.select().where(Music.playlist==self.app.left_view.selected_playlist)
             
        self.list_musics_ui.controls.clear()
        # self.list_musics_ui.rows.clear()
        # self.list_musics_ui.rows = [
        #                 ft.DataRow(
        #                     color=ft.colors.GREY_100,                           
        #                     cells=[
        #                     ft.DataCell(                                
        #                         ft.Container(                                                                     
        #                             content=ft.PopupMenuButton(
        #                                         icon=ft.icons.MORE_VERT,  
        #                                         tooltip='Actions',
        #                                         icon_size=20,       
        #                                         items=[
        #                                             ft.PopupMenuItem(text="Get metadata", on_click=lambda e, m=music: shazam.update_metadata(m, self.app)),
        #                                             ft.PopupMenuItem(text="Remove", on_click=lambda e, m=music: self.remove_music(m)),
        #                                         ]
        #                                     )
        #                         )
                                 
        #                     ),
        #                     ft.DataCell(                                                                    
        #                         ft.Container(                                  
        #                             width=50,                                    
        #                             shadow=ft.BoxShadow(
        #                             blur_radius=40, 
        #                             color=ft.colors.BLUE_500 if music == self.player_view.selected_music else ft.colors.WHITE24),
        #                             content=ft.Image(src=music.coverart, fit=ft.ImageFit.COVER),
        #                         ),
        #                         on_double_tap=lambda  e, m=music: self.player_view.play_music(m)
        #                     ),
        #                     ft.DataCell(                                                                    
        #                         ft.Container(                                  
        #                             width=250,                                    
        #                             shadow=ft.BoxShadow(
        #                             blur_radius=40, 
        #                             color=ft.colors.BLUE_500 if music == self.player_view.selected_music else ft.colors.WHITE24),
        #                             content=ft.Text(
        #                                 value=music.title, 
        #                                 overflow=ft.TextOverflow.ELLIPSIS,
        #                                 max_lines=1,  # Garante que seja apenas uma linha com elipses
        #                                 color=ft.colors.BLUE_600 if music == self.player_view.selected_music else ft.colors.BLACK,
        #                                 style=ft.TextStyle(weight='bold')
        #                             ),
        #                         ),
        #                         on_double_tap=lambda  e, m=music: self.player_view.play_music(m)
        #                     ),
        #                     ft.DataCell(                                                                    
        #                         ft.Container(                                  
        #                             width=100,                                    
        #                             shadow=ft.BoxShadow(
        #                             blur_radius=40, 
        #                             color=ft.colors.BLUE_500 if music == self.player_view.selected_music else ft.colors.WHITE24),
        #                             content=ft.Text(
        #                                 value=music.album, 
        #                                 tooltip=music.album,
        #                                 overflow=ft.TextOverflow.ELLIPSIS,
        #                                 max_lines=1,  # Garante que seja apenas uma linha com elipses
        #                                 color=ft.colors.BLUE_600 if music == self.player_view.selected_music else ft.colors.BLACK,
        #                                 style=ft.TextStyle(weight='bold')
        #                             ),
        #                         ),
        #                         on_double_tap=lambda  e, m=music: self.player_view.play_music(m)
        #                     ),
        #                     ft.DataCell(
        #                         ft.Container(
        #                             width=150,
        #                             shadow=ft.BoxShadow(
        #                             blur_radius=40, 
        #                             color=ft.colors.BLUE_500 if music == self.player_view.selected_music else ft.colors.WHITE10),
        #                             content=ft.Text(
        #                                         value=music.artist,
        #                                         color=ft.colors.BLUE_600 if music == self.player_view.selected_music else ft.colors.BLACK,
        #                                         style=ft.TextStyle(weight='bold')
        #                                         )),
        #                             on_double_tap=lambda e, m=music: self.player_view.play_music(m)
        #                             ),
        #                     ft.DataCell(
        #                         ft.Container(
        #                             width=200,
        #                             shadow=ft.BoxShadow(
        #                             blur_radius=40, 
        #                             color=ft.colors.BLUE_500 if music == self.player_view.selected_music else ft.colors.WHITE10),
        #                             content=ft.Text(
        #                                         value=music.duration,
        #                                         color=ft.colors.BLUE_600 if music == self.player_view.selected_music else ft.colors.BLACK,
        #                                         style=ft.TextStyle(weight='bold')
        #                                 )),
        #                             on_double_tap=lambda e, m=music: self.player_view.play_music(m)
        #                             ),
        #                     # ft.DataCell(ft.Text(music.duration), on_double_tap=lambda e, m=music: self.play_music(m)),
        #                     ft.DataCell(ft.IconButton(icon=ft.icons.HIGHLIGHT_REMOVE, on_click= lambda e, m=music: self.remove_music(m)))
        #                 ]
        #                 ) for music in self.list_musics
        #             ]        
        
        self.list_musics_ui.controls = [
             ft.Container(
                    bgcolor=ft.colors.with_opacity(color=ft.colors.BLUE_500, opacity=0.3) if music == self.player_view.selected_music else ft.colors.BLACK12,
                    padding=ft.padding.all(10),
                    border=ft.Border(
                        bottom=ft.BorderSide(
                            width=3,
                            color= ft.colors.BLACK12
                        )
                    ),                   
                    # shadow=ft.BoxShadow(
                    #                 blur_radius=10, 
                    #                 color=ft.colors.with_opacity(color=ft.colors.BLUE_500, opacity=0.3) if music == self.player_view.selected_music else ft.colors.WHITE10
                    # ),
                    ink_color=ft.colors.WHITE,
                    on_click=lambda e, m=music: self.player_view.play_music(m),
                    # on_hover=lambda e, m=music: highlight_item(e, m),
                    key=f'music-item-{music.id}',
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[         
                            ft.Container(
                                padding=ft.padding.only(left=5, right=15),
                                content=ft.Text(value=f'{i+1}', color=ft.colors.WHITE, text_align='left')
                            ),                                              
                            ft.Container(
                                expand=True,                                
                                padding=ft.padding.symmetric(horizontal=5),                               
                                content=\
                                    ft.Row(
                                        controls=[                                                                       
                                            ft.Container(
                                                content=ft.Image(
                                                        src=music.coverart,
                                                        fit=ft.ImageFit.COVER,
                                                        width=50
                                                )
                                            ),  
                                            ft.Column(                                              
                                                controls=[                                                    
                                                    ft.Text(
                                                        value=music.title,                                                  
                                                        text_align=ft.TextAlign.START,
                                                        overflow=ft.TextOverflow.ELLIPSIS,
                                                        max_lines=1,
                                                        weight='bold',
                                                        color=ft.colors.WHITE,                                                        
                                                    ),                                               
                                                    ft.Text(
                                                        value=music.artist,                                                  
                                                        text_align=ft.TextAlign.START,
                                                        overflow=ft.TextOverflow.ELLIPSIS,
                                                        max_lines=1,
                                                        color= ft.colors.WHITE
                                                    )
                                            ]
                                    )]
                                )
                            ),  
                            ft.Container(  
                                expand=True,  
                                visible= not self.app.is_sm,
                                alignment=ft.alignment.center,
                                content=ft.Text(value=music.album, color=ft.colors.WHITE,text_align=ft.TextAlign.CENTER)
                            ),                                                                                
                            ft.Container(   
                                # expand=True,           
                                padding=ft.padding.symmetric(horizontal=30),  
                                visible= not self.app.is_sm,     
                                alignment=ft.alignment.center_right,           
                                content=ft.Text(value=music.duration.replace('.',':'), color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER)
                            ),   
                            ft.Container(     
                                # expand=True,  
                                alignment=ft.alignment.center_right,                                                              
                                content=ft.PopupMenuButton(
                                            icon=ft.icons.MORE_VERT,  
                                            icon_color=ft.colors.WHITE,
                                            tooltip='Actions',
                                            icon_size=20,       
                                            items=[
                                                ft.PopupMenuItem(text="Get metadata", on_click=lambda e, m=music: shazam.update_metadata(m, self.app)),
                                                ft.PopupMenuItem(text="Remove", on_click=lambda e, m=music: self.remove_music(m)),
                                            ]
                                        )
                            )                         
                        ]
                    )
                ) for i, music in enumerate(self.list_musics)
        ]
        # self.list_musics_ui.controls = [
        #     ft.Row(
        #         alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        #         controls=[
        #             ft.Container(
        #                 # expand=True, 
        #                 padding=ft.padding.only(left=15),
        #                 content=ft.Text(value='#', color=ft.colors.WHITE) 
        #             ),
        #             ft.Container(
        #                 expand=True, 
        #                 content=ft.Text(value='Title', color=ft.colors.WHITE, text_align='center')
        #             ),
        #             ft.Container(
        #                 expand=True, 
        #                 visible= not self.app.is_sm,
        #                 content=ft.Text(value='Album', color=ft.colors.WHITE,text_align='center')
        #             ),
        #             ft.Container(
        #                 expand=True, 
        #                 content=ft.Icon(name=ft.icons.ACCESS_TIME, color=ft.colors.WHITE)
        #             ),
        #         ]
        #     )
        # ] + self.list_musics_ui.controls
        
        # self.list_musics_ui.update()
        if self.player_view.selected_music:
            key_to_focus = f'music-item-{self.player_view.selected_music.id}' 
            self.list_musics_ui.scroll_to(key=key_to_focus,offset=0, duration=1000)          
        self.list_musics_ui.update()            


    def build(self):
        self.file_picker = ft.FilePicker(
                on_result=lambda e: self.add_music_to_playlist(e.files, self.app.left_view.selected_playlist)
         )
        self.app.page.overlay.append(self.file_picker)

        self.search_view = SearchView(self.app)
        self.left_view = LeftView(self)              

        self.playlist_title_ui = \
        ft.Text(
            value=self.app.left_view.selected_playlist.name,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.WHITE
        )
        self.update_metadata_btn = ft.IconButton(
                                        alignment=ft.alignment.center,
                                        icon=ft.icons.SAVE_ALT, 
                                        icon_color=ft.colors.WHITE,
                                        icon_size=25,
                                        tooltip='Update metadata all tracks',
                                        on_click= lambda e: self.update_metadata_playlist(e)
                                        )
        self.save_mp3_metadata_btn = ft.IconButton(
                                        alignment=ft.alignment.center,
                                        icon=ft.icons.SAVE, 
                                        icon_color=ft.colors.WHITE,
                                        icon_size=25,
                                        tooltip='Save metadata to mp3 files',
                                        on_click= lambda e: self.save_metadata_playlist_for_mp3_files(e)
                                        )
        

        # self.list_musics_ui = \
        # ft.DataTable(
        #     bgcolor=ft.colors.WHITE12,
        #     expand=True,
        #     columns=[
        #         ft.DataColumn(ft.Text('',text_align=ft.TextAlign.CENTER,style=ft.TextStyle(weight='bold',color=ft.colors.WHITE)),heading_row_alignment="start"),
        #         ft.DataColumn(ft.Text('Cover',text_align=ft.TextAlign.CENTER,style=ft.TextStyle(weight='bold',color=ft.colors.WHITE)),heading_row_alignment="start"),
        #         ft.DataColumn(ft.Text('Title',text_align=ft.TextAlign.CENTER,style=ft.TextStyle(weight='bold',color=ft.colors.WHITE)),heading_row_alignment="start"),
        #         ft.DataColumn(ft.Text('Album',text_align=ft.TextAlign.CENTER,style=ft.TextStyle(weight='bold',color=ft.colors.WHITE)),heading_row_alignment="start"),            
        #         ft.DataColumn(ft.Text('Artist',text_align=ft.TextAlign.CENTER,style=ft.TextStyle(weight='bold',color=ft.colors.WHITE)),heading_row_alignment="start"),            
        #         ft.DataColumn(ft.Text('Duration',text_align=ft.TextAlign.CENTER,style=ft.TextStyle(weight='bold',color=ft.colors.WHITE)),heading_row_alignment="start"),            
        #         ft.DataColumn(ft.Text('Remove?',text_align=ft.TextAlign.CENTER,style=ft.TextStyle(weight='bold',color=ft.colors.WHITE)),heading_row_alignment="start"),            
        #     ],
        #     rows=[]
        # )
        self.header_list_musics_ui = \
        ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Container(
                        # expand=True, 
                        padding=ft.padding.only(left=15),
                        content=ft.Text(value='#', color=ft.colors.WHITE) 
                    ),
                    ft.Container(
                        expand=True, 
                        content=ft.Text(value='Title', color=ft.colors.WHITE, text_align='center')
                    ),
                    ft.Container(
                        expand=True, 
                        visible= not self.app.is_sm,
                        alignment=ft.alignment.center,
                        content=ft.Text(value='Album', color=ft.colors.WHITE,text_align='center')
                    ),
                    ft.Container(
                        # expand=True, 
                        visible= not self.app.is_sm,
                        padding=ft.padding.symmetric(horizontal=30),  
                        alignment=ft.alignment.center_right,
                        content=ft.Icon(name=ft.icons.ACCESS_TIME, color=ft.colors.WHITE)
                    ),
                    ft.Container(
                        # expand=True, 
                        alignment=ft.alignment.center_right,
                        content=ft.Text(value='Actions', color=ft.colors.WHITE,text_align='center')
                    ),
                ]
            )
        self.list_musics_ui = ft.Column(scroll=ft.ScrollMode.ALWAYS)

        self.add_music_btn = ft.ElevatedButton(
                        text='musics',
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.GREEN_500,
                        icon_color=ft.colors.WHITE, 
                        icon=ft.icons.ADD_OUTLINED, 
                        on_click=lambda e: self.load_music(self.file_picker)
                        )
        
        self.player_view = PlayerView(self.app)
        
        self.content_ui = \
        ft.Stack([
            
            ft.Container(
                # col={'xs':12, 'sm':9}, 
                padding=ft.padding.all(20),
                expand=True,
                bgcolor = ft.colors.BLACK45,
                shadow=ft.BoxShadow(blur_radius=15,color=ft.colors.with_opacity(color=ft.colors.BLUE_400, opacity=0.3)),
                content=\
                ft.ResponsiveRow(
                    controls=[
                            ft.Column(
                                col={'xs':0,'sm':0, 'md':4},                               
                                controls=[
                                    self.left_view.content_ui
                                ]
                            ),
                            ft.Column(
                                    col={'sm':12, 'md':8},                                    
                                    controls= [
                                        ft.Row(
                                            alignment= ft.MainAxisAlignment.CENTER,
                                            height=20,
                                            controls=[
                                                # self.search_view.content_ui
                                            ]
                                        ),
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                            ft.Icon(name=ft.icons.PLAY_ARROW_SHARP, color=ft.colors.WHITE),
                                            self.playlist_title_ui,
                                            ft.Column(
                                                col=2,
                                                alignment=ft.alignment.center_right,
                                                controls=[
                                                    ft.Row(
                                                        controls=[
                                                            self.update_metadata_btn,
                                                            self.save_mp3_metadata_btn
                                                        ]
                                                    )
                                                ]
                                            ),                           
                                        ],spacing=0),
                                        #Deveria ter uma row pra scrolar pros lados 
                                        ft.Column(                                             
                                            height=350,                     
                                            # scroll = ft.ScrollMode.ALWAYS,
                                            controls=[
                                                ft.Container(
                                                    border_radius=10,     
                                                    # expand=True, 
                                                    alignment=ft.alignment.center,                                   
                                                    content=self.header_list_musics_ui, 
                                                ),                   
                                                ft.Container( 
                                                    border_radius=10,     
                                                    expand=True, 
                                                    alignment=ft.alignment.center,                                   
                                                    content=self.list_musics_ui,
                                                ),                           
                                            ]
                                        ),
                                        ft.Row(
                                                alignment=ft.MainAxisAlignment.END,
                                                controls=[
                                                    self.add_music_btn
                                                ]
                                        ),
                                        self.player_view.content_ui
                                    ],
                            ),
                    ]
                    
                )
            ),
            self.search_view.content_ui,
            ]
            ,alignment=ft.alignment.top_center
        )
    
         


