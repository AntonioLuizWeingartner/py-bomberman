from __future__ import annotations
import enum
from os import closerange, system
from sys import path
import sys
import time
from types import MethodType
from pygame import sprite
from core.app import Keyboard
import pygame
import core.entity_system
import core.event_system
import core.core_components
import core.app
import functools
from typing import Dict, List, Optional, MutableSet
from core.math import Vector2

class GridCell:
    
    def __init__(self, img: pygame.Surface, grid_position: Vector2, event_system: core.event_system.EventSystem, walkable: bool = True, destructible: bool = False) -> None:
        self.__walkable: bool = walkable
        self.__destructible: bool = destructible
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
    def destructible(self) -> bool:
        return self.__destructible
    
    @destructible.setter
    def destructible(self, val: bool):
        self.__destructible = val

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
        self.__grid_bombs: List[List[Optional[Bomb]]] = list()
        self.__grid_explosions: List[List[bool]] = list()

        for x in range(self.__grid_size.x):
            column: List[GridCell] = list()
            bomb_column: List[Optional[Bomb]] = list()
            explosion_column: List[bool] = list()
            for y in range(self.__grid_size.y):
                if (x+1) % 2 == 0 and (y+1) % 2 == 0:
                    cell = GridCell(self.app.image_loader.get_image("ob"), Vector2(x,y), self.event_system, False, False)
                else:
                    cell = GridCell(self.app.image_loader.get_image("wall"), Vector2(x,y), self.event_system, False, True)   

                self.event_system.listen("cell_img_changed", self.update_grid_img, sender=cell)
                column.append(cell)
                bomb_column.append(None)
                explosion_column.append(False)

            self.__grid_cells.append(column)
            self.__grid_bombs.append(bomb_column)
            self.__grid_explosions.append(explosion_column)
        self.__grid_cells[0][0].image = self.app.image_loader.get_image("dirt")
        self.__grid_cells[0][1].image = self.app.image_loader.get_image("dirt")
        self.__grid_cells[1][0].image = self.app.image_loader.get_image("dirt")
        self.__grid_cells[0][0].walkable = True
        self.__grid_cells[0][1].walkable = True
        self.__grid_cells[1][0].walkable = True
        self.__grid_cells[0][0].destructible = False
        self.__grid_cells[0][1].destructible = False
        self.__grid_cells[1][0].destructible = False

        self.__grid_cells[self.__grid_size.x-1][self.__grid_size.y-1].image = self.app.image_loader.get_image("dirt")
        self.__grid_cells[self.__grid_size.x-2][self.__grid_size.y-1].image = self.app.image_loader.get_image("dirt")
        self.__grid_cells[self.__grid_size.x-1][self.__grid_size.y-2].image = self.app.image_loader.get_image("dirt")
        self.__grid_cells[self.__grid_size.x-1][self.__grid_size.y-1].walkable = True
        self.__grid_cells[self.__grid_size.x-2][self.__grid_size.y-1].walkable = True
        self.__grid_cells[self.__grid_size.x-1][self.__grid_size.y-2].walkable = True

        self.__grid_cells[self.__grid_size.x-1][self.__grid_size.y-1].destructible = False
        self.__grid_cells[self.__grid_size.x-2][self.__grid_size.y-1].destructible = False
        self.__grid_cells[self.__grid_size.x-1][self.__grid_size.y-2].destructible = False

        self.__grid_cells[self.__grid_size.x-1][0].image = self.app.image_loader.get_image("dirt")
        self.__grid_cells[self.__grid_size.x-2][0].image = self.app.image_loader.get_image("dirt")
        self.__grid_cells[self.__grid_size.x-1][1].image = self.app.image_loader.get_image("dirt")
        self.__grid_cells[self.__grid_size.x-1][0].walkable = True
        self.__grid_cells[self.__grid_size.x-2][0].walkable = True
        self.__grid_cells[self.__grid_size.x-1][1].walkable = True

        self.__grid_cells[self.__grid_size.x-1][0].destructible = False
        self.__grid_cells[self.__grid_size.x-2][0].destructible = False
        self.__grid_cells[self.__grid_size.x-1][1].destructible = False

        self.generate_grid_image()
        self.centralize_grid_in_screen()

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

    @property
    def bombs(self) -> List[List[Optional[Bomb]]]:
        return self.__grid_bombs

    @property
    def explosions(self) -> List[List[bool]]:
        return self.__grid_explosions


