from dataclasses import dataclass
from typing import Self, Any
from math import sqrt


@dataclass(frozen=True, eq=True, order=True)
class Vec2:
    x: int
    y: int

    @property
    def r(self):
        return self.x

    @property
    def c(self):
        return self.y
    
    @r.setter
    def r(self, v):
        self.x = v
    
    @c.setter
    def c(self, v):
        self.y = v

    def __add__(self, other: Self):
        return Vec2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Self):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int):
        return Vec2(self.x * other, self.y * other)
    
    def __rmul__(self, other: int):
        return self.__mul__(other)
    
    def __truediv__(self, other: int | float):
        if not (isinstance(other, int) or isinstance(other, float)):
            return NotImplemented
        return Vec2(self.x / other, self.y / other)

    def __floordiv__(self, other: int | float):
        if not (isinstance(other, int) or isinstance(other, float)):
            return NotImplemented
        return Vec2(self.x // other, self.y // other)

    def dot(self, other: Self):
        if not isinstance(other, Vec2):
            return NotImplemented
        return self.x * other.x + self.y * other.y
    
    def cross(self, other: Self):
        if not isinstance(other, Vec2):
            return NotImplemented
        return self.x*other.y - self.y*other.x
    
    def distance(self, other: Self) -> float:
        if not isinstance(other, Vec2):
            return NotImplemented
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def manhattan_distance(self, other: Self):
        if not isinstance(other, Vec2):
            return NotImplemented
        return abs(self.x - other.x) + abs(self.y - other.y)

    def magnitude(self):
        return sqrt(self.dot(self))

    def normalized(self):
        return self / self.magnitude()

    def in_bounds(self, grid: list[list[Any]]):
        return self.r >= 0 and self.c >= 0 and self.r < len(grid) and self.c < len(grid[self.r])

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'


class XYDir:
    N = Vec2(0, 1)
    S = Vec2(0, -1)
    E = Vec2(1, 0)
    W = Vec2(-1, 0)

    L = W
    R = E
    U = N
    D = S

    _opposite = {
        N: S,
        S: N,
        E: W,
        W: E
    }

    _all = {N, S, E, W}

    @staticmethod
    def opposite(d: Self):
        return XYDir._opposite[d]

    @staticmethod
    def all():
        return XYDir._all


class RCDir:
    N = Vec2(-1, 0)
    S = Vec2(1, 0)
    E = Vec2(0, 1)
    W = Vec2(0, -1)

    L = W
    R = E
    U = N
    D = S

    _opposite = {
        N: S,
        S: N,
        E: W,
        W: E
    }

    _all = {N, S, E, W}

    @staticmethod
    def opposite(d: Self):
        return RCDir._opposite[d]

    @staticmethod
    def all():
        return RCDir._all
