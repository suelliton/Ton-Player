import flet as ft
from peewee import fn
from models import Playlist

class SearchView():
    _instance = None
    content_ui = None
    search_field = None
    list_results_ui = None
    playlists = None
    def __new__(cls,app, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SearchView, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, app):
        if not hasattr(self, "_initialized"):
            print("Creating SearchView")
            self.app = app          
            self.build()

    def loss_focus(self, e):
        self.list_results_ui.visible = False
        self.list_results_ui.update()

    def select_playlist(self, e, p):
        self.search_field.value = None
        self.search_field.update()
        self.list_results_ui.controls.clear()
        self.list_results_ui.visible = False
        self.list_results_ui.update()
        self.app.left_view.select_playlist(e, p)

    def search(self,e):
        if len(e.control.value.strip()) == 0:
            self.list_results_ui.controls.clear()
            self.list_results_ui.visible = False
            self.list_results_ui.update()
            return 
        def highlight_item(e, p):       
            e.control.bgcolor = ft.colors.BLACK45 if e.data == "true" else ft.colors.BLACK12
            e.control.update()  # Atualiza o elemento

        self.playlists = Playlist.select().where(Playlist.name.contains(e.control.value))
        self.list_results_ui.visible = True
        self.list_results_ui.controls.clear()
        self.list_results_ui.controls = [
             ft.Container(
                    bgcolor=ft.colors.BLACK12,
                    padding=ft.padding.all(10),
                    border=ft.Border(
                        bottom=ft.BorderSide(
                            width=3,
                            color= ft.colors.BLACK12
                        )
                    ),
                    ink_color=ft.colors.WHITE,
                    on_click=lambda e, p=playlist: self.select_playlist(e, p),
                    on_hover=lambda e, p=playlist: highlight_item(e, p),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Image(
                                src=playlist.coverart,
                                fit=ft.ImageFit.COVER,
                                width=50
                            ),
                            ft.Container(
                                expand=True,
                                content=ft.Text(
                                    playlist.name,
                                    text_align=ft.TextAlign.START,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                    max_lines=1,
                                    color= ft.colors.WHITE
                                )
                            ),                          
                        ]
                    )
                ) for playlist in self.playlists
        ]
        self.list_results_ui.update()
    def build(self):
        self.search_field = ft.TextField(
                                hint_text='Search',
                                hint_style=ft.TextStyle(color=ft.colors.WHITE),
                                text_align='center',
                                border_radius=20,
                                height=40,
                                color=ft.colors.WHITE,
                                bgcolor=ft.colors.with_opacity(color='#34495e', opacity=1),
                                on_change=lambda e: self.search(e),
                                # on_blur=lambda e: self.loss_focus(e)
                                )
        self.list_results_ui = ft.ListView(visible=False)
        self.content = \
        ft.Container(
            bgcolor=ft.colors.with_opacity(color='#34495e', opacity=1),
            width=400,
            border_radius=20,    
            margin=ft.margin.only(top=10, left=10, right=10),                   
            content=\
            ft.Column(                       
                controls=[
                    self.search_field,
                    self.list_results_ui
                ]
            )
            
        )
        