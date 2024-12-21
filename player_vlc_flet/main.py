import flet as ft
from vlc_player import VlcPlayer, PlayerState
from flet_player import FletPlayer
from utils import transform_millisseconds_to_mm_ss

class App():
    page = None
    content_ui = None
    message = None
    progressbar = None
    duration_total_ui = None
    position_ui = None
    volume_ui = None

    def __init__(self, page: ft.Page):
        self.page = page
    
    
    def build(self):
        self.page.window.max_height = 600
        self.page.window.max_width = 600

        def show_load():  
            if self.message:         
                self.message.value = "Loaded"
                self.message.update()

        def show_play():
            self.message.value = "Playing"
            self.message.update()

        def show_stopped():
            self.message.value = "Stopped"
            self.message.update()

        def show_completed():
            self.message.value = "Completed"
            self.message.update()

        def show_paused():
            self.message.value = "Paused"
            self.message.update()
        
        def on_state_changed(state: PlayerState):
            print(f"State changed to: {state.value}")
        
        def update_progress_bar(position_millisseconds):          
            self.progressbar.value = position_millisseconds
            self.progressbar.update()

            duration_formatted = transform_millisseconds_to_mm_ss(position_millisseconds)  
            self.position_ui.value = duration_formatted
            self.position_ui.update()
        
        def show_duration_total(duration_millissecondes):
            self.progressbar.max = duration_millissecondes
            self.progressbar.update()

            duration_formatted = transform_millisseconds_to_mm_ss(duration_millissecondes)   
                 
            self.duration_total_ui.value = duration_formatted
            self.duration_total_ui.update()
        
        def seek_music(e):   
            print(f'Seek to value: {e.control.value}')      
            self.player.seek(e.control.value)

        #Player initializations

        #Initialization for FletPlayer(ft.Audio)
        #relative path using assets_dir from flet config
        # silent_path = '/musics/silent_short.mp3' 
        # flower_path = '/musics/jisoo-flower.mp3'
        # whiplash_path = '/musics/aespa-whiplash.mp3'
        # supernova_short_path = '/musics/aespa-supernova-short.mp3'
        # drama_path = '/musics/aespa-drama.mp3'

        # self.player = FletPlayer(
        #     src=silent_path,
        #     page=self.page,
        #     on_load=show_load,
        #     on_play=show_play,
        #     on_stopped=show_stopped,
        #     on_completed=show_completed,
        #     on_paused=show_paused,
        #     on_position_changed=update_progress_bar,
        #     on_duration_changed=show_duration_total,
        #     on_state_changed=on_state_changed
        # )
        #self.player.initialize()        


        #Initialization for VlcPlayer(VLC player library)
        #relative path from actual dir, don't understand assets_dir config from flet
        silent_path = './assets/musics/silent_short.mp3' 
        flower_path = './assets/musics/jisoo-flower.mp3'
        whiplash_path = './assets/musics/aespa-whiplash.mp3'
        supernova_short_path = './assets/musics/aespa-supernova-short.mp3'
        drama_path = './assets/musics/aespa-drama.mp3'
        self.player = VlcPlayer(
            src = silent_path,                   
            on_load=show_load,
            on_play=show_play,
            on_stopped=show_stopped,
            on_completed=show_completed,
            on_paused=show_paused,
            on_position_changed = update_progress_bar,
            on_duration_changed=show_duration_total,
            on_state_changed=on_state_changed
        )
        self.player.initialize()        


        #UI elements initialization
    
        self.message = ft.Text(value="Olá")        

        self.progressbar = ft.Slider(value=0, label="{value}",max=270000, min=0, divisions=1000, width=300,on_change=lambda e: seek_music(e))
                
        self.duration_total_ui = ft.Text(value='0:00')
         
        self.position_ui = ft.Text(value='0:00')

        self.volume_ui = ft.Slider(
            value=0.33,
            min=0,
            max=1,
            divisions=100,
            on_change=lambda e:self.player.set_volume(e.control.value)
        )    

        self.content_ui = \
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(value='State',weight='bold'),
                                ft.Container(padding=ft.padding.all(10),content=self.message),
                                ft.Text(value='Progressbar',weight='bold'),
                                ft.Container(padding=ft.padding.all(10),content=self.progressbar),
                                ft.Text(value='Duration total',weight='bold'),
                                ft.Container(padding=ft.padding.all(10),content=self.duration_total_ui),
                                ft.Text(value='Actual position',weight='bold'),
                                ft.Container(padding=ft.padding.all(10),content=self.position_ui),                
                                ft.Text(value='Volume control',weight='bold'),
                                ft.Container(padding=ft.padding.all(10),content=self.volume_ui), 
                            ]
                        ),
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(value='Musics',weight='bold'),
                                ft.ElevatedButton(text='Load and play Flower', on_click=lambda e:self.player.load_and_play(flower_path)),
                                ft.ElevatedButton(text='Load and play Whiplash', on_click=lambda e:self.player.load_and_play(whiplash_path)),
                                ft.ElevatedButton(text='Load and play Supernova short',  on_click=lambda e:self.player.load_and_play(supernova_short_path)),
                                ft.ElevatedButton(text='Load and play Drama',  on_click=lambda e:self.player.load_and_play(drama_path)),
                                ft.ElevatedButton(text='Play', bgcolor='blue', on_click=lambda e:self.player.play()),
                                ft.ElevatedButton(text='Stop', bgcolor='red', on_click=lambda e:self.player.stop()),
                                ft.ElevatedButton(text='Pause', bgcolor='grey', on_click=lambda e:self.player.pause_release()),
                            ]
                        )
                    ]
                )
            ]
        )        

        self.page.add(self.content_ui)
        self.page.update()

def main(page:ft.Page):
    app = App(page)
    app.build()


ft.app(target=main)