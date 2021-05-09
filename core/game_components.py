from __future__ import annotations
from ast import walk
from core.app import Keyboard
import pygame
import core.entity_system
import core.event_system
import core.core_components
import core.app
import functools
from typing import List
from core.math import Vector2

class GridCell:
    
    def __init__(self, img: pygame.Surface, grid_position: Vector2, event_system: core.event_system.EventSystem, walkable: bool = True) -> None:
        self.__walkable: bool = walkable
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
                if (x+1) % 2 == 0 and (y+1) % 2 == 0:
                    cell = GridCell(self.app.image_loader.get_image("wall"), Vector2(x,y), self.event_system, False)
                else:
                    cell = GridCell(self.app.image_loader.get_image("dirt"), Vector2(x,y), self.event_system)   

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

    @property
    def dimensions(self) -> Vector2:
        return Vector2(self.__grid_size.x*self.__cell_size.x, self.__grid_size.y*self.__cell_size.y)

    @property
    def cells(self) -> List[List[GridCell]]:
        return self.__grid_cells

class GridAgent(core.entity_system.ScriptableComponent):

    def on_init(self):
        self.__sprite_renderer: core.core_components.SpriteRenderer = self.owner.get_component(core.core_components.SpriteRenderer)
        self.__movement_disabled: bool = False
        self.__target_position: Vector2 = Vector2(0,0)
        self.__mov_delta: Vector2 = Vector2(0,0)


    def set_grid(self, grid: GameGrid, initial_pos: Vector2):
        self.__grid: GameGrid = grid
        self.__grid_pos: Vector2 = initial_pos
        self.__grid_size: Vector2 = grid.grid_size
        self.__cell_size: Vector2 = grid.cell_size
        self.__agent_img: pygame.Surface = pygame.Surface(self.__cell_size.tuple)
        self.__agent_img.fill((255,255,255))
        self.__sprite_renderer.sprite = self.__agent_img
        self.place_agent()

    def place_agent(self):
        world_pos = self.compute_world_position(self.__grid_pos)
        self.__target_position = world_pos
        self.transform.position = world_pos

    def compute_world_position(self, grid_position: Vector2) -> Vector2:
        offset = self.__grid.transform.position - (self.__grid.dimensions/2)
        world_position = Vector2(0,0)
        world_position.x = grid_position.x*self.__cell_size.x
        world_position.y = grid_position.y*self.__cell_size.y
        world_position += offset
        world_position += self.__cell_size/2
        return world_position

    def move(self, direction: Vector2):
        if self.__movement_disabled:
            return
        target_grid_pos = self.__grid_pos + direction

        if target_grid_pos.x > self.__grid_size.x - 1 or target_grid_pos.x < 0 or target_grid_pos.y > self.__grid_size.y - 1 or self.__grid_size.y < 0:
            return
        
        if self.__grid.cells[target_grid_pos.x][target_grid_pos.y].walkable is False:
            return
        

        self.__grid_pos = target_grid_pos
        self.__target_position = self.compute_world_position(self.__grid_pos)
        self.__mov_delta = (self.__target_position - self.transform.position)/10
        self.__movement_disabled = True

    def update(self):
        self.transform.position += self.__mov_delta
        if (self.transform.position - self.__target_position).squared_mag <= 0.15:
            self.transform.position = self.__target_position
            self.__movement_disabled = False
            self.__mov_delta = Vector2(0,0)


class AIAgent(GridAgent):
    pass

class Player(GridAgent):

    def on_init(self):
        super().on_init()
        self.keyboard.register_callback(pygame.K_DOWN, Keyboard.KEY_PRESSED, functools.partial(self.move, Vector2(0, 1)))
        self.keyboard.register_callback(pygame.K_UP, Keyboard.KEY_PRESSED, functools.partial(self.move, Vector2(0, -1)))
        self.keyboard.register_callback(pygame.K_LEFT, Keyboard.KEY_PRESSED, functools.partial(self.move, Vector2(-1, 0)))
        self.keyboard.register_callback(pygame.K_RIGHT, Keyboard.KEY_PRESSED, functools.partial(self.move, Vector2(1, 0)))

class GameManager(core.entity_system.ScriptableComponent):

    def update(self):
        pass