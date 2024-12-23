import flet as ft
from app import App

def show_notification(app: App, message: str, duration: int = 5000)-> None:
    snack = ft.SnackBar(
        duration=duration,
        content=ft.Text(
                    value=message,
                    color=ft.colors.WHITE,
                    weight='bold'
                    )
    )    
    app.page.add(snack)
    app.page.open(snack)  