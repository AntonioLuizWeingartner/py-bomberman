from __future__ import annotations
import pygame
import core.entity_system
import core.event_system
import core.core_components
from typing import List
from core.math import Vector2


class GridCell:
    
    def __init__(self, img: pygame.Surface, grid_position: Vector2, event_system: core.event_system.EventSystem) -> None:
        self.__walkable: bool = True
        self.__cell_image: pygame.Suface = img
        self.__event_system: core.event_system.EventSystem = event_system
        self.__grid_position = grid_position

    @property
    def walkable(self) -> bool:
        return self.__walkable
    
    @walkable.setter
    def walkable(self, val: bool):
        self.__walkable = val

    @property
    def image(self) -> pygame.Surface:
        return self.__cell_image

    @image.setter
    def image(self, img: pygame.Surface):
        self.__cell_image = img
        self.__event_system.broadcast("cell_img_changed", self, self.__grid_position)

class GameGrid(core.entity_system.ScriptableComponent):

    def on_init(self):
        self.__sprite_renderer: core.core_components.SpriteRenderer = self.owner.get_component(core.core_components.SpriteRenderer)

    def update(self):
        pass

    def generate_grid(self, grid_size: Vector2, cell_size: Vector2):
        self.__grid_size = grid_size
        self.__cell_size = cell_size
        self.__grid_cells: List[List[GridCell]] = list()
        self.__grid_image: pygame.Surface = pygame.Surface((grid_size.x*cell_size.x, grid_size.y * cell_size.y))

        for x in range(self.__grid_size.x):
            column: List[GridCell] = list()
            for y in range(self.__grid_size.y):
                cell = GridCell(self.app.image_loader.get_image("wall"), Vector2(x,y), self.event_system)
                self.event_system.listen("cell_img_changed", self.update_grid_img, sender=cell)
                column.append(cell)

            self.__grid_cells.append(column)

        self.generate_grid_image()
        self.centralize_grid_in_screen()
        self.__grid_cells[0][0].image = self.app.image_loader.get_image("dirt")

    def generate_grid_image(self):
        for x in range(self.__grid_size.x):
            for y in range(self.__grid_size.y):
                img = pygame.transform.scale(self.__grid_cells[x][y].image, self.__cell_size.tuple)
                self.__grid_image.blit(img, (x*self.__cell_size.x, y*self.__cell_size.y))
        self.__sprite_renderer.sprite = self.__grid_image

    def centralize_grid_in_screen(self):
        self.transform.position = Vector2(self.app.display.get_width()/2, self.app.display.get_height()/2)

    def update_grid_img(self, cell_position: Vector2):
        x = cell_position.x
        y = cell_position.y
        img = pygame.transform.scale(self.__grid_cells[x][y].image, self.__cell_size.tuple)
        self.__grid_image.blit(img, (x*self.__cell_size.x, y*self.__cell_size.y))

    @property
    def grid_size(self) -> Vector2:
        return self.__grid_size

    @property
    def cell_size(self) -> Vector2:
        return self.__cell_size

class GridAgent(core.entity_system.ScriptableComponent):
    
    def update(self):
        pass

class AIController(core.entity_system.ScriptableComponent):
    
    def update(self):
        pass

class PlayerController(core.entity_system.ScriptableComponent):

    def update(self):
        pass

class GameManager(core.entity_system.ScriptableComponent):

    def update(self):
        pass