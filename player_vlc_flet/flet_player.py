from player import Player
from typing import Callable, Optional, List
from enum import Enum
import flet as ft

class PlayerState(Enum):
    PLAYING = "playing"
    PAUSED = "paused"
    STOPPED = "stopped"
    COMPLETED = "completed"

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
            src: Optional[str] = None, 
            page: Optional[ft.Page] = None,
            on_load: Optional[Callable[[], None]] = None,
            on_play: Optional[Callable[[], None]] = None,            
            on_completed: Optional[Callable[[], None]] = None,            
            on_stopped: Optional[Callable[[], None]] = None,            
            on_paused: Optional[Callable[[], None]] = None,      
            on_release: Optional[Callable[[], None]] = None,               
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
            on_release=on_release
            )
        self._state = PlayerState.STOPPED
        self._src = src
        self._page = page
        self._audio = None
        self._duration = 0
        self._volume = 0.33
        self._muted = False     
        self._on_position_changed_func = on_position_changed
        self._on_duration_changed_func = on_duration_changed
        self._on_state_changed_func = on_state_changed
        self._observers: List[Callable[[PlayerState], None]] = []  # Callbacks list

        
        if self._on_state_changed_func:
            self.add_observer(self._on_state_changed_func)
    
    def initialize(self):
        self._audio = ft.Audio(
                                src='/musics/Silent_short.mp3', 
                                autoplay=False, 
                        )
        self._page.overlay.append(self._audio)
        self._page.update()
        self._audio.on_loaded = lambda e: self._audio.play()        
        self._audio.on_state_changed = lambda e: self.on_audio_state_changed(e)    
        self._audio.on_position_changed = lambda e: self._on_position_changed(e) 
        self._audio.on_duration_changed = lambda e: self._on_duration_changed(e)
        self.set_volume(self._volume)
        self._audio.update()       
    
    def on_audio_state_changed(self, e):   
        # print('AUDIO STATE', e.data)
        if e.data == "completed":
            self._on_completed()
            self.state = PlayerState.STOPPED
        # elif e.data == "paused":
        #     self._on_paused()
        #     self.state = PlayerState.PAUSED
        # elif e.data == "playing":
        #     self._on_play()
        #     self.state = PlayerState.PLAYING
         
    def add_observer(self, observer: Callable[[PlayerState], None]):
        """Add a new observer."""
        self._observers.append(observer)

    def remove_observer(self, observer: Callable[[PlayerState], None]):
        """Remove a observer."""
        self._observers.remove(observer)

    def _notify_observers(self):
        """Notify all observers about chandes in state."""
        for observer in self._observers:
            observer(self._state)
        
    def _on_position_changed(self, e):
        self._on_position_changed_func(int(e.data)) 
    
    def _on_duration_changed(self, e):
        self._duration = int(e.data)
        if self._on_duration_changed_func:
            self._on_duration_changed_func(self._duration)
    
    def _set_duration(self):
        ...
    
    def load(self, src):       
        self._src = src
        self._audio.src = self._src
        self._audio.update()
        self._on_load()   
    
    def load_and_play(self, src):
        print('Load and play music')
        if self.state in [PlayerState.PLAYING, PlayerState.PAUSED]:
            print('Stopping current music')
            self.stop()
        self.load(src)
        self.play()
    
    def is_playing(self):
        return self._audio.is_playing()
    
    def is_muted(self):
        return self._muted   
    
    def _task_play(self):
        self._audio.play()
    
    def play(self):      
        print('Play music')
        # thread = Thread(target=self.task_play)
        # thread.start()                
        if self.state == PlayerState.PLAYING:
            print('Music was in execution')
            return            
        self.state = PlayerState.PLAYING
        self._on_play() 
        self._task_play()    
    
    def stop(self):
        print('Stopped music')
        self._audio.pause()
        self.seek(0)
        self.state = PlayerState.STOPPED
        self._on_stopped()
    
    def pause_release(self):
        if self.state == PlayerState.STOPPED:
            print('Player is stopped')
            return
        if self.state == PlayerState.PLAYING:
            print('Paused music')
            self._audio.pause()
            self.state = PlayerState.PAUSED
            self._on_paused()
        else:
            print('Release music')
            self._audio.resume()     
            self.state = PlayerState.PLAYING     
            self._on_release()
            self._on_play()
    
    def seek(self, position):
        print('position seek', position)
        self._audio.seek(int(position))
    
    def set_volume(self, value):
        self._volume = value
        self._audio.volume = self.volume     
        self._audio.update()    
    
    def mute_unmute(self):        
        self._muted = not self._muted
        if self._muted:
            self.set_volume(0.0)
        else:
            self.set_volume(self._volume)

        
        

    