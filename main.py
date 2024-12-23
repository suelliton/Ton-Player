import flet as ft
from views.app import App

def main(page: ft.Page):
    app = App(page)
    app.build()    

if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets')