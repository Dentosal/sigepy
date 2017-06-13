from vector import Vector
from math import pi

EPSILON = 1e-10

class Rect(object):
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], self.__class__):
            self.x = args[0].x
            self.y = args[0].y
            self.w = args[0].w
            self.h = args[0].h
        elif len(args) == 2:
            p = Vector(args[0])
            s = Vector(args[1])
            self.x = p.x
            self.y = p.y
            self.w = s.x
            self.h = s.y
        elif len(args) == 4 and all(isinstance(a, (int, float)) for a in args):
            self.x = args[0]
            self.y = args[1]
            self.w = args[2]
            self.h = args[3]
        else:
            raise ValueError()

    @property
    def center(self):
        return Vector(self.x + self.w / 2, self.y + self.h / 2)

    @property
    def corners(self):
        return [
            Vector(self.x,          self.y),
            Vector(self.x + self.w, self.y),
            Vector(self.x,          self.y + self.h),
            Vector(self.x + self.w, self.y + self.h)
        ]

    @property
    def surrounding_rect(self):
        return Rect(*self.as_tuple)

    @property
    def as_tuple(self):
        return (self.x, self.y, self.w, self.h)

    @property
    def rotation(self):
        return 0

    def rotated(self, rotation):
        return RotatedRect(*self.as_tuple, rotation)

    def contains(self, p: Vector):
        return (
            self.x <= p.x <= self.x + self.w and
            self.y <= p.y <= self.y + self.h
        )

    def __eq__(self, other):
        return all(abs(s - o) < EPSILON for s, o in zip(self.as_tuple, other.as_tuple))

    def __repr__(self):
        return f"Rect({self.x:.4f}, {self.y:.4f}, {self.w:.4f}, {self.h:.4f})"

class RotatedRect(Rect):
    def __init__(self, *args):
        super().__init__(*args[:-1])
        self._rotation = args[-1]

    @property
    def rotation(self):
        rot = self._rotation
        while rot < 0:
            rot += 2 * pi
        rot = rot % (2 * pi)
        self._rotation = rot
        return self._rotation

    @property
    def corners(self):
        return [(c - self.center).rotated(self.rotation) + self.center for c in super().corners]

    @property
    def surrounding_rect(self):
        c = self.corners
        min_x = min(p.x for p in c)
        min_y = min(p.y for p in c)
        max_x = max(p.x for p in c)
        max_y = max(p.y for p in c)
        return Rect(min_x, min_y, max_x - min_x, max_y - min_y)

    def rotated(self, rotation):
        return RotatedRect(*self.as_tuple, self.rotation + rotation)

    def contains(self, p: Vector):
        p = (p - self.center).rotated(-self.rotation) + self.center
        return super().contains(p)

    def __eq__(self, other):
        return self.surrounding_rect == other.surrounding_rect

    def __repr__(self):
        return f"{super().__repr__()}.rotated({self.rotation:.4f})"
