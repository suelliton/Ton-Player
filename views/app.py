import flet as ft
from models import Playlist, create_db_and_tables
from views.left_view import LeftView 
from views.listen_view import ListenView
from views.download_view import DownloadView

class App():
    _instance = None  #Unique class instance 
    page = None
    drawer_ui = None
    header_ui = None
    open_drawer_btn = None   
    left_view = None
    listen_view = None    
    stack_main = None
    tab_listen = None
    tab_download = None
    title_tab_selected = None   
    is_sm = False
    selected_tab = 'tab_listen'

    def __new__(cls, page: ft.Page, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(App, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, page: ft.Page):
        if not hasattr(self, "_initialized"):
            self.page = page
            self.initialize()            

    def initialize(self):
        create_db_and_tables()
        self.create_default_playlist()              
        #Events
        self.page.on_resized = self.on_resize

    def on_resize(self, e):      
        if e.width < 768:
            self.left_view.content.visible = False
            self.open_drawer_btn.visible = True           
            self.is_sm = True 
            if self.selected_tab == 'tab_listen': 
                #hide album column and duration from list_musics_ui header
                self.listen_view.header_list_musics_ui.controls[2].visible=False
                self.listen_view.header_list_musics_ui.controls[3].visible=False
        else:  
            self.left_view.content.visible = True           
            self.open_drawer_btn.visible = False
            self.is_sm = False
            if self.selected_tab == 'tab_listen': 
                #show album column and duration from list_musics_ui header
                self.listen_view.header_list_musics_ui.controls[2].visible=True
                self.listen_view.header_list_musics_ui.controls[3].visible=True
        
        self.listen_view.update_list_musics_ui()       
        
        self.listen_view.header_list_musics_ui.update()
        self.page.update()

    # def get_playlists(self):
    #     return Playlist.select()
    
    def create_default_playlist(self,):
        if Playlist.select().count() == 0:
            Playlist.create(name='All')
    
    def select_listen_view(self, e):
        print('Selected listen view')
        self.selected_tab = self.tab_listen.key
        self.stack_main.controls.clear()
        self.stack_main.controls.append(self.tab_listen) 
        self.stack_main.update()

        self.title_tab_selected.value = 'Listen'
        self.title_tab_selected.update()

    def select_download_view(self, e):
        print('Selected download view')
        self.selected_tab = self.tab_download.key
        self.stack_main.controls.clear()
        self.stack_main.controls.append(self.tab_download) 
        self.stack_main.update()

        self.title_tab_selected.value = 'Download'
        self.title_tab_selected.update()
            
    def build(self):
        self.page.window.width = 400
        self.page.window.height = 720
        self.page.title = 'Ton player'
        self.page.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.bgcolor = "#222f3e" #ft.colors.with_opacity(color=ft.colors.BLUE_400, opacity=0.3)

        self.left_view = LeftView(self)
        
        self.drawer_ui = ft.NavigationDrawer(
            bgcolor= "#222f3e",
            shadow_color= ft.colors.with_opacity(color=ft.colors.BLUE_700, opacity=1),
            controls=[
                ft.Column(
                controls = [
                    ft.Container(                    
                        padding=ft.padding.all(30),
                        content=ft.Column(
                            
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.END,
                                        controls=[
                                            ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=ft.colors.WHITE, on_click=lambda e:self.page.close(self.drawer_ui)),
                                        ]
                                    ),
                                    ft.Text(value='Playlists',weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                                    ft.Divider(),
                                    self.left_view.playlists_ui, 
                                    ft.Divider(),
                                    self.left_view.add_playlist_btn,
                                    ft.Divider(),
                            ] 
                        )
                    )                   
                ]
            )]
        )

        self.open_drawer_btn = ft.IconButton(
            visible=True,
            icon_color=ft.colors.WHITE,
            icon=ft.icons.MENU,
            icon_size=20,
            on_click=lambda _: self.page.open(self.drawer_ui),
        )   
        
        self.title_tab_selected = ft.Text('Listen', color=ft.colors.WHITE,size=20, weight='bold')

        self.header_ui = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                height=30,
                controls=[
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        controls=[self.open_drawer_btn]
                    ),                
                    ft.Column(                        
                        controls=[
                            ft.Container(
                                padding=ft.padding.all(10),
                                content=self.title_tab_selected
                            )
                        ]
                    )
                ]
            )
       
        self.page.add(
            self.header_ui
        )
       
        self.listen_view = ListenView(self)
        self.download_view = DownloadView(self)

        
        self.tab_listen = ft.Container(
                    key='tab_listen',
                    # width=400,
                    height=620,
                    # col={'xs':12, 'sm':9}, 
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.BLACK12,
                    border_radius=16,
                    # shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.with_opacity(opacity=0.4,color=ft.colors.BLACK)),
                    content=ft.Column(
                        controls=[
                                # ft.Text(
                                #     value="Listen",
                                #     color=ft.colors.BLUE_500,
                                #     size=25
                                # ),
                                self.listen_view.content
                        ]
                    )
        )
    
        self.tab_download = ft.Container(
                    key='tab_download',
                    # width=400,
                    height=620,
                    # col={'xs':12, 'sm':9}, 
                    alignment=ft.alignment.center,
                    # bgcolor=ft.colors.WHITE,
                    border_radius=16,
                    shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.with_opacity(opacity=0.4,color=ft.colors.BLACK)),
                    content=ft.Column(
                        controls=[
                                # ft.Text(
                                #     value="Download",
                                #     color=ft.colors.BLUE_500,
                                #     size=25
                                # ),
                                self.download_view.content
                        ]
                    )
        )
    
       

        self.page.bottom_appbar = ft.BottomAppBar(
            bgcolor=ft.colors.BLACK12,
            height=60,
            # shape= ft.NotchShape.CIRCULAR,            
            content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                                ft.IconButton(icon=ft.icons.QUEUE_MUSIC,icon_color=ft.colors.WHITE, icon_size=28, on_click=lambda e : self.select_listen_view(e)),
                                ft.IconButton(icon=ft.icons.DOWNLOAD,icon_color=ft.colors.WHITE, icon_size=28,on_click=lambda e : self.select_download_view(e)),
                            ]
            )            
        )
        
        self.stack_main = \
        ft.Stack(            
            controls = [           
                ft.ResponsiveRow(    
                    columns=12,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                            self.tab_listen
                                # self.left_view.content_ui,
                                # self.main_view.content_ui
                            ],                        
                )
            ],
        )
    
        self.page.add(self.stack_main)
        self.left_view.update_playlists_ui()
        self.listen_view.update_list_musics_ui()
        self.page.update()
       






