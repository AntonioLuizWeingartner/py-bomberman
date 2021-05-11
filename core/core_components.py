import pygame
import core.entity_system
import core.math

#TODO ADD SOUND COMPONENT
class SpriteRenderer(core.entity_system.DrawableComponent):

    def on_init(self):
        self.__sprite: pygame.Surface = self.app.image_loader.get_image("default")
        self.__display: pygame.Surface = self.app.display
        self.__half_size = core.math.Vector2(self.__sprite.get_width()/2, self.__sprite.get_height()/2)

    def draw(self):
        self.__display.blit(self.__sprite, (self.transform.position - self.__half_size).tuple)

    @property
    def sprite(self) -> pygame.Surface:
        return self.__sprite

    @sprite.setter
    def sprite(self, new_sprite: pygame.Surface):
        self.__sprite = new_sprite
        self.__half_size = core.math.Vector2(self.__sprite.get_width()/2, self.__sprite.get_height()/2)
