import time
import pygame
import pygame.display
import pygame.event
import core.event_system
import core.entity_system

class Clock:
    """
    Essa classe representa um relógio que pode ser pausado. Útil para realizar animações.
    """

    def __init__(self):
        self.__pause_amount: float = 0
        self.__pause_time_point: float = 0
        self.__paused: bool = False

    def pause(self):
        if self.__paused is False:
            self.__paused = True
            self.__pause_time_point = time.perf_counter()
        
    def unpause(self):
        if self.__paused:
            self.__paused = False
            self.__pause_amount += time.perf_counter() - self.__pause_time_point

    def now(self):
        if self.__paused:
            return self.__pause_time_point
        else:
            return time.perf_counter() - self.__pause_amount

class TimingData:

    def __init__(self, fps: float):
        self.__fps = fps
        self.__frame_period = 1/fps
        self.__last_frame_time_point = 0

    @property
    def frame_period(self) -> float:
        return self.__frame_period
    
    @property
    def last_frame_time_point(self) -> float:
        return self.__last_frame_time_point

    @last_frame_time_point.setter
    def last_frame_time_point(self, new_time_point: float):
        self.__last_frame_time_point = new_time_point

    @property
    def target_fps(self) -> float:
        return self.__fps

class Application:

    """
    Essa classe é um contêiner para todos os outros objetos da aplicação. Ela é responsável por gerenciar e inicializar todos os objetos do jogo.
    """
    def __init__(self, 
                display: pygame.Surface,
                clock: Clock,
                event_system: core.event_system.EventSystem,
                world: core.entity_system.World,
                app_timing_data: TimingData):
        
        self.__display: pygame.Surface = display
        self.__clock: Clock = clock
        self.__run_application: bool = True
        self.__paused: bool = False
        self.__event_System = event_system
        self.__world: core.entity_system.World = world
        self.__world.set_app(self)

        self.__timing_data = app_timing_data

    def pause(self):
        if self.__paused is False:
            self.__paused = True
            self.__clock.pause()
    
    def unpause(self):
        if self.__paused:
            self.__paused = False
            self.__clock.unpause()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__run_application = False
    
    def update_game_world(self):
        if self.__paused is False:
            self.__world.update()



    def start(self):
        while self.__run_application:
            self.process_events()
            if self.__clock.now() - self.__timing_data.last_frame_time_point >= self.__timing_data.frame_period:
                pass

    @property
    def event_system(self) -> core.event_system.EventSystem:
        return self.__event_System