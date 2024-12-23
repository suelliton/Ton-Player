import flet as ft
from vlc_player import VlcPlayer, PlayerState
# from flet_player import FletPlayer
from utils import transform_millisseconds_to_mm_ss

class Indicators(ft.Container):
    def __init__(self, app):
        self.app = app
        super().__init__()

        
        self.build()
    
    def show_load(self):  
        if self.message:         
            self.message.value = "Loaded"
            self.message.update()

    def show_play(self):
        self.message.value = "Playing"
        self.message.update()

    def show_stopped(self):
        self.message.value = "Stopped"
        self.message.update()

    def show_completed(self):
        self.message.value = "Completed"
        self.message.update()

    def show_paused(self):
        self.message.value = "Paused"
        self.message.update()
    
    def on_state_changed(self,state: PlayerState):
        print(f"State changed to: {state.value}")
    
    def update_progress_bar(self, position_millisseconds):          
        self.progressbar.value = position_millisseconds
        self.progressbar.update()

        duration_formatted = transform_millisseconds_to_mm_ss(position_millisseconds)  
        self.position_ui.value = duration_formatted
        self.position_ui.update()
    
    def show_duration_total(self, duration_millissecondes):
        self.progressbar.max = duration_millissecondes
        self.progressbar.update()

        duration_formatted = transform_millisseconds_to_mm_ss(duration_millissecondes)   
                
        self.duration_total_ui.value = duration_formatted
        self.duration_total_ui.update()
    
    def seek_music(self, e):   
        print(f'Seek to value: {e.control.value}')      
        self.app.player.seek(e.control.value)
        
    
    def build(self):            
        self.message = ft.Text(value="message")    

        self.progressbar = ft.Slider(value=0, label="{value}",max=270000, min=0, divisions=1000, width=300,on_change=lambda e: self.seek_music(e))
                
        self.duration_total_ui = ft.Text(value='0:00')
         
        self.position_ui = ft.Text(value='0:00')

        self.volume_ui = ft.Slider(
            value=0.33,
            min=0,
            max=1,
            divisions=100,
            on_change=lambda e:self.app.player.set_volume(e.control.value)
        )    
        self.content = \
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
        )

class ListMusics(ft.Container):
    def __init__(self, app):
        self.app = app
        super().__init__()
        self.width = 200
        # self.height= 100
        self.padding = ft.padding.all(20)
        self.content = self.build()
    
    
    def build(self):
        return ft.ListView(
            spacing=20,
            controls=[
                ft.ElevatedButton(text='Load and play Flower', on_click=lambda e:self.app.player.load_and_play(self.app.flower_path)),
                ft.ElevatedButton(text='Load and play Whiplash', on_click=lambda e:self.app.player.load_and_play(self.app.whiplash_path)),
                ft.ElevatedButton(text='Load and play Supernova short',  on_click=lambda e:self.app.player.load_and_play(self.app.supernova_short_path)),
                ft.ElevatedButton(text='Load and play Drama',  on_click=lambda e:self.app.player.load_and_play(self.app.drama_path)),
                ft.ElevatedButton(text='Play', bgcolor='blue', on_click=lambda e:self.app.player.play()),
                ft.ElevatedButton(text='Stop', bgcolor='red', on_click=lambda e:self.app.player.stop()),
                ft.ElevatedButton(text='Pause', bgcolor='grey', on_click=lambda e:self.app.player.pause_resume()),

            ]
        )
      

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

        indicators = Indicators(self)
        list_musics_ui = ListMusics(self)
  

        self.content_ui = \
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(value='Indicators',color=ft.colors.BLUE_300,weight='bold'),
                                indicators
                            ]
                        ),
                        
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(value='Musics',color=ft.colors.BLUE_300,weight='bold'),
                                list_musics_ui,
                            ]
                        )
                    ]
                )
            ]
        )        

        self.page.add(self.content_ui)
        self.page.update()
    
        #Player initializations

        ################################### FLET PLAYER #####################################

        #Initialization for FletPlayer(ft.Audio)
        #relative path using assets_dir from flet config
        # self.silent_path = '/musics/silent-short.mp3' 
        # self.flower_path = '/musics/jisoo-flower.mp3'
        # self.whiplash_path = '/musics/aespa-whiplash.mp3'
        # self.supernova_short_path = '/musics/aespa-supernova-short.mp3'
        # self.drama_path = '/musics/aespa-drama.mp3'

        # self.player = FletPlayer(
        #     page=self.page,
        #     src=self.silent_path,
        #     on_load=show_load,
        #     on_play=show_play,
        #     on_stopped=show_stopped,
        #     on_completed=show_completed,
        #     on_paused=show_paused,
        #     on_position_changed=update_progress_bar,
        #     on_duration_changed=show_duration_total,
        #     on_state_changed=on_state_changed
        # )
        # self.player.initialize()      
         
        ################################### FLET PLAYER #####################################  

        ################################### VLC PLAYER #####################################
        #Initialization for VlcPlayer(VLC player library)
        #relative path from actual dir, don't understand assets_dir config from flet
        self.silent_path = './assets/musics/silent-short.mp3' 
        self.flower_path = './assets/musics/jisoo-flower.mp3'
        self.whiplash_path = './assets/musics/aespa-whiplash.mp3'
        self.supernova_short_path = './assets/musics/aespa-supernova-short.mp3'
        self.drama_path = './assets/musics/aespa-drama.mp3'
        self.player = VlcPlayer(
            src = self.silent_path,   
            use_thread=True,                
            on_load=indicators.show_load,
            on_play=indicators.show_play,
            on_stopped=indicators.show_stopped,
            on_completed=indicators.show_completed,
            on_paused=indicators.show_paused,
            on_position_changed = indicators.update_progress_bar,
            on_duration_changed=indicators.show_duration_total,
            on_state_changed=indicators.on_state_changed
        )
        self.player.initialize()        

        ################################### VLC PLAYER #####################################


        #UI elements initialization
    
        
       

def main(page:ft.Page):
    app = App(page)
    app.build()


ft.app(target=main)