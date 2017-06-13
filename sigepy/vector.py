from math import sqrt, pi, sin, cos, atan2

class Vector(object):
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], self.__class__):
            self.x = args[0].x
            self.y = args[0].y
        elif len(args) == 2 and all(isinstance(a, (int, float)) for a in args):
            self.x = float(args[0])
            self.y = float(args[1])
        else:
            raise ValueError()

    @classmethod
    def from_angle(cls, angle):
        assert isinstance(angle, (int, float))
        angle %= pi * 2
        return cls(cos(angle), sin(angle))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @property
    def zero(self):
        return self.x == 0 and self.y == 0

    @property
    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    @property
    def len(self):
        return self.length

    def __abs__(self):
        return self.length

    def __neg__(self):
        return self.__class__(-self.x, -self.y)

    def __add__(self, other):
        assert isinstance(other, self.__class__)
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        assert isinstance(other, self.__class__)
        return self.__class__(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        assert isinstance(other, (int, float))
        return self.__class__(self.x * other, self.y * other)

    def __div__(self, other):
        assert isinstance(other, (int, float))
        return self.__class__(self.x / other, self.y / other)

    @property
    def normalized(self):
        if self.zero:
            return self.__class__(0, 0)
        else:
            return self.__class__(self.x / self.length, self.y / self.length)

    @property
    def angle(self):
        if self.zero:
            raise ArithmeticError("Null vector has no angle")

        a = atan2(self.y, self.x)
        if a < 0:
            a += 2 * pi;
        return a

    def rotated(self, angle):
        """Rotates this vector counterclockwise by angle radians and returns the result."""
        if self.zero:
            return Vector(0, 0)
        else:
            return Vector.from_angle(self.angle + angle) * self.length

    def smaller_angle_between(self, other):
        """Returns the smaller angle between two vectors."""
        return abs(self.angle - other.angle) % pi

    def directed_angle_between(self, other):
        """Returns a directed angle between two vectors."""
        a = abs(self.angle - other.angle)
        if a > pi:
            a -= pi * 2
        return a

    def distance_to(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __iter__(self):
        yield self.x
        yield self.y

    def __repr__(self):
        if isinstance(self.x, int) and isinstance(self.y, int):
            return "{}({}, {})".format(self.__class__.__name__, self.x, self.y)
        return "{}({:.4f}, {:.4f})".format(self.__class__.__name__, self.x, self.y)
