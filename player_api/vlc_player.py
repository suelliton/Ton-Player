from player_api.player import Player, PlayerState
import vlc 
import time
from threading import Thread
from typing import Callable, Optional, List

class VlcPlayer(Player):
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
            src: Optional[str] = None, 
            use_thread: bool = False,
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
            on_state_changed=on_state_changed
            )
        self._state = PlayerState.STOPPED
        self._src = src
        self._use_thread = use_thread
        self._thread = None
        self._audio = None
        self._duration = 0
        self._volume = volume
        self._autoplay = autoplay
        self._muted = False     
        self._music_changed = False
        self._on_position_changed_func = on_position_changed
        self._on_duration_changed_func = on_duration_changed       
    
    def initialize(self)-> None:
        if self._src:
            if self._autoplay:
                self.load_and_play(self._src)
            else:
                self.load(self._src)   
        self.set_volume(self._volume)
 
    def _on_position_changed(self)-> None:        
        self._on_position_changed_func(self._audio.get_time()) 
    
    def _on_duration_changed(self)-> None:
        if self._on_duration_changed_func:
            self._on_duration_changed_func(self._duration)
    
    def _set_duration(self)-> None:
        self._duration = self._audio.get_length()
        self._on_duration_changed()
    
    def load(self, src)-> None:       
        self._src = src    
        if not self._audio:
            print('======= Instanciando novo _audio')
            self._audio = vlc.MediaPlayer(self._src)
        else:
            print('======= Usando _audio já existente')
            self._audio.set_media(vlc.Media(self._src))
        
        self._on_load()   
    
    def load_and_play(self, src)-> None:
        print('Load and play music', self.state)
        if self.state in [PlayerState.PLAYING, PlayerState.PAUSED]:
            print('Stopping current music')
            self.stop()
        
        self._music_changed = True
        self.load(src)
        self.play()
    
    def is_playing(self)-> bool:
        return self._audio.is_playing()
    
    def is_muted(self)-> bool:
        return self._muted   
    
    def _task_play(self)-> None:
        self._audio.play()
        self._on_position_changed()
        time.sleep(0.2)
        self._set_duration()
        while self._audio.is_playing() or self.state == PlayerState.PAUSED and not self._music_changed:
            self._on_position_changed()
            print('is playing', self._audio.is_playing())
            time.sleep(0.9)
        print('EXIT of while')

        if self._music_changed:
            self._music_changed = False
        else:
            self.state = PlayerState.STOPPED        
            self._on_completed()

    def play(self)-> None:                       
        if self.state == PlayerState.PLAYING:            
            return      
      
        self.state = PlayerState.PLAYING
        self._on_play() 

        if self._use_thread:
            if self._thread:
                while self._music_changed:
                    print('Aguardando sair do loop')
            self._thread = Thread(target=self._task_play)
            self._thread.start()           
        else:  
            self._task_play()
    
    
    def stop(self)-> None:      
        self._audio.stop()
        self.state = PlayerState.STOPPED
        self._on_stopped()
    
    def pause_resume(self)-> None:
        if self.state == PlayerState.STOPPED:
            return
        self._audio.pause()
        if self.state == PlayerState.PLAYING:
            self.state = PlayerState.PAUSED
            self._on_paused()
        else:
            self.state = PlayerState.PLAYING
            self._on_resume()
            self._on_play()
    
    def seek(self, position)-> None:
        self._audio.set_time(int(position))
    
    def set_volume(self, value)-> None:
        self._volume = int(value*100)
        self._audio.audio_set_volume(self._volume)
    
    def mute_unmute(self)-> None:
        self._muted = not self._muted
        if self._muted:
            self.set_volume(0.0)
        else:
            self.set_volume(self._volume)
        
        