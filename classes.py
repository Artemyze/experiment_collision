from typing import List
from pygame import Vector2

ter = []
class Asteroids:
    def __init__(self, x, y, vector2d: Vector2):
        self._x = x
        self._y = y
        self._box = None
        self._endurance = 1
        self._collision_model = 1
        self._speed = vector2d

    def move(self):
        self._x = self._x + self._speed.x
        self._y = self._y + self._speed.y

    def death(self):
        pass

    @property
    def box(self):
        self._box = QBox(self._x, self._y, 1, 1)
        return self._box

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, vector: Vector2):
        self._speed = vector

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def endurance(self):
        pass

    @property
    def collision_model(self):
        pass

class Point:
    def __init__(self, x_coord=0, y_coord=0):
        self.x = x_coord
        self.y = y_coord

    def __add__(self, other: "Point"):
        self.x += other.x
        self.y += other.y
        return self

    def __truediv__(self, t):
        self.x /= t
        self.y /= t
        return self


class QBox:
    def __init__(self, left=0, top=0, width=0, height=0):
        self.__left = left
        self.__top = top
        self.__width = width
        self.__height = height

    @classmethod
    def from_points(cls, pos: Point, size: Point):
        return QBox(pos.x, pos.y, size.x, size.y)

    @property
    def top(self):
        return self.__top

    @property
    def left(self):
        return self.__left

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def get_right(self):
        return self.__left + self.__width

    def get_bottom(self):
        return self.__top + self.__height

    def get_top_left(self):
        return Point(self.__left, self.__top)

    def get_center(self):
        return Point(self.__left + self.__width / 2, self.__top + self.__height / 2)

    def get_size(self):
        return Point(self.__width, self.__height)

    def contain(self, box: "QBox"):
        return self.__left <= box.__left \
            & box.get_right() <= self.get_right() & \
            self.__top <= box.__top & \
            box.get_bottom() <= self.get_bottom()

    def intersects(self, box: "Box"):
        return (not (self.__left >= box.get_right() or self.get_right() <= box.__left or
                     self.__top >= box.get_bottom() or self.get_bottom() <= box.__top))

    def __repr__(self):
        return f'{self.__top} {self.__left} {self.__width} {self.__height}'


def get_box(value: Point):
    return QBox.from_points(value, value)


class QTree:
    MAX_DEPTH = 7
    THRESHOLD = 1

    def __init__(self, box: QBox, values: List[Asteroids]):
        self.root = self.QNode(0, box, values)
        self.values = values
        self.__add()

    class QNode:
        def __init__(self, depth, box: QBox, values=None):
            if values is None:
                self.values = []
            else:
                self.values = values
            self.children = []
            self.max_values = 1
            self.box = box
            self.depth = depth

        def getQuadrant(self, nodeBox: QBox, valueBox: QBox):
            center = nodeBox.get_center()
            if valueBox.get_right() < center.x:
                if valueBox.get_bottom() < center.y:
                    return 0
                elif valueBox.top >= center.y:
                    return 2
                else:
                    return -1
            elif valueBox.left >= center.x:
                if valueBox.get_bottom() < center.y:
                    return 1
                elif valueBox.top >= center.y:
                    return 3
                else:
                    return -1
            else:
                return -1

        def compute_box(self, value: QBox, i: int):
            origin = value.get_top_left()
            child_size = value.get_size() / 2
            if i == 0:
                northWest = QBox.from_points(origin, child_size)
                return northWest
            elif i == 1:
                northEastPoint = Point(origin.x + child_size.x, origin.y)
                northEast = QBox.from_points(northEastPoint, child_size)
                return northEast
            elif i == 2:
                southWestPoint = Point(origin.x, origin.y + child_size.y)
                southWest = QBox.from_points(southWestPoint, child_size)
                return southWest
                pass
            elif i == 3:
                southEastPoint = origin + child_size
                southEast = QBox.from_points(southEastPoint, child_size)
                return southEast

        def isLeaf(self):
            return len(self.children)==0

        def add(self, value: Asteroids):
            if self.isLeaf():
                if self.depth >= QTree.MAX_DEPTH or len(self.values) < QTree.THRESHOLD:
                    self.values.append(value)
                else:
                    self.split()
                    self.add(value)
            #if len(self.values) >= QTree.THRESHOLD:
            else:
                i = self.getQuadrant(self.box, value.box)
                if i==-1:
                    return
                else:
                    self.children[i].add(value)

        def build(self):
            if self.depth >= QTree.MAX_DEPTH:
                return
            else:
                if not self.isLeaf:
                    self.split()
                for node in self.children:
                    node.build()

        
        def remove_val(self):
            self.values = []

        def split(self):
            self.children = [None] * 4
            for i in range(0, 4):
                new_box = self.compute_box(self.box, i)
                new_node = QTree.QNode(self.depth + 1, new_box, [])
                self.children[i] = new_node

    def __add(self):
        for i in range(len(self.values)):
            self.root.add(self.values[i])

    def get_boxes(self, node: QNode, r, k):
        r.append(node.box)
        k.append(node.depth)
        if len(node.children) != 0:
            for child in node.children:
                self.get_boxes(child, r, k)
        return r, k
