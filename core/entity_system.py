from __future__ import annotations
import abc
import core.app
import core.event_system
import core.math
from typing import Optional, Type, List

class Component:
    
    def __init__(self, owner: Entity):
        self.__owner = owner
    
    def on_init(self):
        pass

    def on_remove(self):
        pass

    @property
    def event_system(self) -> core.event_system.EventSystem:
        return self.app.event_system

    @property
    def transform(self) -> Transform:
        return self.__owner.transform

    @property
    def owner(self) -> Entity:
        return self.__owner

    @property
    def world(self) -> World:
        return self.__owner.world

    @property
    def app(self) -> core.app.Application:
        return self.__owner.app

    @property
    def mouse(self) -> core.app.Mouse:
        return self.__owner.app.mouse

    @property
    def keyboard(self) -> core.app.Keyboard:
        return self.__owner.app.keyboard

class ScriptableComponent(Component, abc.ABC):

    @abc.abstractmethod
    def update(self):
        raise NotImplementedError()
    
class DrawableComponent(Component, abc.ABC):

    @abc.abstractmethod
    def draw(self):
        raise NotImplementedError()


class Transform(Component):
    
    def on_init(self):
        self.__position = core.math.Vector2(0, 0)
        self.__scale = core.math.Vector2(1, 1)

    @property
    def position(self) -> core.math.Vector2:
        return self.__position

    @position.setter
    def position(self, new_pos: core.math.Vector2):
        self.__position = new_pos


class InvalidComponentTypeError(Exception):
    pass

class ComponentNotFoundError(Exception):
    pass

class Entity:

    def __init__(self, world: World) -> None:
        self.__world = world
        self.__components: List[Component] = list()
        self.__scriptables: List[ScriptableComponent] = list()
        self.__drawables: List[DrawableComponent] = list()
        self.__transform = self.add_component(Transform)

    def __get_target_list(self, component_type: Type) -> List[Component]:
        target_list: List[Component] = None
        if issubclass(component_type, ScriptableComponent):
            target_list = self.__scriptables
        elif issubclass(component_type, DrawableComponent):
            target_list = self.__drawables
        elif issubclass(component_type, Component):
            target_list = self.__components
        else:
            raise InvalidComponentTypeError()
    
        return target_list

    def add_component(self, component_type: Type) -> Component:
        target_list = self.__get_target_list(component_type)
        cp = component_type(self)
        target_list.append(cp)
        cp.on_init()
        return cp

    def remove_component(self, component_instance: Component):
        target_list = self.__get_target_list(type(component_instance))
        if component_instance in target_list:
            target_list.remove(component_instance)
            component_instance.on_remove()
        else:
            raise ComponentNotFoundError()

    def get_component(self, component_type: Type) -> Component:
        target_list = self.__get_target_list(component_type)
        for component in target_list:
            if type(component) is component_type:
                return component
        raise ComponentNotFoundError()

    def update(self):
        for component in self.__scriptables:
            component.update()
    
    def draw(self):
        for component in self.__drawables:
            component.draw()

    @property
    def world(self) -> World:
        return self.__world

    @property
    def app(self) -> core.app.Application:
        return self.__world.app

    @property
    def transform(self) -> Transform:
        return self.__transform

class EntityNotFoundError(Exception):
    pass

class World:
    
    def __init__(self):
        self.__app: core.app.Application = None
        self.__entities: List[Entity] = list()

    def set_app(self, app: core.app.Application):
        self.__app = app

    def add_entity(self) -> Entity:
        ent = Entity(self)
        self.__entities.append(ent)
        return ent

    def remove_entity(self, entity_instance: Entity):
        if entity_instance in self.__entities:
            self.__entities.remove(entity_instance)
        else:
            raise EntityNotFoundError()
    
    def update(self):
        for entity in self.__entities:
            entity.update()
    
    def draw(self):
        for entity in self.__entities:
            entity.draw()
        
    @property
    def app(self) -> core.app.Application:
        return self.__app