class GridEntity(core.entity_system.ScriptableComponent):
    pass

    def on_init(self):
        self._sprite_renderer: core.core_components.SpriteRenderer = self.owner.get_component(core.core_components.SpriteRenderer)

    def set_grid(self, grid: GameGrid, initial_pos: Vector2):
        self._grid: GameGrid = grid
        self._grid_pos: Vector2 = initial_pos
        self._grid_size: Vector2 = grid.grid_size
        self._cell_size: Vector2 = grid.cell_size
        self.place_entity()

    def place_entity(self):
        world_pos = self.compute_world_position(self._grid_pos)
        self.transform.position = world_pos

    def compute_world_position(self, grid_position: Vector2) -> Vector2:
        offset = self._grid.transform.position - (self._grid.dimensions/2)
        world_position = Vector2(0,0)
        world_position.x = grid_position.x*self._cell_size.x
        world_position.y = grid_position.y*self._cell_size.y
        world_position += offset
        world_position += self._cell_size/2
        return world_position

class Direction(enum.Enum):
    SOUTH = 0
    NORTH = 1
    WEST = 2
    EAST = 3
    CENTER = 4

class BounceCounter:

    def __init__(self, max_value: int, initial_value: int):
        self.__counter = initial_value
        self.__max = max_value
        self.__min = initial_value
        self.__direction = True
        self.__first_iteration = True

    def update(self) -> int:
        if self.__first_iteration:
            self.__first_iteration = False
            return self.__min

        if self.__direction:
            self.__counter += 1
            if self.__counter == self.__max:
                self.__direction = False
        else:
            self.__counter -= 1
            if self.__counter == self.__min:
                self.__direction = True
        return self.__counter

class Explosion(core.entity_system.ScriptableComponent):

    def on_init(self):
        self.__remove_time_point = time.perf_counter() + 3
        self.__last_frame = 0
        self.__frame_duration = 0.12
        self.__counter = BounceCounter(3,0)
        self.__max_frame_count = 8
        self.__frame_count = 0

    def set_data(self, spr: core.core_components.SpriteRenderer, sprites: List[pygame.Surface], grid: GameGrid, pos: Vector2):
        self.__sprites = sprites
        self.__spr = spr
        self.__grid = grid
        self.__pos = pos

    def update(self):
        if (time.perf_counter() - self.__last_frame) >= self.__frame_duration:
            self.__last_frame = time.perf_counter()
            self.__spr.sprite = self.__sprites[self.__counter.update()]
            self.__frame_count += 1

        if self.__frame_count > self.__max_frame_count:
            self.world.mark_entity_for_deletion(self.owner)
            self.__grid.explosions[self.__pos.x][self.__pos.y] = False
            
class Bomb(GridEntity):

    def on_init(self):
        super().on_init()
        self.__fuse_time = self.app.clock.now() + 3
        self.__frame_duration = 0.1

    def set_grid(self, grid: GameGrid, initial_pos: Vector2):
        super().set_grid(grid, initial_pos)
        self._grid.cells[initial_pos.x][initial_pos.y].walkable = False
        self._grid.bombs[initial_pos.x][initial_pos.y] = self

    def set_owner(self, agent: GridAgent):
        self.__owner = agent

    def create_explosion(self, direction: Direction, pos: Vector2, end: bool = False):
        #TODO MAKE EXPLOSIONS INTERACT WITH THE GRID
        sprites: pygame.Surface = None

        self._grid.explosions[pos.x][pos.y] = True
        

        if end:
            if direction == direction.NORTH:
                sprites = self.app.image_loader.get_sheet("explosions")[3]
            elif direction == direction.SOUTH:
                sprites = self.app.image_loader.get_sheet("explosions")[4]
            elif direction == direction.EAST:
                sprites = self.app.image_loader.get_sheet("explosions")[5]
            elif direction == direction.WEST:
                sprites = self.app.image_loader.get_sheet("explosions")[6]
        else:
            if direction == Direction.CENTER:
                sprites = self.app.image_loader.get_sheet("explosions")[0]
            elif direction == Direction.EAST or direction == Direction.WEST:
                sprites = self.app.image_loader.get_sheet("explosions")[2]
            elif direction == Direction.NORTH or direction == Direction.SOUTH:
                sprites = self.app.image_loader.get_sheet("explosions")[1]

        exp_entity = self.world.add_entity()
        spr = exp_entity.add_component(core.core_components.SpriteRenderer)
        exp_entity.transform.position = self.compute_world_position(pos)
        exp_cp = exp_entity.add_component(Explosion)
        exp_cp.set_data(spr, sprites, self._grid, pos)

    def on_explode(self, incoming_direction: Optional[Direction] = None):
        self.event_system.broadcast("bomb_exploded", sender=self.__owner)
        self._grid.cells[self._grid_pos.x][self._grid_pos.y].walkable = True
        self._grid.bombs[self._grid_pos.x][self._grid_pos.y] = None
        self.world.mark_entity_for_deletion(self.owner)
        firepower = self.__owner.firepower


        expand_east: bool = True if incoming_direction != Direction.EAST else False
        expand_west: bool = True if incoming_direction != Direction.WEST else False
        expand_north: bool = True if incoming_direction != Direction.NORTH else False
        expand_south: bool = True if incoming_direction != Direction.SOUTH else False

        if incoming_direction is None:
            self.app.sound_loader.play_sound("explosion")

      
        self.create_explosion(Direction.CENTER, self._grid_pos)

        for val in range(1,firepower+1):
            final_iteration = val == firepower
            if expand_west:
                target_x = self._grid_pos.x - val
                if target_x >= 0:
                    target_cell: GridCell = self._grid.cells[target_x][self._grid_pos.y]
                    target_bomb: Bomb = self._grid.bombs[target_x][self._grid_pos.y]
                    if target_cell.destructible:
                        target_cell.destructible = False
                        target_cell.walkable = True
                        target_cell.image = self.app.image_loader.get_image("dirt")
                        self.create_explosion(Direction.WEST, Vector2(target_x, self._grid_pos.y), end=True)
                        expand_west = False
                    elif target_bomb is not None:
                        target_bomb.on_explode(Direction.EAST)
                        expand_west = False
                    elif target_cell.walkable:
                        self.create_explosion(Direction.WEST, Vector2(target_x, self._grid_pos.y), end=(target_x == 0 or final_iteration))
                    else:
                        expand_west = False

            if expand_east:
                target_x = self._grid_pos.x + val
                if target_x < self._grid_size.x:
                    target_cell: GridCell = self._grid.cells[target_x][self._grid_pos.y]
                    target_bomb: Bomb = self._grid.bombs[target_x][self._grid_pos.y]
                    if target_cell.destructible:
                        target_cell.destructible = False
                        target_cell.walkable = True
                        target_cell.image = self.app.image_loader.get_image("dirt")
                        self.create_explosion(Direction.EAST, Vector2(target_x, self._grid_pos.y), end=True)
                        expand_east = False
                    elif target_bomb is not None:
                        target_bomb.on_explode(Direction.WEST)
                        expand_east = False
                    elif target_cell.walkable:
                        self.create_explosion(Direction.EAST, Vector2(target_x, self._grid_pos.y), end=(target_x == self._grid_size.x-1 or final_iteration))
                    else:
                        expand_east = False

            if expand_north:
                target_y = self._grid_pos.y - val
                if target_y >= 0:
                    target_cell: GridCell = self._grid.cells[self._grid_pos.x][target_y]
                    target_bomb: Bomb = self._grid.bombs[self._grid_pos.x][target_y]
                    if target_cell.destructible:
                        target_cell.destructible = False
                        target_cell.walkable = True
                        target_cell.image = self.app.image_loader.get_image("dirt")
                        self.create_explosion(Direction.NORTH, Vector2(self._grid_pos.x, target_y), end=True)
                        expand_north = False
                    elif target_bomb is not None:
                        target_bomb.on_explode(Direction.SOUTH)
                        expand_north = False
                    elif target_cell.walkable:
                        self.create_explosion(Direction.NORTH, Vector2(self._grid_pos.x, target_y), end=(target_y == 0 or final_iteration))
                    else:
                        expand_north = False

            if expand_south:
                target_y = self._grid_pos.y + val
                if target_y < self._grid_size.y:
                    target_cell: GridCell = self._grid.cells[self._grid_pos.x][target_y]
                    target_bomb: Bomb = self._grid.bombs[self._grid_pos.x][target_y]
                    if target_cell.destructible:
                        target_cell.destructible = False
                        target_cell.walkable = True
                        target_cell.image = self.app.image_loader.get_image("dirt")
                        self.create_explosion(Direction.SOUTH, Vector2(self._grid_pos.x, target_y), end=True)
                        expand_south = False
                    elif target_bomb is not None:
                        target_bomb.on_explode(Direction.NORTH)
                        expand_south = False
                    elif target_cell.walkable:
                        self.create_explosion(Direction.SOUTH, Vector2(self._grid_pos.x, target_y), end=(target_y == self._grid_size.y - 1 or final_iteration))
                    else:
                        expand_south = False

            if not expand_east and not expand_west and not expand_south and not expand_north:
                break

    @property
    def firepower(self) -> int:
        return self.__owner.firepower      
    
    @property
    def position(self) -> Vector2:
        return self._grid_pos

    def update(self):
        if self.app.clock.now() >= self.__fuse_time:
            self.on_explode()

