

import bgl
import copy
import math
version = '2009-Nov-06'
TRANSPARENT = 0

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return self.x.__str__() + '@' + self.y.__str__()

    #Point comparison:

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, Point):
            return self.x < other.x and self.y < other.y
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Point):
            return self.x > other.x and self.y > other.y
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Point):
            return self.x <= other.x and self.y <= other.y
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Point):
            return self.x >= other.x and self.y >= other.y
        return NotImplemented

    def __round__(self):
        return Point(round(self.x), round(self.y))

    def max(self, other):
        return Point(max(self.x, other.x), max(self.y, other.y))
    
    def min(self, other):
        return Point(min(self.x, other.x), min(self.y, other.y))

    #Point arithmetic:

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        return Point(self.x + other, self.y + other)
        
    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        return Point(self.x - other, self.y - other)

    def __mul__(self, other):
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y)
        return Point(self.x * other, self.y * other)

    def __div__(self, other):
        if isinstance(other, Point):
            return Point(self.x / other.x, self.y / other.y)
        return Point(self.x / other, self.y / other)

    def __floordiv__(self, other):
        if isinstance(other, Point):
            return Point(self.x // other.x, self.y // other.y)
        return Point(self.x // other, self.y // other)

    def __abs__(self):
        return Point(abs(self.x), abs(self.y))

    def __neg__(self):
        return Point(-self.x, -self.y)

    #Point functions:

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y
    
    def cross_product(self, other):
        return self.x * other.y - self.y * other.x

    def distance_to(self, other):
        return (other - self).r()

    def rotate(self, direction, center):
        "direction must be 'right', 'left' or 'pi'"
        offset = self - center
        if direction == 'right':
            return Point(-offset.y, offset,y) + center
        elif direction == 'left':
            return Point(offset.y, -offset.y) + center
        elif direction == 'pi':
            return center - offset
        else:
            return NotImplemented
    
    def flip(self, direction, center):
        "direction must be 'vertical' or 'horizontal'"

        if direction == 'vertical':
            return Point(self.x, center.y * 2 - self.y)
        elif direction == 'horizontal':
            return Point(center.x * 2 - self.x, self.y)
        else:
            return NotImplemented

    #Point polar coordinates:

    def r(self):
        return math.sqrt(self.dot_product(self))

    #Point transforming:

    def scale_by(self, scalePoint):
        return Point(scalePoint.x * self.x, scalePoint.y * self.y)

    def translate_by(self, deltaPoint):
        return Point(deltaPoint.x + self.x, deltaPoint.y + self.y)

    #Point converting:

    def as_list(self):
        return [self.x, self.y]

    def corner(self, cornerPoint):
        return Rectangle(self, cornerPoint)

    def rectangle(self, aPoint):
        return Rectangle(self.min(aPoint), self.max(aPoint))

    def extent(self, extentPoint):
        return Rectangle(self, self + extentPoint)
    
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
        return self.corner.y

    def bottom_center(self):
        return Point(self.center().x, self.bottom())

    def bottom_left(self):
        return Point(self.origin.x, self.corner.y)

    def bottom_right(self):
        return self.corner

    def bounding_box(self):
        return self

    def center(self):
        return (self.top_left() + self.bottom_right()) // 2

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
        return Point(self.left(), self.center().y)

    def right(self):
        return self.corner.x

    def right_center(self):
        return Point(self.right(), self.center().y)

    def top(self):
        return self.origin.y

    def top_center(self):
        return Point(self.center().x, self.top())

    def top_left(self):
        return self.origin

    def top_right(self):
        return Point(self.corner.x, self.origin.y)

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


class Node(object):

    def __init__(self, name = 'node'):
        self.parent = None
        self.children = []
        self.name = name

    def __repr__(self):
        return 'aNode(' + self.name + ')'

    #Node accessing:

    def add_child(self, node):
        self.children.append(node)
        node.parent = self

    def remove_child(self, node):
        self.children.remove(node)
        node.parent = None

    #Node functions:

    def root(self):
        if self.parent == None:
            return self
        else:
            return self.parent.root()

    def depth(self):
        if self.parent == None:
            return 0
        else:
            return self.parent.depth() + 1

    def all_children(self):
        "includes myself"
        result = [self]
        for child in self.children:
            result.extend(child.all_children())
        return result        

    def all_leafs(self):
        result = []
        for element in self.all_children():
            if element.children == []:
                result.append(element)
        return(result)

    def all_parents(self):
        "includes myself"
        result = [self]
        if self.parent != None:
            result.extend(self.parent.all_parents())
        return result        

    def siblings(self):
        result = []
        for element in self.parent.children:
            if element is not self:
                result.append(element)
        return result

    def parent_of_class(self, aClass):
        "answer the first of my parents which is an instance of aClass"
        for element in self.all_parents():
            if isinstance(element, aClass):
                return element
        return None

    def child_of_class(self, aClass):
        "answer the first of my children which is an instance of aClass"
        for element in self.all_children():
            if isinstance(element, aClass):
                return element
        return None

class Morph(Node):

    def __init__(self):
        super(Morph, self).__init__()
        self.bounds = Point(0, 0).corner(Point(50,40))
        self.color = (0.3, 0.3, 0.3)
        self.alpha = 1 
        self.is_visible = True
        self.is_draggable = True
        #self.draw_new()
        self.fps = 0
        # self.last_time = pygame.time.get_ticks()
      
    def __repr__(self):
        return self.__class__.__name__

    def delete(self):
        if self.parent != None:
            self.full_changed()
            self.parent.remove_child(self)

    #stepping:

    def wants_to_step(self):
        return self.is_visible

    def step(self):
        pass

    #Morph accessing - geometry getting:

    def left(self):
        return self.bounds.left()

    def right(self):
        return self.bounds.right()

    def top(self):
        return self.bounds.top()

    def bottom(self):
        return self.bounds.bottom()

    def center(self):
        return self.bounds.center()

    def bottom_center(self):
        return self.bounds.bottom_center()

    def bottom_left(self):
        return self.bounds.bottom_left()

    def bottom_right(self):
        return self.bounds.bottom_right()

    def bounding_box(self):
        return self.bounds

    def corners(self):
        return self.bounds.corners()

    def left_center(self):
        return self.bounds.left_center()

    def right_center(self):
        return self.bounds.right_center()

    def top_center(self):
        return self.bounds.top_center()

    def top_left(self):
        return self.bounds.top_left()

    def top_right(self):
        return self.bounds.top_right()

    def position(self):
        return self.bounds.origin

    def extent(self):
        return self.bounds.extent()

    def width(self):
        return self.bounds.width()

    def height(self):
        return self.bounds.height()

    def full_bounds(self):
        result = self.bounds
        for child in self.children:
            result = result.merge(child.full_bounds())
        return result

    #Morph accessing - changing:

    def set_position(self, aPoint):
        delta = aPoint - self.top_left()
        if delta.x != 0 or delta.y != 0:
            self.move_by(delta)

    def set_center(self, aPoint):
        self.set_position(aPoint - (self.extent() // 2))

    def set_full_center(self, aPoint):
        self.set_position(aPoint - (self.full_bounds().extent() // 2))

    def set_width(self, width):
        self.changed()
        self.bounds.corner = Point(self.bounds.origin.x + width,
                                   self.bounds.corner.y)
        self.changed()

    def set_height(self, height):
        self.changed()
        self.bounds.corner = Point(self.bounds.corner.x,
                                   self.bounds.origin.y + height)
        self.changed()

    def set_extent(self, aPoint):
        self.set_width(max(aPoint.x,0))
        self.set_height(max(aPoint.y,0))

    def move_by(self, delta):
        "move myself by a delta point value"
        self.changed()
        self.bounds = self.bounds.translate_by(delta)
        for child in self.children:
            child.move_by(delta)
        self.changed()

    def keep_within(self, morph):
        "make sure I am completely within another morph's bounds"
        left_off = self.full_bounds().left() - morph.left()
        if left_off < 0:
            self.move_by(Point(-left_off, 0))
        right_off = self.full_bounds().right() - morph.right()
        if right_off > 0:
            self.move_by(Point(-right_off, 0))
        top_off = self.full_bounds().top() - morph.top()
        if top_off < 0:
            self.move_by(Point(0, -top_off))
        bottom_off = self.full_bounds().bottom() - morph.bottom()
        if bottom_off > 0:
            self.move_by(Point(0, -bottom_off))

    #Morph displaying:

    def draw_new(self):
        "initialize my surface"
        print("I use color : ", self.color)
        bgl.glColor4f(self.color[0],self.color[1],self.color[2] ,self.alpha)
        
        dimensions = self.extent().as_list()
        
        print("origin : ",self.bounds.origin)
        
        bgl.glRecti(self.position().x, self.position().y, dimensions[0], dimensions[1])  
