import core.entity_system
import core.math

class SpriteRenderer(core.entity_system.DrawableComponent):

    def on_init(self):
        self.__sprite = self.app.image_loader.get_image("default")
        self.__display = self.app.display
        self.__half_size = core.math.Vector2(self.__sprite.get_width()/2, self.__sprite.get_height()/2)

    def draw(self):
        self.__display.blit(self.__sprite, (self.transform.position - self.__half_size).tuple)