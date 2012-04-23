from  point import *

class Rectangle:

    def __init__(self, origin, corner):
        self.origin = origin
        self.corner = corner

    def __repr__(self):
        return ('(' + self.origin.__str__() + ' | '
                + self.corner.__str__() + ')')

    #Rectangle accessing - getting:

    def area(self):
        w = self.width()
        if w < 0:
            return 0
        else:
            return max(w * self.height(), 0)

    def bottom(self):
#        return self.corner.y
        return self.origin.x

    def bottom_center(self):
        return Point(self.center().x, self.bottom())

    def bottom_left(self):
#        return Point(self.origin.x, self.corner.y)
        return Point(self.origin.x, self.origin.y)

    def bottom_right(self):
#        return self.corner
        return Point(self.corner.x, self.origin.y)

    def bounding_box(self):
        return self

    def center(self):
#        return (self.top_left() + self.bottom_right()) // 2
        return Point(self.origin.x + self.corner.x, self.origin.y +self.corner.y) // 2

    def corners(self):
        return [self.top_left(),
                self.bottom_left(),
                self.bottom_right(),
                self.top_right()]

    def extent(self):
        return self.corner - self.origin

    def height(self):
        return self.corner.y - self.origin.y

    def left(self):
        return self.origin.x

    def left_center(self):
#        return Point(self.left(), self.center().y)
        return Point(self.origin.x, self.center().y)

    def right(self):
        return self.corner.x

    def right_center(self):
#        return Point(self.right(), self.center().y)
        return Point(self.corner.x, self.center().y)

    def top(self):
        return self.origin.y

    def top_center(self):
#        return Point(self.center().x, self.top())
        return Point(self.center().x, self.corner.y)

    def top_left(self):
#        return self.origin
        return Point(self.origin.x, self.corner.y)

    def top_right(self):
#        return Point(self.corner.x, self.origin.y)
        return self.corner

    def width(self):
        return self.corner.x - self.origin.x

    def position(self):
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

    def inset_by(self, delta):
        if isinstance(delta, Rectangle):
            return Rectangle(self.origin + delta.origin, self.corner - delta.corner)
        else:
            return Rectangle(self.origin + delta, self.corner - delta)

    def expand_by(self, integer):
        return Rectangle(self.origin - integer, self.corner + integer)

    def intersect(self, aRectangle):
        return Rectangle(self.origin.max(aRectangle.origin),
                         self.corner.min(aRectangle.corner))

    def merge(self, aRectangle):
        return Rectangle(self.origin.min(aRectangle.origin),
                         self.corner.max(aRectangle.corner))

    #Rectangle testing:

    def contains_point(self, point):
        return self.origin <= point and point < self.corner

    def contains_rectangle(self, rectangle):
        return (rectangle.origin >= self.origin
                and rectangle.corner <= self.corner)

    def intersects(self, rectangle):
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

    def scale_by(self, scale):
        "scale can be either a Point or a scalar"
        return Rectangle(self.origin * scale, self.corner * scale)

    def translate_by(self, factor):
        "factor can be either a Point or a scalar"
        return Rectangle(self.origin + factor, self.corner + factor)
