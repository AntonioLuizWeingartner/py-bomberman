import time
import pygame
import pygame.display
import pygame.event
import pygame.image
import core.event_system
import core.entity_system
from typing import Callable, Dict, List

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

class ImageLoader:

    def __init__(self):
        self.__loaded_images: Dict[str, pygame.Surface] = dict()

    def load_image(self, path: str, alias: str):
        self.__loaded_images[alias] = pygame.image.load(path)
    
    def get_image(self, alias: str) -> pygame.Surface:
        return self.__loaded_images[alias]



class Keyboard:

    KEY_PRESSED = "press"
    KEY_RELEASE = "release"

    def __init__(self, event_system: core.event_system.EventSystem):
        self.__event_system = event_system

    def register_callback(self, key: int, mode: str, callback: Callable):
        self.__event_system.listen(str(key) + mode, callback)
    
    def remove_callback(self, key: int, mode: str, callback: Callable):
        self.__event_system.stop_listening(str(key) + mode, callback)

    def get_state(self) -> List[bool]:
        return pygame.key.get_pressed()

class Mouse:

    def __init__(self, event_system: core.event_system.EventSystem):
        self.__event_system = event_system
    
    def register_callback(self, mouse_key: int, mode: str, callback: Callable):
        self.__event_system.listen(str(mouse_key) + mode, callback)

    def remove_callback(self, mouse_key: int, mode: str, callback: Callable):
        self.__event_system.stop_listening(str(mouse_key) + mode, callback)

    def get_state(self):
        return pygame.mouse.get_pressed()


class Application:

    """
    Essa classe é um contêiner para todos os outros objetos da aplicação. Ela é responsável por gerenciar e inicializar todos os objetos do jogo.
    """
    def __init__(self, 
                display: pygame.Surface,
                clock: Clock,
                event_system: core.event_system.EventSystem,
                world: core.entity_system.World,
                app_timing_data: TimingData,
                img_loader: ImageLoader,
                keyboard: Keyboard,
                mouse: Mouse):
        
        self.__display: pygame.Surface = display
        self.__clock: Clock = clock
        self.__run_application: bool = True
        self.__paused: bool = False
        self.__event_system = event_system
        self.__world: core.entity_system.World = world
        self.__world.set_app(self)

        self.__timing_data = app_timing_data
        self.__image_loader = img_loader

        self.load_standard_assets()

        self.__keyboard = keyboard
        self.__mouse = mouse

    def load_standard_assets(self):
        self.__image_loader.load_image("assets/images/debug.png", "default")
        
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
            elif event.type == pygame.KEYDOWN:
                self.__event_system.broadcast(str(event.key) + Keyboard.KEY_PRESSED)
            elif event.type == pygame.KEYUP:
                self.__event_system.broadcast(str(event.key) + Keyboard.KEY_RELEASE)

    def update_game_world(self):
        if self.__paused is False:
            self.__world.update()

    def draw_game_world(self):
        self.__world.draw()

    def start(self):
        while self.__run_application:
            self.process_events()
            if time.perf_counter() - self.__timing_data.last_frame_time_point >= self.__timing_data.frame_period:
                self.__timing_data.last_frame_time_point = time.perf_counter()
                self.update_game_world()
                self.__display.fill((0,0,0))
                self.draw_game_world()
                pygame.display.flip()
    @property
    def event_system(self) -> core.event_system.EventSystem:
        return self.__event_System 
    
    @property
    def world(self) -> core.entity_system.World:
        return self.__world
    
    @property
    def image_loader(self) -> ImageLoader:
        return self.__image_loader

    @property
    def display(self) -> pygame.Surface:
        return self.__display

    @property
    def keyboard(self) -> Keyboard:
        return self.__keyboard

    @property
    def mouse(self) -> Mouse:
        return self.__mouse