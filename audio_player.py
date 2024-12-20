import flet as ft

class AudioPlayer:
    def __init__(self, src=""):
        # Inicializa o player
        self.audio_control = ft.Audio(src=src, autoplay=False)
        self.src = src

    def set_source(self, src):
        # Atualiza a fonte do áudio e reinicia
        self.audio_control.src = src
        self.audio_control.autoplay = True
        self.audio_control.update()

    def get_control(self):
        # Retorna o controle de áudio para ser embutido no layout
        return self.audio_control

    def set_volume(self, volume):
        self.audio_control.volume = volume
        self.audio_control.update()

    def update(self):
        self.audio_control.update()