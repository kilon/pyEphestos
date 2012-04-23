from .rectangle import *

class Point:
    """ Point class defines the behavior of Points"""

    def __init__(self, x, y):
        """ Point is initialised with 2 parameters (x,y) defining the coordinates"""
        self.x = x
        self.y = y

    def __repr__(self):
        """ getter : return the string representation of point object"""
        return self.x.__str__() + '@' + self.y.__str__()

    #Point comparison:

    def __eq__(self, other):
        """ getter (point) : compare current point with another point and return True of False whether they are equal"""
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __ne__(self, other):
        """ getter (point) : compare current point with another point and return True of False whether they are not equal"""
        return not self.__eq__(other)

    def __lt__(self, other):
        """ getter (point) : compare current point with another point and return True of False whether the first is less than the second"""
        if isinstance(other, Point):
            return self.x < other.x and self.y < other.y
        return NotImplemented

    def __gt__(self, other):
        """ getter (point) : compare current point with another point and return True of False whether the first is greater than the second"""
        if isinstance(other, Point):
            return self.x > other.x and self.y > other.y
        return NotImplemented

    def __le__(self, other):
        """ getter (point) : compare current point with another point and return True of False whether the first is less than or equal to the second"""
        if isinstance(other, Point):
            return self.x <= other.x and self.y <= other.y
        return NotImplemented

    def __ge__(self, other):
        """ getter (point) : compare current point with another point and return True of False whether the first is greater than or equal to  the second"""
        if isinstance(other, Point):
            return self.x >= other.x and self.y >= other.y
        return NotImplemented

    def __round__(self):
        """ getter  : return the round of the point"""
        return Point(round(self.x), round(self.y))

    def max(self, other):
        """ getter (point) : compare current point with another point and return the max between the two"""
        return Point(max(self.x, other.x), max(self.y, other.y))

    def min(self, other):
        """ getter (point) : compare current point with another point and return the min between the two"""
        return Point(min(self.x, other.x), min(self.y, other.y))

    #Point arithmetic:

    def __add__(self, other):
        """ getter (point) : add current point with another point and return the result point"""
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        return Point(self.x + other, self.y + other)

    def __sub__(self, other):
        """ getter (point) : substract current point with another point and return the result point"""
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        return Point(self.x - other, self.y - other)

    def __mul__(self, other):
        """ getter (point) : multiply current point with another point and return the result point"""
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y)
        return Point(self.x * other, self.y * other)

    def __div__(self, other):
        """ getter (point) : divide current point with another point and return the result point"""
        if isinstance(other, Point):
            return Point(self.x / other.x, self.y / other.y)
        return Point(self.x / other, self.y / other)

    def __truediv__(self, other):
        """ getter (point) : true divide current point with another point and return the result point"""
        if isinstance(other, Point):
            return Point(self.x / other.x, self.y / other.y)
        return Point(self.x / other, self.y / other)

    def __floordiv__(self, other):
        """ getter (point) : floor divide current point with another point and return the result point"""
        if isinstance(other, Point):
            return Point(self.x // other.x, self.y // other.y)
        return Point(self.x // other, self.y // other)

    def __abs__(self):
        """ getter  : return the abs"""
        return Point(abs(self.x), abs(self.y))

    def __neg__(self):
        """ getter  : return the negative"""
        return Point(-self.x, -self.y)

    #Point functions:

    def dot_product(self, other):
        """ getter (point) : return the the dot product between the current point and another point"""
        return self.x * other.x + self.y * other.y

    def cross_product(self, other):
        """ getter (point) : return the the cross product between the current point and another point"""
        return self.x * other.y - self.y * other.x

    def distance_to(self, other):
        """ getter (point) : return the the distance between the current point and another point"""
        return (other - self).r()

    def rotate(self, direction, center):
        """ getter (direction,center) : return the the rotation point relative to a center and towards a direction"""
        "direction must be 'right', 'left' or 'pi'"
        offset = self - center
        if direction == 'right':
            return Point(-offset.y, offset.y) + center
        elif direction == 'left':
            return Point(offset.y, -offset.y) + center
        elif direction == 'pi':
            return center - offset
        else:
            return NotImplemented

    def flip(self, direction, center):
        """ getter (direction,center) : return the fliped point relative to a center and towards a direction.Direction must be 'vertical' or 'horizontal"""
        if direction == 'vertical':
            return Point(self.x, center.y * 2 - self.y)
        elif direction == 'horizontal':
            return Point(center.x * 2 - self.x, self.y)
        else:
            return NotImplemented

    #Point polar coordinates:

    def r(self):
#PKHG        return math.sqrt(self.dot_product(self))
        return sqrt(self.dot_product(self))

    #Point transforming:

    def scale_by(self, scalePoint):
        """ getter (point) : return the current point scaled by another point"""
        return Point(scalePoint.x * self.x, scalePoint.y * self.y)

    def translate_by(self, deltaPoint):
        """ getter (point) : return the current point translated by another point"""
        return Point(deltaPoint.x + self.x, deltaPoint.y + self.y)

    #Point converting:

    def as_list(self):
        """ getter : return the current point as a list"""
        return [self.x, self.y]

    def corner(self, cornerPoint):
        """ getter : return the rectangle of the current point with another point"""
        return Rectangle(self, cornerPoint)

    def rectangle(self, aPoint):
        """ getter : return the rectangle of the current point with another point using min and max"""
        return Rectangle(self.min(aPoint), self.max(aPoint))

    def extent(self, extentPoint):
        """ getter : return the rectangle of the current point with another point using extend"""
        return Rectangle(self, self + extentPoint)
