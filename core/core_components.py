from typing import List, Tuple
import pygame
import core.entity_system
import core.math
import abc

#TODO ADD SOUND COMPONENT
class SpriteRenderer(core.entity_system.DrawableComponent):

    def on_init(self):
        self._sprite: pygame.Surface = self.app.image_loader.get_image("default")
        self._display: pygame.Surface = self.app.display
        self._half_size = core.math.Vector2(self._sprite.get_width()/2, self._sprite.get_height()/2)

    def draw(self):
        self._display.blit(self._sprite, (self.transform.position - self._half_size).tuple)

    @property
    def sprite(self) -> pygame.Surface:
        return self._sprite

    @sprite.setter
    def sprite(self, new_sprite: pygame.Surface):
        self._sprite = new_sprite
        self._half_size = core.math.Vector2(self._sprite.get_width()/2, self._sprite.get_height()/2)


class Widget(abc.ABC):
    
    def __init__(self, position: core.math.Vector2, canvas):
        self.__screen_position: core.math.Vector2 = position
        self._half_size: pygame.Vector2 = None
        self._canvas = canvas

    @abc.abstractmethod
    def generate_surface(self) -> pygame.Surface:
        raise NotImplementedError()

    @property
    def position(self) -> core.math.Vector2:
        return self.__screen_position - self._half_size    

    @property
    def half_size(self) -> core.math.Vector2:
        return self._half_size

    @position.setter
    def position(self, new_pos: core.math.Vector2):
        self.__screen_position = new_pos
        self._canvas.render()

class Button(Widget):
    pass

    def __init__(self, position: core.math.Vector2, canvas):
        super().__init__(position, canvas)
        self.__foreground_color: Tuple[int,int,int, int] = (127,127,0,255)
        self.__text: str = "Test"
        self.__font_size: int = 16
        self.__font_color: Tuple[int,int,int,int] = (255,255,255,255)
        self.__surface_size: Tuple = (300,100)
        
    def generate_surface(self) -> pygame.Surface:
        text_surface = pygame.font.SysFont("Arial", self.__font_size, bold=True).render(self.__text,True, self.__font_color)
        surf = pygame.Surface(self.__surface_size, pygame.SRCALPHA)
        surf.fill(self.__foreground_color)
        surf.blit(text_surface, (self.__surface_size[0]/2-text_surface.get_width()/2, self.__surface_size[1]/2-text_surface.get_height()/2))
        self._half_size = pygame.Vector2(surf.get_width()/2, surf.get_height()/2)
        return surf

    def on_click(self):
        pass

    @property
    def foreground_color(self) -> Tuple[int, int, int, int]:
        return self.__foreground_color
    
    @foreground_color.setter
    def foreground_color(self, color: Tuple[int,int,int,int]):
        self.__foreground_color = color
        self._canvas.render()
    
    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, new_text: str):
        self.__text = new_text
        self._canvas.render()

    @property
    def font_size(self) -> int:
        return self.__font_size

    @font_size.setter
    def font_size(self, new_size: int):
        self.__font_size = new_size
        self._canvas.render()

    @property
    def size(self) -> Tuple[int, int]:
        return self.__surface_size
    
    @size.setter
    def size(self, new_size: Tuple[int,int]):
        self.__surface_size = new_size
        self._canvas.render()

class Canvas(SpriteRenderer):

    def on_init(self):
        super().on_init()
        screen_size = core.math.Vector2(self.app.display.get_width(), self.app.display.get_height())
        self._size = screen_size
        self.transform.position = screen_size/2
        self._widgets: List[Widget] = list()
        self._sprite: pygame.Surface = pygame.Surface(self._size.tuple, pygame.SRCALPHA)
        self._sprite.fill((0,0,0,0))
        self._half_size = self._size/2
        self._state: bool = True
        self.event_system.listen("1mouse_down", self.process_click_event)

    def process_click_event(self, click_pos: core.math.Vector2):
        if self._state:
            for widget in self._widgets:
                if isinstance(widget, Button):
                    if click_pos[0] >= (widget.position.x) and click_pos[0] <= (widget.position.x + widget.half_size.x*2) and click_pos[1] >= (widget.position.y) and click_pos[1] <= (widget.position.y +widget.half_size.y*2):
                        widget.on_click()

    def hide(self):
        self._state = False
        self._sprite.fill(0,0,0,0)
    
    def show(self):
        self._state = True
        self.render()

    def render(self):
        self._sprite.fill((0,0,0,0))
        for widget in self._widgets:
            surface = widget.generate_surface()
            self._sprite.blit(surface, widget.position.tuple)
    
    def add_widget(self, widget: Widget):
        if widget not in self._widgets:
            self._widgets.append(widget)
            self.render()

    def remove_widget(self, widget: Widget):
        if widget in self._widgets:
            self._widgets.remove(widget)
            self.render()