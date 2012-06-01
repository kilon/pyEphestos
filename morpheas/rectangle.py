from math import *
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

    def get_dot_product(self, other):
        """ getter (point) : return the the dot product between the current point and another point"""
        return self.x * other.x + self.y * other.y

    def get_cross_product(self, other):
        """ getter (point) : return the the cross product between the current point and another point"""
        return self.x * other.y - self.y * other.x

    def get_distance_to(self, other):
        """ getter (point) : return the the distance between the current point and another point"""
        return (other - self).get_r()
    
    def get_rotate(self, direction, center):
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

    def get_flip(self, direction, center):
        """ getter (direction,center) : return the fliped point relative to a center and towards a direction.Direction must be 'vertical' or 'horizontal"""
        if direction == 'vertical':
            return Point(self.x, center.y * 2 - self.y)
        elif direction == 'horizontal':
            return Point(center.x * 2 - self.x, self.y)
        else:
            return NotImplemented

    #Point polar coordinates:

    def get_r(self):
#PKHG        return math.sqrt(self.dot_product(self))
        return sqrt(self.get_dot_product(self))

    #Point transforming:

    def get_scale_by(self, scalePoint):
        """ getter (point) : return the current point scaled by another point"""
        return Point(scalePoint.x * self.x, scalePoint.y * self.y)

    def get_translate_by(self, deltaPoint):
        """ getter (point) : return the current point translated by another point"""
        return Point(deltaPoint.x + self.x, deltaPoint.y + self.y)

    #Point converting:

    def as_list(self):
        """ getter : return the current point as a list"""
        return [self.x, self.y]
#PKHG.ERROR, not a gette but a setter but should be removed.
#PKHG.decision 09052012_0954 not needed up to other ideas
#    def get_corner(self, cornerPoint):
#        """ getter : return the rectangle of the current point with another point"""
#        return Rectangle(self, cornerPoint)

    def get_rectangle(self, aPoint):
        """ getter : return the rectangle of the current point with another point using min and max"""
        return Rectangle(self.min(aPoint), self.max(aPoint))

    def get_extent(self, extentPoint):
        """ getter : return the rectangle of the current point with another point using extend"""
        return Rectangle(self, self + extentPoint)


class Rectangle:

    def __init__(self, origin, corner):
        self.origin = origin
        self.corner = corner

    def __repr__(self):
        return ('(' + self.origin.__str__() + ' | '
                + self.corner.__str__() + ')')

    #Rectangle accessing - getting:

    def get_area(self):
        w = self.get_width()
        if w < 0:
            return 0
        else:
            return max(w * self.get_height(), 0)

    def get_bottom(self):
#        return self.corner.y
        return self.origin.x

    def get_bottom_center(self):
        return Point(self.get_center().x, self.get_bottom())

    def get_bottom_left(self):
#        return Point(self.origin.x, self.corner.y)
        return Point(self.origin.x, self.origin.y)

    def get_bottom_right(self):
#        return self.corner
        return Point(self.corner.x, self.origin.y)

    def get_bounding_box(self):
        return self

    def get_center(self):
#        return (self.top_left() + self.bottom_right()) // 2
        return Point(self.origin.x + self.corner.x, self.origin.y +self.corner.y) // 2

    def get_corners(self):
        return [self.get_top_left(),
                self.get_bottom_left(),
                self.get_bottom_right(),
                self.get_top_right()]

    def get_extent(self):
        return self.corner - self.origin

    def get_height(self):
        return self.corner.y - self.origin.y

    def get_left(self):
        return self.origin.x

    def get_left_center(self):
#        return Point(self.left(), self.center().y)
        return Point(self.origin.x, self.get_center().y)

    def get_right(self):
        return self.corner.x

    def get_right_center(self):
#        return Point(self.right(), self.center().y)
        return Point(self.corner.x, self.get_center().y)

    def get_top(self):
        return self.origin.y

    def get_top_center(self):
#        return Point(self.center().x, self.top())
        return Point(self.get_center().x, self.corner.y)

    def get_top_left(self):
#        return self.origin
        return Point(self.origin.x, self.corner.y)

    def get_top_right(self):
#        return Point(self.corner.x, self.origin.y)
        return self.corner

    def get_width(self):
        return self.corner.x - self.origin.x

    def get_position(self):
        return self.origin

    #Rectangle comparison:

    def __eq__(self, other):
        if isinstance(other, Rectangle):
            return (self.origin == other.origin
                    and self.corner == other.corner)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    #Rectangle functions:

    def get_inset_by(self, delta):
        if isinstance(delta, Rectangle):
            return Rectangle(self.origin + delta.origin, self.corner - delta.corner)
        else:
            return Rectangle(self.origin + delta, self.corner - delta)

    def get_expand_by(self, integer):
        return Rectangle(self.origin - integer, self.corner + integer)

    def get_intersect(self, aRectangle):
        return Rectangle(self.origin.max(aRectangle.origin),
                         self.corner.min(aRectangle.corner))

    def get_merge(self, aRectangle):
        if self  == Rectangle(Point(300,300),Point(360,380)):
            print("----L296  rectangle.py self, aRectangle,getmerged aRectangle",self, aRectangle, self.origin.min(aRectangle.origin),self.corner.max(aRectangle.corner))
        return Rectangle(self.origin.min(aRectangle.origin),
                         self.corner.max(aRectangle.corner))

    #Rectangle testing:

    def get_contains_point(self, point):
        return self.origin <= point and point < self.corner

    def get_contains_rectangle(self, rectangle):
        return (rectangle.origin >= self.origin
                and rectangle.corner <= self.corner)

    def get_intersects(self, rectangle):
        ro = rectangle.origin
        rc = rectangle.corner
        if rc.x < self.origin.x:
            return False
        elif rc.y < self.origin.y:
            return False
        elif ro.x > self.corner.x:
            return False
        elif ro.y > self.corner.y:
            return False
        else:
            return True

    #Rectangle transforming:

    def get_scale_by(self, scale):
        """scale can be either a Point or a scalar"""
        return Rectangle(self.origin * scale, self.corner * scale)

    def get_translate_by(self, factor):
        """factor can be either a Point or a scalar"""
        return Rectangle(self.origin + factor, self.corner + factor)
