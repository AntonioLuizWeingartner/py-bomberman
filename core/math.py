from __future__ import annotations
from typing import Tuple

class Vector2:

    """
    Esta classe representa vetores de duas dimensões.
    """

    def __init__(self, x: float, y: float):
        self.x = x;
        self.y = y

    def __add__(self, other: Vector2):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __iadd__(self, other: Vector2):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other: Vector2):
        return Vector2(self.x - other.x, self.y - other.y)

    def __isub__(self, other: Vector2):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other: float):
        return Vector2(self.x*other, self.y*other)

    def __imul__(self, other: float):
        self.x *= other
        self.y *= other
        return self

    def __truediv__(self, other: float):
        return Vector2(self.x/other, self.y/other)

    def __hash__(self):
        return hash(self.tuple)

    def __eq__(self, other: Vector2) -> bool:
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def mahattan_distance(self, other: Vector2) -> float:
        return abs(self.x-other.x) + abs(self.y+other.y)

    @property
    def squared_mag(self):
        return self.x**2 + self.y**2

    def __repr__(self) -> str:
        return "Vector2 (x={}, y={})".format(self.x, self.y)
    
    @property
    def tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)