class GridAgent(GridEntity):

    #TODO MAKE GRIDAGENTS DIE WHEN IN CONTACT WITH EXPLOSIONS
    #TODO ADD CHARACTER ANIMATIONS TO GRID AGENTS

    def on_init(self):
        self._sprite_renderer: core.core_components.SpriteRenderer = self.owner.get_component(core.core_components.SpriteRenderer)
        self._movement_disabled: bool = False
        self._target_position: Vector2 = Vector2(0,0)
        self._mov_delta: Vector2 = Vector2(0,0)
        self._fire_power = 5
        self._max_bombs = 3
        self._bomb_count = 0
        self._mov_delta_factor = 10
        self._movement_duration = (1/60)*self._mov_delta_factor
        self._frame_duration = self._movement_duration/7
        self._play_anim = False
        self._current_anim_frame: int = 0
        self._last_frame_tp: float = 0
        self._direction: Direction = Direction.SOUTH
        self._anim_type: int = 0
        self.event_system.listen("bomb_exploded", self.return_bomb, sender=self)

    def return_bomb(self):
        self._bomb_count -= 1

    def set_grid(self, grid: GameGrid, initial_pos: Vector2):
        super().set_grid(grid, initial_pos)
        self._sprite_renderer.sprite = self.app.image_loader.get_sheet("player")[0][2]

    def place_entity(self):
        world_pos = self.compute_world_position(self._grid_pos)
        self._target_position = world_pos
        self.transform.position = world_pos

    def move(self, direction: Vector2):
        if self._movement_disabled:
            return None
        target_grid_pos = self._grid_pos + direction

        if target_grid_pos.x > self._grid_size.x - 1 or target_grid_pos.x < 0 or target_grid_pos.y > self._grid_size.y - 1 or target_grid_pos.y < 0:
            return False
        
        if self._grid.cells[target_grid_pos.x][target_grid_pos.y].walkable is False:
            return False
        
        if direction.y == 1:
            self._direction = Direction.SOUTH
            self._anim_type = 2
        elif direction.y == -1:
            self._direction = Direction.NORTH
            self._anim_type = 0
        elif direction.x == 1:
            self._direction = Direction.EAST
            self._anim_type = 1
        elif direction.x == -1:
            self._direction = Direction.WEST
            self._anim_type = 3

        self._play_anim = True
        self._grid_pos = target_grid_pos
        self._target_position = self.compute_world_position(self._grid_pos)
        self._mov_delta = (self._target_position - self.transform.position)/self._mov_delta_factor
        self._movement_disabled = True
        return True

    def place_bomb(self):
        if self._grid.bombs[self._grid_pos.x][self._grid_pos.y] is None and self._bomb_count < self._max_bombs:
            self.app.sound_loader.play_sound("bomb_place")
            self._bomb_count += 1
            bomb_entity = self.world.add_entity()
            bomb_entity.add_component(core.core_components.SpriteRenderer).sprite = self.app.image_loader.get_image("bomb")
            bomb_cp: Bomb = bomb_entity.add_component(Bomb)
            bomb_cp.set_grid(self._grid, self._grid_pos)
            bomb_cp.set_owner(self)

    def __set_end_sprite(self):
        spr: pygame.Surface = None
        if self._direction == Direction.NORTH:
            spr = self.app.image_loader.get_sheet("player")[0][0]
        elif self._direction == Direction.SOUTH:
            spr = self.app.image_loader.get_sheet("player")[0][2]
        elif self._direction == Direction.EAST:
            spr = self.app.image_loader.get_sheet("player")[0][1]
        elif self._direction == Direction.WEST:
            spr = self.app.image_loader.get_sheet("player")[0][3]
        self._sprite_renderer.sprite = spr

    def on_death(self):
        pass


    def update(self):
        self.transform.position += self._mov_delta
        if(self._play_anim):
            if(time.perf_counter() - self._last_frame_tp >= self._frame_duration):
                self._last_frame_tp = time.perf_counter()
                self._sprite_renderer.sprite = self.app.image_loader.get_sheet("player")[self._current_anim_frame][self._anim_type]
                self._current_anim_frame += 1

        if (self.transform.position - self._target_position).squared_mag <= 0.15:
            self._play_anim = False
            self._current_anim_frame = 0
            self.transform.position = self._target_position
            self._movement_disabled = False
            self._mov_delta = Vector2(0,0)
            self.__set_end_sprite()

        if(self._grid.explosions[self._grid_pos.x][self._grid_pos.y]):
            self.world.mark_entity_for_deletion(self.owner)
            self.on_death()

    @property
    def firepower(self) -> int:
        return self._fire_power

