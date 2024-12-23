import flet as ft
from enum import Enum

class NotificationType(Enum):
    INFO = "info"
    SUCCESS = "success"
    ERROR = "error"

def show_notification(app: any, message: str, duration: int = 5000, type: str = NotificationType.INFO)-> None:
    bgcolor = None
    if type == NotificationType.INFO:
        bgcolor = ft.colors.BLUE_400
    elif type == NotificationType.SUCCESS:
        bgcolor = ft.colors.GREEN_400
    elif type == NotificationType.ERROR:
        bgcolor = ft.colors.RED_400

    snack = ft.SnackBar(
        duration=duration,
        bgcolor=bgcolor,
        content=ft.Text(
                    value=message,
                    color=ft.colors.WHITE,
                    weight='bold'
                    )
    )    
    app.page.add(snack)
    app.page.open(snack)  