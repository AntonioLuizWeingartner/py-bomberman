import time
import pygame
import pygame.display


class Clock:

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

    def __init__(self, display: pygame.Surface):
        self.__display: pygame.Surface = display

    def start(self):
        pass
