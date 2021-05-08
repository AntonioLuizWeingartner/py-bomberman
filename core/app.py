import time
import pygame
import pygame.display
import pygame.event
import core.event_system

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

class Application:

    """
    Essa classe é um contêiner para todos os outros objetos da aplicação. Ela é responsável por gerenciar e inicializar todos os objetos do jogo.
    """
    def __init__(self, 
                display: pygame.Surface,
                clock: Clock,
                event_system: core.event_system.EventSystem):
        
        self.__display: pygame.Surface = display
        self.__clock: Clock = clock
        self.__run_application: bool = True
        self.__event_System = event_system

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__run_application = False
    
    def start(self):
        while self.__run_application:
            self.process_events()
    
