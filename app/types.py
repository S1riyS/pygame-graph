import typing as t
from enum import Enum


class Function(t.NamedTuple):
    function: t.Callable
    left_x: t.Optional[float] = None
    right_x: t.Optional[float] = None


class GraphType(str, Enum):
    CARTESIAN = 'CARTESIAN'
    POLAR = 'POLAR'
