from player_api.player import Player, PlayerState
# from player import Player, PlayerState
from typing import Callable, Optional, List
import flet as ft

class FletPlayer(Player):
    @property
    def src(self)-> str:
        return self._src
    
    @src.setter
    def src(self, value: str):       
        self._src = value
      
    @property
    def duration(self)-> any:
        return self._duration
    
    @duration.setter
    def duration(self, value: any):       
        self._duration = value

    @property
    def muted(self)-> bool:
        return self._muted
    
    @muted.setter
    def muted(self, value: bool):       
        self._muted = value

    @property
    def volume(self)-> float:
        return self._volume
    
    @volume.setter
    def volume(self, value: float):       
        self._volume = value

    @property
    def state(self) -> PlayerState:   
        return self._state

    @state.setter
    def state(self, value: PlayerState):    
        if value != self._state:  
            self._state = value
            self._notify_observers()

    def __init__(
            self, 
            page: ft.Page,  #required,
            src: Optional[str] = None, 
            autoplay: Optional[bool] = False, 
            volume: Optional[float] = 0.33,
            on_load: Optional[Callable[[], None]] = None,
            on_play: Optional[Callable[[], None]] = None,            
            on_completed: Optional[Callable[[], None]] = None,            
            on_stopped: Optional[Callable[[], None]] = None,            
            on_paused: Optional[Callable[[], None]] = None,      
            on_resume: Optional[Callable[[], None]] = None,               
            on_position_changed: Optional[Callable[[], None]] = None,            
            on_duration_changed: Optional[Callable[[], None]] = None,            
            on_state_changed: Optional[Callable[[], None]] = None,            
            ):
        super().__init__(
            on_load=on_load,
            on_play=on_play,
            on_completed=on_completed,
            on_stopped=on_stopped,
            on_paused=on_paused,
            on_resume=on_resume,
            on_state_changed = on_state_changed
            )
        self._state = PlayerState.STOPPED
        self._src = src
        self._autoplay = autoplay
        self._page = page
        self._audio = None
        self._duration = 0
        self._volume = volume 
        self._muted = False     
        self._on_position_changed_func = on_position_changed
        self._on_duration_changed_func = on_duration_changed
    
    def initialize(self)-> None:
        self._audio = ft.Audio(src=self._src, autoplay=self._autoplay)
        self._page.overlay.append(self._audio)
        self._page.update()
        self._audio.on_loaded = lambda e: self._audio.play()        
        
        if self._on_state_changed_func:
            self._audio.on_state_changed = lambda e: self.on_audio_state_changed(e)   
        if self._on_position_changed_func: 
            self._audio.on_position_changed = lambda e: self._on_position_changed(e) 
        if self._on_duration_changed_func:
            self._audio.on_duration_changed = lambda e: self._on_duration_changed(e)
        self.set_volume(self._volume)
        self._audio.update()       
    
    def on_audio_state_changed(self, e)-> None:   
        if e.data == "completed":#another values for this states can be: paused, playing
            self._on_completed()
            self.state = PlayerState.STOPPED    
        
    def _on_position_changed(self, e)-> None:
        self._on_position_changed_func(int(e.data)) 
    
    def _on_duration_changed(self, e)-> None:
        self._duration = int(e.data)
        if self._on_duration_changed_func:
            self._on_duration_changed_func(self._duration)
    
    def _set_duration(self)-> None:
        "No implemented"
        ...
    
    def load(self, src)-> None:       
        self._src = src
        self._audio.src = self._src
        self._audio.update()
        self._on_load()   
    
    def load_and_play(self, src)-> None:       
        if self.state in [PlayerState.PLAYING, PlayerState.PAUSED]:           
            self.stop()
        self.load(src)
        self.play()
    
    def is_playing(self)-> bool:
        return self.state == PlayerState.STOPPED
    
    def is_muted(self)-> bool:
        return self._muted   
    
    def _task_play(self)->None:
        self._audio.play()
    
    def play(self)-> None:#this method should not be called diretc, only for load_and_play method 
        # thread = Thread(target=self.task_play)
        # thread.start()                
        if self.state == PlayerState.PLAYING:            
            return            
        self.state = PlayerState.PLAYING
        self._on_play() 
        self._task_play()    
    
    def stop(self)-> None:        
        self._audio.pause()
        self.seek(0)
        self.state = PlayerState.STOPPED
        self._on_stopped()
    
    def pause_resume(self)-> None:
        if self.state == PlayerState.STOPPED:           
            return
        if self.state == PlayerState.PLAYING:            
            self._audio.pause()
            self.state = PlayerState.PAUSED
            self._on_paused()
        else:            
            self._audio.resume()     
            self.state = PlayerState.PLAYING     
            self._on_resume()
            self._on_play()
    
    def seek(self, position)-> None:       
        self._audio.seek(int(position))
    
    def set_volume(self, value)-> None:
        self._volume = value
        self._audio.volume = self.volume     
        self._audio.update()    
    
    def mute_unmute(self)-> None:        
        self._muted = not self._muted
        if self._muted:
            self.set_volume(0.0)
        else:
            self.set_volume(self._volume)

    