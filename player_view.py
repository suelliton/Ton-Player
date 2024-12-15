import flet as ft
from enum import Enum

class PlayerState(Enum):
    PLAYING = "playing"
    PAUSED = "paused"
    STOPPED = "stopped"
    COMPLETED = "completed"

class PlayerView():
    _instance = None
    content_ui = None
    player = None
    progress_bar_ui = None
    duration_indicator_ui = None
    mute_unmute_btn = None
    volume_control = None
    state = PlayerState.STOPPED 
    selected_music = None
    playing_duration = 0
    volume = 0.33
    muted = False

    def __new__(cls,app, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PlayerView, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, app):
        if not hasattr(self, "_initialized"):
            print("Creating PlayerView")
            self.app = app          
            self.build()
    
    def play_music(self, music=None):
        if self.state == PlayerState.STOPPED:
            if not music:
                if not self.selected_music:
                    self.selected_music = self.app.listen_view.list_musics[0]
                    self.player.src = self.selected_music.path
                    # self.player.play()                
                else:
                    if self.state == PlayerState.STOPPED:
                        # self.player.src = self.selected_music.path
                        self.player.resume()                    
            else:
                self.selected_music = music
                self.player.src = self.selected_music.path
        elif self.state == PlayerState.PAUSED:
            self.player.resume()
        elif self.state == PlayerState.PLAYING:
            if music:
                self.selected_music = music
                self.player.src = self.selected_music.path
            
        self.player.update()
        self.state = PlayerState.PLAYING
        if self.selected_music:
            print(self.state.value, self.selected_music.title)
        else:
            print('No selected music')
        self.app.listen_view.update_list_musics_ui()

        self.update_btns()
    
    def pause_music(self):
        if self.state == PlayerState.PAUSED:
            self.player.resume()
            self.state = PlayerState.PLAYING
        elif self.state == PlayerState.PLAYING:
            self.player.pause()
            self.state = PlayerState.PAUSED
        self.player.update()

        self.update_btns()

    def stop_music(self):        
        # self.player.release()     
        self.player.pause()  
        self.player.seek(0) 
        self.player.update()
        self.state = PlayerState.STOPPED
        # print(self.state.value, self.selected_music.name)
        self.update_btns()
    
    def state_player_changed(self, e):
        print('State changed to ', e.data)
        if e.data == "completed":
            self.next_music()      

    def prev_music(self):
        print("------------------------------")
        print("Prev Music Actual", self.selected_music.title if self.selected_music else "None")
        # Garante que a playlist é convertida para uma lista
        musics_playlist = list(self.app.listen_view.list_musics)
        if self.selected_music:
            try:
                # Obtém o índice da música atual
                index = musics_playlist.index(self.selected_music)
            except ValueError:
                print("Erro: Música atual não encontrada na playlist!")
                return
            # Verifica se há uma próxima música
            if index > 0:
                next_music = musics_playlist[index - 1]
                self.play_music(next_music)  # Toca a próxima música
            else:
                print("Início da playlist!")
        else:
            print("Nenhuma música está tocando!")
        print("Prev Music Next", self.selected_music.title if self.selected_music else "None")
        print("------------------------------")

    def next_music(self):
        print("------------------------------")
        print("Next Music Actual", self.selected_music.title if self.selected_music else "None")
            
        # Garante que a playlist é convertida para uma lista
        musics_playlist = list(self.app.listen_view.list_musics)
        if self.selected_music:
            try:
                # Obtém o índice da música atual
                index = musics_playlist.index(self.selected_music)
            except ValueError:
                print("Erro: Música atual não encontrada na playlist!")
                return
            print('Index', index)
            # Verifica se há uma próxima música
            if index + 1 < len(musics_playlist):
                next_music = musics_playlist[index + 1]
                
                self.play_music(next_music)  # Toca a próxima música
            else:
                print("Fim da playlist!")
        else:
            print("Nenhuma música está tocando!, iniciando da primeira música")
            self.play_music(self.app.listen_view.list_musics[0])  


        print("Next Music Next", self.selected_music.title if self.selected_music else "None")
        print("------------------------------")

    # def volume_down(self):
    #     self.player.volume -= 0.1
    #     self.player.update()
    #     print('Volume', self.player.volume)

    # def volume_up(self):
    #     self.player.volume += 0.1
    #     self.player.update()
    #     print('Volume', self.player.volume)
    
    def set_volume(self, e):       
        self.volume = float(e.control.value/100)
        self.player.volume = self.volume
        self.player.update()

        self.muted = False
        self.mute_unmute_btn.icon = ft.icons.VOLUME_MUTE
        self.mute_unmute_btn.icon_color = ft.colors.WHITE
        self.mute_unmute_btn.update()

    def mute_unmute_volume(self, e):
        if self.muted:
            self.player.volume = self.volume
            e.control.icon = ft.icons.VOLUME_MUTE
            e.control.icon_color = ft.colors.WHITE
            e.control.update()
        else:
            self.player.volume = 0
            e.control.icon = ft.icons.VOLUME_OFF
            e.control.icon_color = ft.colors.RED_400
            e.control.update()
        self.muted = not self.muted
        self.player.update()

    
    
    def format_duration(self, milliseconds):
        total_seconds = milliseconds // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"
    
    def update_progress_bar_ui(self, e):
        position = int(e.data)
        if self.playing_duration > 0:  # Evita divisão por zero
            percent_position = ((position * 100) / self.playing_duration)/100
        else:
            percent_position = 0 
        self.progress_bar_ui.value = percent_position
        self.progress_bar_ui.update()
        self.duration_indicator_ui.value = self.format_duration(position)
        self.duration_indicator_ui.update()

    def update_playing_duration(self, e):
        self.playing_duration = int(e.data)
    
    def update_btns(self):
        if self.state == PlayerState.PLAYING:
            self.play_btn.bgcolor = ft.colors.BLUE_400
            self.pause_btn.bgcolor = None
        elif self.state == PlayerState.STOPPED:
            self.play_btn.bgcolor = None
            self.pause_btn.bgcolor = None
        elif self.state == PlayerState.PAUSED:    
            self.pause_btn.bgcolor = ft.colors.BLUE_400
            self.play_btn.bgcolor = None
        
        self.play_btn.update()
        self.pause_btn.update()

    def build(self):
        self.player = ft.Audio(
            src='Silent_short.mp3',
            autoplay= False,
            volume=0.33,
            balance=0,
            on_loaded=lambda _: self.player.play() ,
            on_duration_changed=lambda e: self.update_playing_duration(e),
            on_position_changed=lambda e: self.update_progress_bar_ui(e),
            on_state_changed=lambda e:  self.state_player_changed(e),
            # on_seek_complete=lambda _: self.next_music(),
        )
        self.app.page.overlay.append(self.player)



        self.progress_bar_ui = \
        ft.ProgressBar(value=0,color=ft.colors.BLUE_600)

        self.duration_indicator_ui = \
        ft.Text(value='0.00', color=ft.colors.WHITE, weight='bold')

        self.mute_unmute_btn = \
        ft.IconButton(
                    icon=ft.icons.VOLUME_MUTE,
                    tooltip='Mute',
                    icon_color=ft.colors.WHITE,
                    on_click=lambda e: self.mute_unmute_volume(e)
        )

        self.volume_control = \
        ft.Slider(
                min=0, 
                max=100,
                value=33,
                scale=0.8,
                # width=300,
                expand=True,                                    
                divisions=100,
                active_color=ft.colors.BLUE_600,                                     
                label="{value}%", 
                on_change=lambda e: self.set_volume(e)
        )

        self.play_btn = ft.IconButton(
                                    col=1,
                                    icon_size=35,
                                    icon=ft.icons.PLAY_CIRCLE,
                                    tooltip='Play',
                                    icon_color=ft.colors.WHITE, 
                                    on_click=lambda _: self.play_music())

        self.pause_btn = ft.IconButton(
                                    col=1,
                                    icon=ft.icons.PAUSE_CIRCLE,
                                    tooltip='Pause',
                                    icon_color=ft.colors.WHITE, 
                                    on_click=lambda _: self.pause_music())

        self.controls = \
        ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,           
                    controls=[   
                                ft.IconButton(col=1,icon=ft.icons.SKIP_PREVIOUS,tooltip='Previous', icon_color=ft.colors.WHITE, on_click=lambda _: self.prev_music()),
                                self.play_btn,
                                self.pause_btn,
                                ft.IconButton(col=1,icon=ft.icons.STOP_CIRCLE,tooltip='Stop',icon_color=ft.colors.WHITE, on_click=lambda _: self.stop_music()),
                                ft.IconButton(col=1,icon=ft.icons.SKIP_NEXT,tooltip='Next',icon_color=ft.colors.WHITE, on_click=lambda _: self.next_music()),       
                            ]
                ),
                ft.Row(
                    controls=[
                         ft.Column(
                            col=1,                          
                            controls=[
                                self.mute_unmute_btn, 
                            ]
                        ),
                        ft.Column(  
                            col=11,   
                            expand=True,                     
                            controls=[
                                self.volume_control,
                            ]
                        )
                    ]
                )
            ]
        )

        self.content_ui = \
        ft.Container(
            content= ft.Column(
                alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                        ft.Row(
                            # vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[                                
                                ft.Container(
                                    expand=10,
                                    # margin=ft.margin.only(left=20),
                                    padding = ft.padding.only(left=20),
                                    alignment=ft.alignment.center,
                                    content = self.progress_bar_ui
                                ),
                                ft.Container(
                                    expand=1,
                                    alignment=ft.alignment.center,
                                    content = self.duration_indicator_ui
                                )
                            ]
                        ),
                        self.controls   
                ]
            )
        )
