# from player_api.player import Player, PlayerState
from player import Player, PlayerState
from typing import Callable, Optional, List

class PygamePlayer(Player):
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
