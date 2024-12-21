import vlc 
import time
from threading import Thread
from typing import Callable, Optional, List
from enum import Enum
from player import Player

class PlayerState(Enum):
    PLAYING = "playing"
    PAUSED = "paused"
    STOPPED = "stopped"
    COMPLETED = "completed"

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
        if self._src:
            self.load(self._src)   
        self.set_volume(self._volume)
    
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

    def _on_position_changed(self):        
        self._on_position_changed_func(self._audio.get_time()) 
    
    def _on_duration_changed(self):
        if self._on_duration_changed_func:
            self._on_duration_changed_func(self._duration)
    
    def _set_duration(self):
        self._duration = self._audio.get_length()
        self._on_duration_changed()
    
    def load(self, src):       
        self._src = src    
        self._audio = vlc.MediaPlayer(self._src)
        self._on_load()   
    
    def load_and_play(self, src):
        print('Load and play music', self.state)
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
        self._on_position_changed()
        time.sleep(0.5)
        self._set_duration()
        while self._audio.is_playing() or self.state == PlayerState.PAUSED:
            self._on_position_changed()
            time.sleep(1)

        self.state = PlayerState.STOPPED        
        self._on_completed()

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
        self._audio.stop()
        self.state = PlayerState.STOPPED
        self._on_stopped()
    
    def pause_release(self):
        if self.state == PlayerState.STOPPED:
            print('Player is stopped')
            return
        self._audio.pause()
        if self.state == PlayerState.PLAYING:
            print('Paused music')
            self.state = PlayerState.PAUSED
            self._on_paused()
        else:
            print('Release music')
            self.state = PlayerState.PLAYING
            self._on_release()
            self._on_play()
    
    def seek(self, position):
        self._audio.set_time(int(position))
    
    def set_volume(self, value):
        print(f'Setting volume to: {value}')
        self._volume = int(value*100)
        self._audio.audio_set_volume(self._volume)
    
    def mute_unmute(self):
        self._muted = not self._muted
        if self._muted:
            self.set_volume(0.0)
        else:
            self.set_volume(self._volume)

        
        
        
        