class AIAgent(GridAgent):

    class ASNode:

        def __init__(self, pos: Vector2, parent: AIAgent.ASNode, dist_f_start: int, dist_f_end: int):
            self.position = pos
            self.parent = parent
            self.g_cost = dist_f_start
            self.h_cost = dist_f_end

        @property
        def f_cost(self) -> int:
            return self.g_cost + self.h_cost

    class AIStates:
        SEEKCOVER = 0
        ATTACK = 1
        DESTROY = 2
        IDLE = 3

    def on_init(self):
        super().on_init()
        self.__state: AIAgent.AIStates = AIAgent.AIStates.IDLE
        self.__wait_frames: int = 0
        self.__crr_wait: int = 0
        self.__seek_cover_frames: int = 0
        self.__crr_seek_cover: int = 0
        self._max_bombs = 1

    def set_player(self, player: Player):
        self.__player = player

    def find_path(self, end_pos: Vector2, ignore_walkability: bool = False):
        open_nodes: Dict[Vector2, AIAgent.ASNode] = dict()
        closed_nodes: Dict[Vector2, AIAgent.ASNode] = dict()
        open_nodes[self._grid_pos] = AIAgent.ASNode(self._grid_pos, None, 0, 0)
        danger_grid: List[List[bool]] = self.__expand_bombs()
        if end_pos == self._grid_pos:
            return

        def find_lowest_f_cost_node(nodes: Dict[Vector2, AIAgent.ASNode]) -> AIAgent.ASNode:
            lowest_f_cost_node: AIAgent.ASNode = AIAgent.ASNode(Vector2(0,0), None, 5000,5000)
            for node in nodes.values():
                if node.f_cost < lowest_f_cost_node.f_cost:
                    lowest_f_cost_node = node
            return lowest_f_cost_node

        while open_nodes:
            q: AIAgent.ASNode = find_lowest_f_cost_node(open_nodes)
            del open_nodes[q.position]
            successsors: List[AIAgent.ASNode] = list()

            temp_pos = q.position + Vector2(0,1)

            if temp_pos.y < self._grid_size.y and (self._grid.cells[temp_pos.x][temp_pos.y].walkable or (ignore_walkability and self._grid.cells[temp_pos.x][temp_pos.y].destructible)) and self._grid.explosions[temp_pos.x][temp_pos.y] is False and danger_grid[temp_pos.x][temp_pos.y] is False:
                successsors.append(AIAgent.ASNode(temp_pos, q, q.g_cost+1, temp_pos.mahattan_distance(end_pos)))

            temp_pos = q.position + Vector2(0,-1)
            if temp_pos.y >= 0 and (self._grid.cells[temp_pos.x][temp_pos.y].walkable or (ignore_walkability and self._grid.cells[temp_pos.x][temp_pos.y].destructible)) and self._grid.explosions[temp_pos.x][temp_pos.y] is False and danger_grid[temp_pos.x][temp_pos.y] is False:
                successsors.append(AIAgent.ASNode(temp_pos, q, q.g_cost+1, temp_pos.mahattan_distance(end_pos)))

            temp_pos = q.position + Vector2(1,0)
            if temp_pos.x < self._grid_size.x and (self._grid.cells[temp_pos.x][temp_pos.y].walkable or (ignore_walkability and self._grid.cells[temp_pos.x][temp_pos.y].destructible)) and self._grid.explosions[temp_pos.x][temp_pos.y] is False and danger_grid[temp_pos.x][temp_pos.y] is False:
                successsors.append(AIAgent.ASNode(temp_pos, q, q.g_cost+1, temp_pos.mahattan_distance(end_pos)))
            
            temp_pos = q.position + Vector2(-1,0)
            if temp_pos.x >= 0 and (self._grid.cells[temp_pos.x][temp_pos.y].walkable or (ignore_walkability and self._grid.cells[temp_pos.x][temp_pos.y].destructible)) and self._grid.explosions[temp_pos.x][temp_pos.y] is False and danger_grid[temp_pos.x][temp_pos.y] is False:
                successsors.append(AIAgent.ASNode(temp_pos, q, q.g_cost+1, temp_pos.mahattan_distance(end_pos)))

            for succ in successsors:
                if succ.position == end_pos:
                    return succ

                if succ.position in open_nodes:
                    if open_nodes[succ.position].f_cost < succ.f_cost:
                        continue
                elif succ.position in closed_nodes:
                    if closed_nodes[succ.position].f_cost < succ.f_cost:
                        continue
                else:
                    open_nodes[succ.position] = succ
            
            closed_nodes[q.position] = q

    def __build_path(self, node: AIAgent.ASNode) -> List[AIAgent.ASNode]:
        if node is None:
            return None

        path = list()
        n = node
        while n.parent is not None:
            path.insert(0, n)
            n = n.parent
        if path:
            return path
        else:
            path.append(n)
            return path



    def __expand_bombs(self) -> List[List[bool]]:
        #TODO RETURN A GRID WITH EVERY BOMB EXPLODED
        danger_grid: List[List[bool]] = list()
        bombs: List[Bomb] = list()
        for x in range(self._grid_size.x):
            danger_grid_column: List[bool] = list()
            for y in range(self._grid_size.y):
                if self._grid.bombs[x][y] is not None:
                    bombs.append(self._grid.bombs[x][y])
                    danger_grid_column.append(True)
                else:
                    danger_grid_column.append(False)
            danger_grid.append(danger_grid_column)

        for bomb in bombs:
            expand_west: bool = True
            expand_east: bool = True
            expand_north: bool = True
            expand_south: bool = True
            for i in range(1, bomb.firepower):
                
                if not(expand_west or expand_west or expand_north or expand_south):
                    break

                if expand_west:
                    target_x = bomb.position.x - i
                    if target_x < 0:
                        expand_west = False
                    else:
                        danger_grid[target_x][bomb.position.y] = True
                
                if expand_east:
                    target_x = bomb.position.x + i
                    if target_x >= self._grid_size.x:
                        expand_east = False
                    else:
                        danger_grid[target_x][bomb.position.y] = True

                if expand_north:
                    target_y = bomb.position.y - i
                    if target_y < 0:
                        expand_north = False
                    else:
                        danger_grid[bomb.position.x][target_y] = True
                
                if expand_south:
                    target_y = bomb.position.y + i
                    if target_y >= self._grid_size.y:
                        expand_south = False
                    else:
                        danger_grid[bomb.position.x][target_y] = True

        return_grid: List[List[bool]] = list()
        for i in range(self._grid_size.x):
            list_column = [a or b for a,b in zip(danger_grid[i], self._grid.explosions[i])]
            return_grid.append(list_column)
        return return_grid

    def __find_path_to_safety(self) -> AIAgent.ASNode:
        open_nodes: List[AIAgent.ASNode] = list()
        closed_nodes: Dict[Vector2, AIAgent.ASNode] = dict()
        open_nodes.append(AIAgent.ASNode(self._grid_pos, None, 0, 0))
        danger_grid = self.__expand_bombs()

        if danger_grid[self._grid_pos.x][self._grid_pos.y] is False:
            return open_nodes[0]
        while open_nodes:
            q = open_nodes.pop(0)
            closed_nodes[q.position] = q
            successors: List[AIAgent.ASNode] = list()
            
            temp_pos = q.position + Vector2(0, 1)
            if temp_pos.y < self._grid_size.y and self._grid.cells[temp_pos.x][temp_pos.y].walkable and temp_pos not in closed_nodes:
                successors.append(AIAgent.ASNode(temp_pos, q, 0, 0))

            temp_pos = q.position + Vector2(0, -1)
            if temp_pos.y >= 0 and self._grid.cells[temp_pos.x][temp_pos.y].walkable and temp_pos not in closed_nodes:
                successors.append(AIAgent.ASNode(temp_pos, q, 0, 0))
            
            temp_pos = q.position + Vector2(1, 0)
            if temp_pos.x < self._grid_size.y and self._grid.cells[temp_pos.x][temp_pos.y].walkable and temp_pos not in closed_nodes:
                successors.append(AIAgent.ASNode(temp_pos, q, 0, 0))

            temp_pos = q.position + Vector2(-1, 0)
            if temp_pos.x >= 0 and self._grid.cells[temp_pos.x][temp_pos.y].walkable and temp_pos not in closed_nodes:
                successors.append(AIAgent.ASNode(temp_pos, q, 0, 0))

            open_nodes.extend(successors)

            for succ in successors:
                if danger_grid[succ.position.x][succ.position.y] is False:
                    return succ

    def __AI_update(self):
        if self.__state == AIAgent.AIStates.IDLE:
            if self.__crr_wait < self.__wait_frames:
                self.__crr_wait += 1
            else:
                self.__crr_wait = 0
                path_to_player = self.find_path(self.__player._grid_pos)
                if path_to_player is not None:
                    self.__state = AIAgent.AIStates.ATTACK
                else:
                    self.__state = AIAgent.AIStates.DESTROY

        elif self.__state == AIAgent.AIStates.SEEKCOVER:
            #TODO path find to safety, use flood fill maybe
            #TODO go towards that path until your bomb explodes
            if self._bomb_count == 0 and self.__crr_seek_cover >= self.__seek_cover_frames:
                self.__crr_seek_cover = 0
                print("SEEK COVER COMPLETED, GOING IDLE FOR 30 FRAMES")
                self.__wait(1)
            else:
                self.__crr_seek_cover += 1
                path_to_safety = self.__build_path(self.__find_path_to_safety())
                if path_to_safety is not None:
                    move_dir = path_to_safety[0].position - self._grid_pos
                    self.move(move_dir)

                else:
                    print("WILL DIE")

            pass
        elif self.__state == AIAgent.AIStates.DESTROY:
            #TODO path find to player, ignoring walkability
            path_to_player = self.find_path(self.__player._grid_pos, True)
            true_path_to_player = self.find_path(self.__player._grid_pos)
            if true_path_to_player is not None:
                self.__wait(30)

            if path_to_player is not None:
                #TODO move towards path
                path = self.__build_path(path_to_player)
                move_dir = path[0].position - self._grid_pos

                if self.move(move_dir) is False:
                    #TODO If a destructible block is in the next position, place a bomb and then change state to seek cover
                    self.place_bomb()
                    self.__seekcover(250)
            else:
                pass

        elif self.__state == AIAgent.AIStates.ATTACK:
            #TODO pathfind to player, considering walkability
            #TODO move towards path until you can place a bomb to kill him
            #TODO if you can kill him, place down a bomb and seek covers
            #TODO If path suddenly gets blocked, change behaviour to seek cover
            y_aligned: bool = True if self._grid_pos.y == self.__player._grid_pos.y else False
            x_aligned: bool = True if self._grid_pos.x == self.__player._grid_pos.x else False

            if y_aligned:
                distance = self._grid_pos.x - self.__player._grid_pos.x
                direction: int = -1 if distance > 0 else 1
                if distance <= self.firepower:
                    #TODO test if there is a clear path between player and bot
                    clear_path: bool = True
                    for i in range(distance):
                        if self._grid.cells[self._grid_pos.x +i*direction][self._grid_pos.y].walkable is False:
                            clear_path = False
                            break

                    if clear_path:
                        self.place_bomb()
                        self.__seekcover(250)
            elif x_aligned:
                distance = self._grid_pos.y - self.__player._grid_pos.y
                direction: int = -1 if distance > 0 else 1
                if distance <= self.firepower:
                    #TODO test if there is a clear path between player and bot
                    clear_path: bool = True
                    for i in range(distance):
                        if self._grid.cells[self._grid_pos.x][self._grid_pos.y +i*direction].walkable is False:
                            clear_path = False
                            break

                    if clear_path:
                        self.place_bomb()
                        self.__seekcover(250)
            else:
                #TODO go towards player
                path = self.__build_path(self.find_path(self.__player._grid_pos))

                if path is not None:
                    move_dir = path[0].position - self._grid_pos
                    self.move(move_dir)

            print("ATTACKING")
            pass

    def __seekcover(self, frames: int):
        self.__state = AIAgent.AIStates.SEEKCOVER
        self.__seek_cover_frames = frames

    def __wait(self, frames: int):
        self.__state = AIAgent.AIStates.IDLE
        self.__wait_frames = frames
    
    def update(self):
        super().update()
        self.__AI_update()

class Player(GridAgent):

    def on_init(self):
        super().on_init()
        self.keyboard.register_callback(pygame.K_DOWN, Keyboard.KEY_PRESSED, functools.partial(self.move, Vector2(0, 1)))
        self.keyboard.register_callback(pygame.K_UP, Keyboard.KEY_PRESSED, functools.partial(self.move, Vector2(0, -1)))
        self.keyboard.register_callback(pygame.K_LEFT, Keyboard.KEY_PRESSED, functools.partial(self.move, Vector2(-1, 0)))
        self.keyboard.register_callback(pygame.K_RIGHT, Keyboard.KEY_PRESSED, functools.partial(self.move, Vector2(1, 0)))
        self.keyboard.register_callback(pygame.K_SPACE, Keyboard.KEY_PRESSED, functools.partial(self.place_bomb))

    def on_death(self):
        self.app.sound_loader.play_sound("player_death")

class GameManager(core.entity_system.ScriptableComponent):

    def update(self):
        pass