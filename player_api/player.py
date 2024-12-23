from abc import ABC, abstractmethod
from typing import Callable, Optional, List
from enum import Enum

class PlayerState(Enum):#this enum class control the internal state of player
    PLAYING = "playing"
    PAUSED = "paused"
    STOPPED = "stopped"
    COMPLETED = "completed"

class Player(ABC):
    def __init__(
            self,
            on_load: Optional[Callable[[], None]] = None,
            on_play: Optional[Callable[[], None]] = None,            
            on_completed: Optional[Callable[[], None]] = None,            
            on_stopped: Optional[Callable[[], None]] = None,            
            on_paused: Optional[Callable[[], None]] = None,   
            on_resume: Optional[Callable[[], None]] = None,   
            on_state_changed: Optional[Callable[[], None]] = None,   
            )-> None:
        self._on_load_func = on_load
        self._on_play_func = on_play
        self._on_completed_func = on_completed
        self._on_stopped_func = on_stopped
        self._on_paused_func = on_paused
        self._on_resume_func = on_resume
        self._on_state_changed_func = on_state_changed

        self._observers: List[Callable[[PlayerState], None]] = []  # Callbacks list
        
        if self._on_state_changed_func:
            self.add_observer(self._on_state_changed_func)
        
    def add_observer(self, observer: Callable[[PlayerState], None])-> None:
        """Add a new observer."""
        self._observers.append(observer)

    def remove_observer(self, observer: Callable[[PlayerState], None])-> None:
        """Remove a observer."""
        self._observers.remove(observer)

    def _notify_observers(self)-> None:
        """Notify all observers about chandes in state."""
        for observer in self._observers:
            observer(self._state)

    def _on_load(self)-> None:
        print('Loaded music')
        if self._on_load_func:
            self._on_load_func()

    def _on_play(self)-> None:
        print('Played music')
        if self._on_play_func:
            self._on_play_func()
    
    def _on_completed(self)-> None:
        print('Completed music')
        if self._on_completed_func:
            self._on_completed_func()

    def _on_stopped(self)-> None:
        print('Stopped music')
        if self._on_stopped_func:
            self._on_stopped_func()

    def _on_paused(self)-> None:
        print('Paused music')
        if self._on_paused_func:
            self._on_paused_func()
    
    def _on_resume(self)-> None:
        print('Resume music')
        if self._on_resume_func:
            self._on_resume_func()    

    @abstractmethod
    def initialize(self)-> None:
        "Abstract method to start the class behavior"
        ...

    @abstractmethod
    def _on_position_changed(self)-> None:
        "Abstract method trigged when pass the seconds music"
        ...

    @abstractmethod
    def _on_duration_changed(self)-> None:
        "Abstract method trigged when starts a new play execution"
        ...

    @abstractmethod
    def _set_duration(self)-> None:
        "Abstract method intern of class to set a duration attribute"
        ...

    @abstractmethod
    def _task_play(self)-> None:
        "Abstract method intern to task of play music"
        ...

    @abstractmethod
    def load(self, src: str)-> None:
        "Abstract method to load a src music"
        ...

    @abstractmethod
    def load_and_play(self, src: str)-> None:
        "Abstract method to load and automatically play a music"
        ...

    @abstractmethod
    def is_playing(self)-> bool:
        "Abstract method to returns if player is in execution or no"
        ...

    @abstractmethod
    def is_muted(self)-> bool:
        "Abstrac method to returns if player is muted or no"
        ...

    @abstractmethod
    def play(self)-> None:
        "Abstract method called to play a music, call _task_play"
        ... 

    @abstractmethod
    def stop(self)-> None:
        "Abstract method called to stop execution music definitively, but don't erase data class"
        ...

    @abstractmethod
    def pause_resume(self)-> None:
        "Abstract method called to pause or release the execution music"
        ...

    @abstractmethod
    def seek(self, position: int)-> None:
        "Abstract method called to jump to specific part of music"
        ...

    @abstractmethod
    def set_volume(self, value: float)-> None:
        "Abstract method called to set volume player"
        ...

    @abstractmethod
    def mute_unmute(self)-> None:
        "Abstract method called to mute or unmute player"
        ...
