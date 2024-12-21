from abc import ABC, abstractmethod
from typing import Callable, Optional

class Player(ABC):
    def __init__(
            self,
            on_load: Optional[Callable[[], None]] = None,
            on_play: Optional[Callable[[], None]] = None,            
            on_completed: Optional[Callable[[], None]] = None,            
            on_stopped: Optional[Callable[[], None]] = None,            
            on_paused: Optional[Callable[[], None]] = None,   
            on_release: Optional[Callable[[], None]] = None,   
            )-> None:
        self._on_load_func = on_load
        self._on_play_func = on_play
        self._on_completed_func = on_completed
        self._on_stopped_func = on_stopped
        self._on_paused_func = on_paused
        self._on_release_func = on_release
        # super().__init__()

    def _on_load(self)-> None:
        print('Loaded music')
        if self._on_load_func:
            self._on_load_func()

    def _on_play(self)-> None:
        print('Played music')
        if self._on_play_func:
            self._on_play_func()
    
    def _on_completed(self)-> None:
        print('Completed music execution')
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
    
    def _on_release(self)-> None:
        print('Release music')
        if self._on_release_func:
            self._on_release_func()
   
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
    def pause_release(self)-> None:
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
