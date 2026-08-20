import math
from collections.abc import Sequence
from typing import TypeVar

pi = math.pi
hpi = math.pi / 2

T = TypeVar("T",int,float)


class Vector[T: int | float](Sequence):
    """
    A vector that can be any length

    .. code-block:: python3

        from gregium.vector import Vector

        Vector(1,2,3)
        Vector(5)
        Vector(5,10,15,20,25,30,35,...)
        Vector(*(1.3,1.5,0.3,0.2))
    """

    position: tuple[T, ...]

    def __init__(self, *args: T):

        self.position = tuple(args)

    def __len__(self) -> int:

        return len(self.position)

    def __getitem__(self, i: int) -> T:

        return self.position[i]

    def __add__(self, other: "Vector[T]|T") -> "Vector[T]":

        other_type = type(other)

        if type(other) is Vector:

            return Vector(*(x + y for x, y in zip(self, other)))

        elif other_type is int or other_type is float:

            return Vector(*(x + other for x in self))

        raise TypeError(
            f"unsupported operand type(s) for +: '{type(self).__name__}' and '{other_type.__name__}'"
        )

    def __radd__(self, other: "Vector[T]|T") -> "Vector[T]":

        try:
            return self.__add__(other)
        except TypeError:
            raise TypeError(
                f"unsupported operand type(s) for +: '{type(other).__name__}' and '{type(self).__name__}'"
            )

    def __iadd__(self, other: "Vector[T]|T") -> "Vector[T]":

        try:
            return self.__add__(other)
        except TypeError:
            raise TypeError(
                f"unsupported operand type(s) for +=: '{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __sub__(self, other: "Vector[T]|T") -> "Vector[T]":

        other_type = type(other)

        if type(other) is Vector:

            return Vector(*(x - y for x, y in zip(self, other)))

        elif other_type is int or other_type is float:

            return Vector(*(x - other for x in self))

        raise TypeError(
            f"unsupported operand type(s) for -: '{type(self).__name__}' and '{other_type.__name__}'"
        )

    def __rsub__(self, other: "Vector[T]|T") -> "Vector[T]":

        try:
            return self.__sub__(other)
        except TypeError:
            raise TypeError(
                f"unsupported operand type(s) for -: '{type(other).__name__}' and '{type(self).__name__}'"
            )

    def __isub__(self, other: "Vector[T]|T") -> "Vector[T]":

        try:
            return self.__sub__(other)
        except TypeError:
            raise TypeError(
                f"unsupported operand type(s) for -=: '{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __mul__(self, other: "Vector[T]|T") -> "Vector[T]":

        other_type = type(other)

        if type(other) is Vector:

            return Vector(*(x * y for x, y in zip(self, other)))

        elif other_type is int or other_type is float:

            return Vector(*(x * other for x in self))

        raise TypeError(
            f"unsupported operand type(s) for *: '{type(self).__name__}' and '{other_type.__name__}'"
        )

    def __rmul__(self, other: "Vector[T]|T") -> "Vector[T]":

        try:
            return self.__mul__(other)
        except TypeError:
            raise TypeError(
                f"unsupported operand type(s) for *: '{type(other).__name__}' and '{type(self).__name__}'"
            )

    def __imul__(self, other: "Vector[T]|T") -> "Vector[T]":

        try:
            return self.__mul__(other)
        except TypeError:
            raise TypeError(
                f"unsupported operand type(s) for *=: '{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __truediv__(self, other: "Vector[T]|T") -> "Vector[float]":

        other_type = type(other)

        if type(other) is Vector:

            return Vector(*(x / y for x, y in zip(self, other)))

        elif other_type is int or other_type is float:

            return Vector(*(x / other for x in self))

        raise TypeError(
            f"unsupported operand type(s) for /: '{type(self).__name__}' and '{other_type.__name__}'"
        )

    def __itruediv__(self, other: "Vector[T]|T") -> "Vector[float]":

        try:
            return self.__truediv__(other)
        except TypeError:
            raise TypeError(
                f"unsupported operand type(s) for /=: '{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __floordiv__(self, other: "Vector[T]|T") -> "Vector[int]":

        other_type = type(other)

        if type(other) is Vector:

            return Vector(*(x // y for x, y in zip(self, other)))

        elif other_type is int or other_type is float:

            return Vector(*(x // other for x in self))

        raise TypeError(
            f"unsupported operand type(s) for //: '{type(self).__name__}' and '{other_type.__name__}'"
        )

    def __ifloordiv__(self, other: "Vector[T]|T") -> "Vector[int]":

        try:
            return self.__floordiv__(other)
        except TypeError:
            raise TypeError(
                f"unsupported operand type(s) for //=: '{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __mod__(self, other: "Vector[T]|T") -> "Vector[T]":

        other_type = type(other)

        if type(other) is Vector:

            return Vector(*(x % y for x, y in zip(self, other)))

        elif other_type is int or other_type is float:

            return Vector(*(x % other for x in self))

        raise TypeError(
            f"unsupported operand type(s) for %: '{type(self).__name__}' and '{other_type.__name__}'"
        )

    def __imod__(self, other: "Vector[T]|T") -> "Vector[T]":

        try:
            return self.__mod__(other)
        except TypeError:
            raise TypeError(
                f"unsupported operand type(s) for %=: '{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __lshift__(self, other: "Vector[T]|T") -> "Vector[T]":

        other_type = type(other)

        if type(other) is Vector:

            return Vector(*(x << y for x, y in zip(self, other)))

        elif other_type is int or other_type is float:

            return Vector(*(x << other for x in self))

        raise TypeError(
            f"unsupported operand type(s) for <<: '{type(self).__name__}' and '{other_type.__name__}'"
        )

    def __ilshift__(self, other: "Vector[T]|T") -> "Vector[T]":

        try:
            return self.__lshift__(other)
        except TypeError:
            raise TypeError(
                f"unsupported operand type(s) for <<=: '{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __rshift__(self, other: "Vector[T]|T") -> "Vector[T]":

        other_type = type(other)

        if type(other) is Vector:

            return Vector(*(x >> y for x, y in zip(self, other)))

        elif other_type is int or other_type is float:

            return Vector(*(x >> other for x in self))

        raise TypeError(
            f"unsupported operand type(s) for >>: '{type(self).__name__}' and '{other_type.__name__}'"
        )

    def __irshift__(self, other: "Vector[T]|T") -> "Vector[T]":

        try:
            return self.__rshift__(other)
        except TypeError:
            raise TypeError(
                f"unsupported operand type(s) for >>=: '{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __contains__(self, value: object) -> bool:
        return self.position.__contains__(value)

    def __pow__(self, other: "Vector[T]|T") -> "Vector[T]":

        other_type = type(other)

        if type(other) is Vector:

            return Vector(*(x**y for x, y in zip(self, other)))

        elif other_type is int or other_type is float:

            return Vector(*(x**other for x in self))

        raise TypeError(
            f"unsupported operand type(s) for **: '{type(self).__name__}' and '{other_type.__name__}'"
        )

    def __ipow__(self, other: "Vector[T]|T") -> "Vector[T]":

        try:
            return self.__pow__(other)
        except TypeError:
            raise TypeError(
                f"unsupported operand type(s) for **=: '{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __xor__(self, other: "Vector[T]|T") -> "Vector[T]":

        other_type = type(other)

        if type(other) is Vector:

            return Vector(*(x ^ y for x, y in zip(self, other)))

        elif other_type is int or other_type is float:

            return Vector(*(x ^ other for x in self))

        raise TypeError(
            f"unsupported operand type(s) for ^: '{type(self).__name__}' and '{other_type.__name__}'"
        )

    def __ixor__(self, other: "Vector[T]|T") -> "Vector[T]":

        try:
            return self.__xor__(other)
        except TypeError:
            raise TypeError(
                f"unsupported operand type(s) for ^=: '{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __and__(self, other: "Vector[T]|T") -> "Vector[T]":

        other_type = type(other)

        if type(other) is Vector:

            return Vector(*(x & y for x, y in zip(self, other)))

        elif other_type is int or other_type is float:

            return Vector(*(x & other for x in self))

        raise TypeError(
            f"unsupported operand type(s) for &: '{type(self).__name__}' and '{other_type.__name__}'"
        )

    def __iand__(self, other: "Vector[T]|T") -> "Vector[T]":

        try:
            return self.__and__(other)
        except TypeError:
            raise TypeError(
                f"unsupported operand type(s) for &=: '{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __or__(self, other: "Vector[T]|T") -> "Vector[T]":

        other_type = type(other)

        if type(other) is Vector:

            return Vector(*(x | y for x, y in zip(self, other)))

        elif other_type is int or other_type is float:

            return Vector(*(x | other for x in self))

        raise TypeError(
            f"unsupported operand type(s) for |: '{type(self).__name__}' and '{other_type.__name__}'"
        )

    def __ior__(self, other: "Vector[T]|T") -> "Vector[T]":

        try:
            return self.__or__(other)
        except TypeError:
            raise TypeError(
                f"unsupported operand type(s) for |=: '{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __invert__(self) -> "Vector[T]":

        return Vector(*(~x for x in self))

    def __abs__(self) -> "Vector[T]":

        return Vector(*(abs(x) for x in self))

    def __round__(self) -> "Vector[T]":

        return Vector(*(round(x) for x in self))

    def __bool__(self) -> bool:

        return any(self)

    def __eq__(self, other: "Vector[T]") -> bool:

        if type(other) is type(self):

            return not all(x - y for x, y in zip(self, other))

        raise TypeError(
            f"unsupported operand type(s) for ==: '{type(self).__name__}' and '{type(other).__name__}'"
        )

    def __ne__(self, other: "Vector[T]") -> bool:

        if type(other) is type(self):

            return any(x - y for x, y in zip(self, other))

        raise TypeError(
            f"unsupported operand type(s) for !=: '{type(self).__name__}' and '{type(other).__name__}'"
        )

    def __neg__(self) -> "Vector[T]":

        return Vector(*(-x for x in self))

    def __str__(self):

        return str(self.position)

    def __repr__(self):

        return type(self).__name__ + repr(self.position)

    def magnitude(self) -> float:
        """
        Returns the magnitude (distance) of the vector
        """
        return math.sqrt(sum(x**2 for x in self))

    def unit(self) -> "Vector[float]":
        """
        Gets the unit vector
        """

        magnitude = self.magnitude()
        if magnitude == 0:
            return Vector(*([0] * len(self)))
        return self / magnitude

    def distance(self, other: "Vector[T]") -> float:
        """
        Returns the distance to the other vector
        """

        return (self - other).magnitude()

    def relative(self, other: "Vector[T]") -> "Vector[float]":
        """
        Finds the unit vector pointing towards the other vector

        `self.distance(other) * this.relative(other) == self - other`
        """

        return (self - other).unit()

    def angle(self) -> float:
        """
        Gets the angle of the Vector [0-2π)

        Only works if the Vector is 2D
        """

        if len(self.position) != 2:
            raise ValueError('Vector must be 2D to run "angle"')

        x = self.position[0]
        y = self.position[1]

        if x == 0:
            return hpi + (pi if y < 0 else 0)
        return math.atan(y / x) + (pi if x < 0 else 0)

    def as_polar(self) -> tuple[float, float]:
        """
        Returns the vector as a polar coordinate (r,θ)

        Uses radians

        Only works if the Vector is 2D
        """

        return (self.magnitude(), self.angle())

    @classmethod
    def from_polar(cls, coordinate: tuple[float, float]) -> "Vector[float]":
        """
        Creates a new vector using the polar coordinate (r,θ)

        :param coordinate: The polar coordinate (r,θ)
        :type coordinate: tuple[float,float]

        Uses radians
        """

        x: float = coordinate[0] * math.cos(coordinate[1])
        y: float = coordinate[0] * math.sin(coordinate[1])

        return cls(x, y)

    @property
    def x(self) -> T:
        """
        The X value of the Vector

        Will raise error if Vector has < 1 dimensions
        """
        return self.position[0]

    @property
    def y(self) -> T:
        """
        The Y value of the Vector

        Will raise error if Vector has < 2 dimensions
        """
        return self.position[1]

    @property
    def z(self) -> T:
        """
        The Z value of the Vector

        Will raise error if Vector has < 3 dimensions
        """
        return self.position[2]

    @property
    def w(self) -> T:
        """
        The W value of the Vector

        Will raise error if Vector has < 4 dimensions
        """
        return self.position[3]


def Vector2(x: T, y: T) -> Vector[T]:
    """
    Generator for a 2D vector
    """

    return Vector(x, y)


def Vector3(x: T, y: T, z: T) -> Vector[T]:
    """
    Generator for a 3D vector
    """

    return Vector(x, y, z)


def Vector4(x: T, y: T, z: T, w: T) -> Vector[T]:
    """
    Generator for a 4D vector
    """

    return Vector(x, y, z, w)
