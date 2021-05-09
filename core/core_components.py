import core.entity_system

class SpriteRenderer(core.entity_system.DrawableComponent):

    def on_init(self):
        self.__sprite = self.app.image_loader.get_image("default")
        self.__display = self.app.display

    def draw(self):
        self.__display.blit(self.__sprite, self.transform.position.tuple)