import bgl, blf
import copy
#PKHG direct import!! import math #PKHG todo sqrt, sin , cos, degrees
from math import radians, sin, cos, sqrt
version = '2012-Apr-16'
TRANSPARENT = 0
debug_mouse = False
debug_mymorph = False
debug_world = False

#winding.ttf
#font = blf.load("c:/Windows/Fonts/Verdana.ttf");print("\n===start++++++DBG parse L12" , font, blf.dimensions(font,"PKHG "))

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
        """ getter (direction,center) : return the the rotation point relative to a center and towards a direction. Direction must be 'right', 'left' or 'pi'"""
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
        """ getter (direction,center) : return the fliped point relative to a center and towards a direction.D irection must be 'vertical' or 'horizontal"""
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

class Morph(Node ): 
    
    def __init__(self, bounds = None, rounded = False, with_name = False):
        super(Morph, self).__init__()
        if bounds:
            self.bounds = bounds
        else:
            self.bounds = Point(0, 0).corner(Point(100,60))
        self.color = (0.3, 0.3, 0.3)
        self.alpha = 1
        self.is_visible = True
        self.is_draggable = True
        self.fps = 0
        self.rounded = rounded
        # self.last_time = pygame.time.get_ticks()
        self.with_name = with_name

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
#        delta = aPoint - self.top_left()
        delta = aPoint - self.bottom_left()
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
    def draw_new(self,event):
        "initialize my surface"
        # print("I use color : ", self.color)
        bgl.glColor4f(self.color[0],self.color[1],self.color[2] ,self.alpha)
        # new_position = Point(event.mouse_region_x,event.mouse_region_y)

        # self.set_position(new_position)


        dimensions = self.extent().as_list()

        # print("dimensions : ", dimensions)
        if self.rounded:
            draw_rounded_morph(self, small = 0.2)        
        else:
            bgl.glRecti(self.position().x, self.position().y, self.position().x+dimensions[0], self.position().y+dimensions[1])
        # print ("I draw a rect : ", [self.position().x, self.position().y, self.position().x+dimensions[0], self.position().y+dimensions[1]])
        font_id = blf.load("c:/Windows/Fonts/arialbd.ttf")
        size = 36
        blf.size(font_id, size, 72)
        dims_x,dims_y = blf.dimensions(font_id, self.name)
        x = self.bounds.origin.x 
        xx = self.bounds.corner.x

        difx = xx - x
        if dims_x > difx:
            quot = difx/dims_x
            size = int(size * quot)
        y = self.bounds.corner.y - size
        if self.with_name:
            DrawStringToViewport(self.name, self, size , (1,1,1,1), font_id, x , y)


    def draw_on(self, rectangle=None):
        if not self.is_visible:
            return
        if rectangle == None:
            rectangle = self.bounds
        area = rectangle.intersect(self.bounds)
        if area.extent() > Point(0,0):
            p = area.origin.as_list()
            area.origin = area.origin - self.bounds.origin
            area.corner = area.corner - self.bounds.origin
            self.draw_new()

    def full_draw_on(self, rectangle=None):
        if not self.is_visible:
            return
        if rectangle == None:
            rectangle = self.full_bounds()
        self.draw_on(rectangle)
        for child in self.children:
            child.full_draw_on(rectangle)

    def hide(self):
        self.is_visible = False
        self.changed()
        for morph in self.children:
            morph.hide()

    def show(self):
        self.is_visible = True
        self.changed()
        for morph in self.children:
            morph.show()

    def toggle_visibility(self):
        self.is_visible = not self.is_visible
        self.changed()
        for morph in self.children:
            morph.toggle_visibility()

    #Morph updating:

    def changed(self):
        w = self.root()
        """
        if isinstance(w, World):
            w.broken.append(copy.copy(self.bounds))
        """

    def full_changed(self):
        w = self.root()
        if isinstance(w, World):
            w.broken.append(copy.copy(self.full_bounds()))

    #Morph accessing - structure:
    """
    def world(self):
        if isinstance(self.root(), World):
            return self.root()
    """
    def add(self, morph):
        parent = morph.parent
        if parent is not None:
            parent.remove_child(morph)
        self.add_child(morph)

    def morph_at(self, point):
        morphs = self.all_children()
        for m in morphs[::-1]:
            if m.full_bounds().contains_point(point):
                return m

    #Morph duplicating:

    def full_copy(self):
        new = copy.copy(self)
        lst = []
        for m in self.children:
            new_child = m.full_copy()
            new_child.parent = new
            lst.append(new_child)
        new.children = lst
        return new

    def duplicate(self):
        clone = self.full_copy()
        clone.parent = None
        clone.pick_up()

    #Morph dragging and dropping:

    def root_for_grab(self):
        if self.parent == None or isinstance(self.parent, Frame):
            return self
        else:
            return self.parent.root_for_grab()

    def wants_drop_of(self, morph):
        "default is False - change for subclasses"
        return False

    def pick_up(self):
        self.set_position(world.hand.position() - (self.extent() // 2))
        world.hand.grab(self)

    #Morph events:

    def handles_mouse_over(self):
        return False

    def handles_mouse_click(self):
        return False

    def handles_mouse_move(self):
        return False

    def mouse_down_left(self, pos):
        pass

    def mouse_up_left(self, pos):
        pass

    def mouse_click_left(self, pos):
        pass


    def mouse_down_middle(self, pos):
        pass

    def mouse_up_middle(self, pos):
        pass

    def mouse_click_middle(self, pos):
        pass

    def mouse_down_right(self, pos):
        pass

    def mouse_up_right(self, pos):
        pass

    def mouse_click_right(self, pos):
        pass

    def mouse_enter(self):
        pass

    def mouse_enter_dragging(self):
        pass

    def mouse_leave(self):
        pass

    def mouse_leave_dragging(self):
        pass

    def mouse_move(pos):
        pass

    #Morph menus:

    def context_menu(self):
        if world.is_dev_mode:
            return self.developers_menu()
        else:
            return None

    def developers_menu(self):
        menu = Menu(self, self.__class__.__name__)
        menu.add_item("pick up", 'pick_up')
        menu.add_item("attach...", 'choose_parent')
        menu.add_item("duplicate...", 'duplicate')
        menu.add_line()
        menu.add_item("transparency...", 'choose_alpha')
        menu.add_item("resize...", 'resize')
        if not isinstance(self.parent, Frame):
            menu.add_item("adjust position...", 'adjust_position')
        menu.add_item("color...", 'choose_color')
        menu.add_line()
        menu.add_item("hide", 'hide')
        menu.add_item("close", 'delete')
        return menu

    def choose_alpha(self):
        result = self.prompt(self.__class__.__name__ + "\nalpha\nvalue:",
                            str(self.alpha),
                            50)
        if result != None:
            self.alpha = min(max(int(result),0),254)
            self.draw_new()
            self.changed()

    def choose_color(self):
        result = self.pick_color(self.__class__.__name__ + "\ncolor:",
                            self.color)
        if result != None:
            self.color = result
            self.draw_new()
            self.changed()

    def resize(self):
        handle = Resizer(self)
        while self.is_resizing(handle):
            world.do_one_cycle()
        handle.delete()

    def is_resizing(self, handle):
        if world.hand.is_dragging(handle):
            return True
        elif pygame.mouse.get_pressed() != (1,0,0):
            return True
        elif world.hand.morph_at_pointer() is handle:
            return True
        else:
            return False

    def change_extent_to(self, point):
        self.changed()
        self.set_extent(point)
        self.draw_new()
        self.changed()

    def adjust_position(self):
        self.add_shadow()
        p = pygame.mouse.get_pos()
        pos = Point(p[0], p[1])
        offset = pos - self.bounds.origin
#PKHG.? pygame
        while pygame.mouse.get_pressed() == (0,0,0):
            mousepos = pygame.mouse.get_pos()
            self.set_position(Point(mousepos[0], mousepos[1]) - offset)
            world.do_one_cycle()
        self.remove_shadow()

    def choose_parent(self):
        self.choose_morph().add(self)
        self.changed()

    def choose_morph(self):
        self.hint('click on a morph\nto select it')
        while pygame.mouse.get_pressed() == (0,0,0):
            world.do_one_cycle()
        return world.hand.morph_at_pointer()

    #Morph utilities:

    def hint(self, msg):
        m = Menu()
        m.title = msg.__str__()
        m.is_draggable = True
        m.popup_centered_at_hand()

    def inform(self, msg):
        m = Menu()
        m.title = msg.__str__()
        m.add_item("Ok")
        m.is_draggable = True
        m.popup_centered_at_hand()

    def ask_yes_no(self, msg):
        m = SelectionMenu()
        m.title = msg.__str__()
        m.add_item("Yes", True)
        m.add_item("No", False)
        m.is_draggable = True
        return m.get_user_choice()

    def prompt(self, msg, default='', width=100):
        m = SelectionMenu()
        m.title = msg.__str__()
        m.add_entry(default, width)
        m.add_line(2)
        m.add_item("Ok", True)
        m.add_item("Cancel", False)
        m.is_draggable = True
        if m.get_user_choice():
            return m.get_entries()[0]
        else:
            return None

    def pick_color(self, msg, default=(0,0,0,)):
        m = SelectionMenu()
        m.title = msg.__str__()
        m.add_color_picker(default)
        m.add_line(2)
        m.add_item("Ok", True)
        m.add_item("Cancel", False)
        m.is_draggable = True
        if m.get_user_choice():
            return m.get_color_picks()[0]
        else:
            return None
class Frame(Morph):
    " I clip my submorphs at my bounds "

    def full_bounds(self):

        return self.bounds

    def wants_drop_of(self, morph):
        return True

    def full_draw_on(self, surface, rectangle=None):
        if rectangle == None:
            rectangle = self.full_bounds()
        rectangle = rectangle.intersect(self.full_bounds())
        self.draw_on(rectangle)
        for child in self.children:
            child.full_draw_on(surface, self.bounds.intersect(rectangle))

    def developers_menu(self):
        menu = super(Frame, self).developers_menu()
        menu.add_line()
        menu.add_item("move all inside...", 'keep_all_submorphs_within')
        return menu

    def keep_all_submorphs_within(self):
        for m in self.children:
            m.keep_within(self)

class World(Frame):
    "I represent the screen"

    def __init__(self, x=800, y=600):
        super(World, self).__init__()
        self.hand = Hand()
        self.hand.world = self
        self.keyboard_receiver = None
        self.text_cursor = None
        self.bounds = Point(0, 0).corner(Point(x, y))
        self.color = (0.,1.0,1)#(130, 130, 130)
        self.alpha = 0.2 #PKHG
#PKHG.INFO World is a Frames, a Frame  is a Morph, a Morh has color and alpha (yet!)
        self.open_menu = None
        self.is_visible = True
        self.is_draggable = False
        self.is_dev_mode = True
        self.is_quitting = False
        #self.draw_new()
        self.broken = []

    def __repr__(self):
        return 'World(' + self.extent().__str__() + ')'

    def draw_new(self, event):
        draw_rounded_morph(self, small = 0.2)        
        return
        icon = Ellipse().image
        pygame.display.set_icon(icon)
        self.image = pygame.display.set_mode(self.extent().as_list(),
                                             pygame.RESIZABLE)
        pygame.display.set_caption('Morphic')
        self.image.fill(self.color)

    def broken_for(self, morph):
        "private"
        result = []
        fb = morph.full_bounds()
        for r in self.broken:
            if r.intersects(fb):
                result.append(r)
        return result

    def add(self, morph):
        """if isinstance(morph, Menu):
            if isinstance(self.open_menu, Menu):
                self.open_menu.delete()"""
        super(World, self).add(morph)
        self.open_menu = morph

    #World displaying:

    def full_draw_on(self, surface, rectangle=None):
        if rectangle == None:
            rectangle = self.bounds
        if rectangle.extent() > Point(0,0):
            self.image.fill(self.color, rectangle.as_rect())
            for child in self.children:
                child.full_draw_on(surface, rectangle)
            self.hand.full_draw_on(surface, rectangle)



    #World menus:

    def context_menu(self):
        menu = Menu(self, self.__class__.__name__)
        if self.is_dev_mode:
            menu.add_item("create a morph...", 'user_create_new_morph')
            menu.add_line()
            menu.add_item("hide all", 'hide_all')
            menu.add_item("show all", 'show_all_hiddens')
            menu.add_item("move all inside...", 'keep_all_submorphs_within')
            menu.add_item("color...", 'choose_color')
            menu.add_line()
            menu.add_item("stop all bouncers", 'stop_all_bouncers')
            menu.add_item("start all bouncers", 'start_all_bouncers')
            menu.add_line()
            menu.add_item("switch to user mode", 'toggle_dev_mode')
            menu.add_item("close", 'delete')
        else:
            menu.add_item("enter developer's mode", 'toggle_dev_mode')
        menu.add_line()
        menu.add_item("about...", 'about')
        return menu

    def user_create_new_morph(self):
        menu = Menu(self, "create new")
        menu.add_item("rectangle...", 'user_create_rectangle')
        menu.add_item("ellipse...", 'user_create_ellipse')
        menu.add_item("circle box...", 'user_create_circle_box')
        menu.add_item("rounded box...", 'user_create_rounded_box')
        menu.add_item("polygon...", 'user_create_polygon')
        menu.add_line()
        menu.add_item("string...", 'user_create_string')
        menu.add_item("text...", 'user_create_text')
        menu.add_line()
        menu.add_item("bouncer...", 'user_create_bouncer')
        menu.add_item("frame...", 'user_create_frame')
        menu.add_item("palette...", 'user_create_color_palette')
        menu.add_item("slider...", 'user_create_slider')

        menu.popup_at_hand()

    def user_create_rectangle(self):
        Morph().pick_up()

    def stop_all_bouncers(self):
        for m in self.all_children():
            if isinstance(m, Bouncer):
                m.is_stopped = True

    def start_all_bouncers(self):
        for m in self.all_children():
            if isinstance(m, Bouncer):
                m.is_stopped = False

    #World methods:

    def delete(self):
        if self.ask_yes_no("really quit?"):
            self.is_quitting = True

    def toggle_dev_mode(self):
        self.is_dev_mode = not self.is_dev_mode

    def show_all_hiddens(self):
        for morph in self.children:
            if not morph.is_visible:
                morph.show()

    def hide_all(self):
        for morph in self.children:
            morph.hide()

    def pick_up(self):
        pass

    def edit(self, stringMorph):
        if self.text_cursor != None:
            self.text_cursor.delete()
        self.text_cursor = TextCursor(stringMorph)
        stringMorph.parent.add(self.text_cursor)
        self.keyboard_receiver = self.text_cursor

    def stop_editing(self):
        if self.text_cursor != None:
            self.text_cursor.delete()
        self.keyboard_receiver = None

    def about(self):
        self.inform("morphic.py\n\n\
a lively GUI for Python\ninspired by Squeak\nbased on Pygame\n\
" + version + "\n\nwritten by Jens Monig\njens@moenig.org")

    #World utilities:

    def fontname_by_user(self):
        names = sorted(pygame.font.get_fonts())
        choice = ListMenu(names,
                          'choose font').get_user_choice()
        if choice == False:
            return None
        else:
            return choice



    #World events / dragging and dropping:

    def wants_drop_of(self, morph):
        return True

    def handles_mouse_click(self):
        return True

    #World mainloop:

    def loop(self):
        self.full_draw_on()

class Hand(Morph):
    "I represent the mouse cursor"

    def __init__(self):
        super(Hand, self).__init__()
        self.world = None
        self.mouse_over_list = []
        self.mouse_down_morph = None
        self.morph_to_grab = None
        self.moving_morph= False
        self.bounds = Point(0, 0).corner(Point(0,0))

    def __repr__(self):
        return 'Hand(' + self.center().__str__() + ')'

    def attach_to_world(self, world):
        self.world = world

    def changed(self):
        print("\n--dbg pkgh changed called")
        if self.world != None:
            b = self.full_bounds()
            print("--dbg pkhg b = self.full_bounds() extent", b, b.extent())
            if b.extent() != Point(0, 0):
                self.world.broken.append(self.full_bounds())
                print("--dbg pkhg world.broken", self.world.broken[:])

    def draw_on(self, rectangle=None):
        pass

    def process_mouse_event(self, event):
        if event.type == 'MOUSEMOVE':
            return self.process_mouse_move(event)
        elif event.value=='PRESS':
            return self.process_mouse_down(event)
        elif event.value=='RELEASE':
            return self.process_mouse_up(event)

    def morph_at_pointer(self):
        morphs = self.world.children
        for m in morphs[::-1]:
            if m.full_bounds().contains_point(self.bounds.origin) and m.is_visible:
                return m.morph_at(self.bounds.origin)
        return self.world

    def all_morphs_at_pointer(self):
        answer = []
        # morphs = self.world.all_children()
        morphs = self.world.children
        for m in morphs:
            if m.is_visible and (m.full_bounds().contains_point
                                 (self.bounds.origin)):
                answer.append(m)
        return answer

    #Hand dragging and dropping:

    def drop_target_for(self, morph):
        target = self.morph_at_pointer()
        while target.wants_drop_of(morph) == False:
            target = target.parent
        return target
#Hand
    def grab(self, morph):
        if self.children == []:
            self.world.stop_editing()
            self.add(morph)
            self.changed()
            print("morph has been grabbed")

    def drop(self):
        if self.children != []:
            morph = self.children[0]
            target = self.drop_target_for(morph)
            self.changed()
            target.add(morph)
            morph.changed()
            self.morph_to_grab = None
            self.children = []
            self.set_extent(Point(0, 0))

            print("morph has been droped")


    #Hand event dispatching:

    def process_mouse_down(self, event):
        returned_value = {'PASS_THROUGH'}
        if self.children != []:
            self.drop()
        else:
            pos = Point(event.mouse_region_x,
                        event.mouse_region_y)
            morph = self.morph_at_pointer()

            is_menu_click = False

            """for m in morph.all_parents():
                if isinstance(m, Menu) or isinstance(m, Widget):
                    is_menu_click = True
            if not is_menu_click:
                if isinstance(world.open_menu, SelectionMenu):
                    world.open_menu.choice = False
                elif isinstance(world.open_menu, Menu):
                    world.open_menu.delete()

            if world.text_cursor != None:
                if morph is not world.text_cursor.target:
                    world.stop_editing()"""

            self.morph_to_grab = morph.root_for_grab()
            print("self.morph_to_grab : ",self.morph_to_grab )
            if morph.is_draggable:
                self.moving_morph =True
            while not morph.handles_mouse_click():
                morph = morph.parent
            self.mouse_down_morph = morph
            if event.type == 'LEFTMOUSE':
                morph.mouse_down_left(pos)


            elif event.type == 'MIDDLEMOUSE':
                morph.mouse_down_middle(pos)
            elif event.type == 'RIGHTMOUSE':
                morph.mouse_down_right(pos)
            else:
                pass
        return returned_value

    def process_mouse_up(self, event):
        if self.children != []:
            self.drop()
            if self.moving_morph == True:
                    self.moving_morph = False
                    print("movement finished")
        else:
            pos = Point(event.mouse_region_x,
                        event.mouse_region_y)
            morph = self.morph_at_pointer()

            is_menu_click = False
            """for m in morph.all_parents():
                if isinstance(m, Menu) or isinstance(m, Widget):
                    is_menu_click = True"""
            """
            if event.type == 'RIGHTMOUSE' and event.value == 'RELEASE' and not is_menu_click:
                menu = morph.context_menu()
                if menu != None:
                    menu.popup_at_hand()

                    """

            while not morph.handles_mouse_click():
                morph = morph.parent

            if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                morph.mouse_up_left(pos)

                if morph is self.mouse_down_morph:
                    morph.mouse_click_left(pos)

            elif event.type == 'MIDDLEMOUSE' and event.value == 'RELEASE':
                morph.mouse_up_middle(pos)
                if morph is self.mouse_down_morph:
                    morph.mouse_click_middle(pos)
            elif event.type == 'RIGHTMOUSE' and event.value =='RELEASE' and not is_menu_click:
                morph.mouse_up_right(pos)
                if morph is self.mouse_down_morph:
                    morph.mouse_click_right(pos)
            else:
                pass
        return {'PASS_THROUGH'}

    def process_mouse_move(self, event):
        value_returned = {'PASS_THROUGH'}
        mouse_over_new = self.all_morphs_at_pointer()
        if self.children == [] and event.type == 'MOUSEMOVE':
            top_morph = self.morph_at_pointer()
            if top_morph.handles_mouse_move():
                pos = Point(event.mouse_region_x,
                            event.mouse_region_y)
                top_morph.mouse_move(pos)
            morph = top_morph.root_for_grab()
            if morph is self.morph_to_grab and morph.is_draggable:

                self.grab(morph)
                value_returned = {'RUNNING_MODAL'}



        for old in self.mouse_over_list:
            if old not in mouse_over_new :
                old.mouse_leave()
                if event.type == 'MOUSEMOVE':
                    old.mouse_leave_dragging()
                    print("I am dragging the old morph")

        for new in mouse_over_new:
            if new not in self.mouse_over_list:
                new.mouse_enter()
                if event.type == 'MOUSEMOVE':
                    new.mouse_enter_dragging()

            print("I am dragging the  new morph")



        if self.children != [] and event.type == 'MOUSEMOVE' and self.moving_morph == True:
            self.morph_to_grab.set_position(self.bounds.origin)
            print("WARNING !!!! morph move : ",self.morph_to_grab)
            value_returned = {'RUNNING_MODAL'}
        self.mouse_over_list = mouse_over_new
        return value_returned

    #Hand testing:

    def is_dragging(self, morph):
        if self.children != []:
            return morph is self.children[0]
        else:
            return False

    
class RoundedBox(Morph):

#    def __init__(self, edge=4, border=2, bordercolor=pygame.Color(0,0,0)):
    def __init__(self, edge=4, border=20, bordercolor=(0,0,0), alpha = .7, bot_left = Point(0,0), top_right = Point(100,100)):
        super(RoundedBox, self).__init__()
        self.bounds = bot_left.corner(top_right)
        self.edge = edge
        self.border = border
        self.bordercolor = bordercolor        
        self.alpha = alpha #PKHG.ADDED
        print("RoundedBox created")
        
    def draw_new(self, event):
#        self.image = pygame.Surface(self.extent().as_list())
#        self.image.set_colorkey(TRANSPARENT)
#        self.image.set_alpha(self.alpha)
#        self.image.fill(TRANSPARENT)
        self.fill_rounded(max(self.edge - (self.border // 2),0),
                          self.color, self.border)

        self.fill_rounded(self.edge, self.bordercolor, 0)
#PKHG.means no inset black color if not changed at creation-time

    def fill_rounded(self, edge, color, inset):        
        "private"
        print("fill rounded color = ", color, " inset = ",  inset)
        if inset == 0:
            draw_rounded_morph(self, small = 0.05, color = color, alpha = self.alpha)
        else:
            rect = self.bounds.inset_by(inset)
            draw_rounded_morph(rect, small = 0.1, rectangle=True, color=(0,0,1), alpha = 1)

    #RoundedBox menu:

    def developers_menu(self):
        menu = super(RoundedBox, self).developers_menu()
        menu.add_line()
        menu.add_item("border color...", 'choose_border_color')
        menu.add_item("border size...", 'choose_border')
        menu.add_item("corner size...", 'choose_edge')
        return menu

    def choose_border(self):
        result = self.prompt("border:",
                            str(self.border),
                            50)
        if result != None:
            self.changed()
            self.border = min(max(int(result),0),self.width()//3)
            self.draw_new()
            self.changed()

    def choose_edge(self):
        result = self.prompt("corner:",
                            str(self.edge),
                            50)
        if result != None:
            self.changed()
            self.edge = min(max(int(result),0),self.width()//3)
            self.draw_new()
            self.changed()

    def choose_border_color(self):
        result = self.pick_color(self.__class__.__name__ + "\nborder color:",
                            self.bordercolor)
        if result != None:
            self.bordercolor = result
            self.draw_new()
            self.changed()

def ellipsePoint(center, a, b, t):
    t = radians(t)
    x = a * cos(t)
    y = b * sin(t)
    Pt = Point(x,y)
    return center + Pt

def draw_rounded_morph(morph, small = 0.1, rectangle = False , color=(0,0,0), alpha = 1 ):
    def rounded_corners(cornerPT, offset,  NSEW, a):
#        print("\n === dbg ronded corn", cornerPT, offset, NSEW, a)
        point_list = []
        numb = 10 
        fac = 90./numb
        tvals = [NSEW +  el * fac  for el in range(numb +1)]
        midPt = cornerPT + offset
        for t  in tvals:
            res = ellipsePoint(midPt,a,a,t)
            point_list.append(res)
        return point_list
        
    if debug_world and not rectangle and  morph.name == "World":
        print("\n======DBG my name is", morph.name, " my color is", morph.color, morph.alpha)
    small = abs(small)
    if rectangle:
        bounds = morph
    else:
        bounds = morph.bounds
    PNW = bounds.top_left()
    PZW = bounds.bottom_left()
    PZE = bounds.bottom_right()
    PNE = bounds.top_right()
    disUp = PNW.distance_to(PZW)
    disSide = PZW.distance_to(PZE)
    a = min(disUp, disSide) * small

    offset = Point(a, a)
    draw_all_points = []
#    print("\n====DBG PZW, offset", PZW, offset)
    draw_all_points.extend(rounded_corners(PZW, offset,  180, a))
    offset = Point(-a, a)
    draw_all_points.extend( rounded_corners(PZE, offset, 270, a))
    offset = Point(-a, -a)
    draw_all_points.extend(rounded_corners(PNE, offset, 0, a))
    offset = Point(a , -a)
    draw_all_points.extend(rounded_corners(PNW, offset, 90, a))
    draw_all_points.append(draw_all_points[0]) #top to end!
    bgl.glEnable(bgl.GL_BLEND) #PKHG.??? needed??? YES!!!
    if rectangle:
        bgl.glColor4f(color[0], color[1], color[2], alpha)
    else:
        bgl.glColor4f(morph.color[0], morph.color[1], morph.color[2], morph.alpha)
    bgl.glBegin(bgl.GL_POLYGON)

#PKHG works for Morph    bgl.glColor4f(1, 1, 0, .5)
#    if morph.name == "World":
#        print("\n=======dBG color set =", morph.color[0], morph.color[1], morph.color[2], morph.alpha)
    for el in draw_all_points:
        bgl.glVertex2f(el.x,el.y)
    bgl.glEnd()
    return

def DrawStringToViewport(text, morph, size, color, font_id, x, y):
    ''' my_string : the text we want to print
        pos_x, pos_y : coordinates in integer values
        size : font height.
        colour_type : used for definining the colour'''
#    my_dpi, font_id = 72, 0 # dirty fast assignment
#
    bgl.glColor4f(*color)
#    x = morph.bounds.origin.x 
#    xx = morph.bounds.corner.x
#    difx = xx - x
#PKHG. make it a parameter    y = morph.bounds.corner.y - size
#    dimsx, dimsy = blf.dimensions(font_id,text)
#    print("\ndbg before dims = ", dimsx, dimsy, difx, morph.name)
    blf.position(font_id, x, y, 0)
#    if dimsx > difx:
#        size *= difx/dimsx
#        size = int(size)
#    blf.size(font_id, size, my_dpi)
#    dims = blf.dimensions(font_id,text)
#    print("\ndbg after dims = ", dims)
    blf.draw(font_id, text)



class Text(Morph):
    "I am a mult line, word wrapping string"

    def __init__(self,
                 text,
                 fontname="verdana",
                 fontsize=24,
                 bold=False,
                 italic=False,
                 alignment='left',
#PKHG.INFO a real Text nees a with > 0 !!!
                 max_width=200):
#        pygame.font.init()
#PKHG.TODO or always only font_id = 0 the default??
#PKHG.works        self.font = blf.load("c:/Windows/Fonts/Verdana.ttf")
#        self.font = blf.load("c:/Windows/Fonts/Verdana.ttf") #this works
#no becomes bigger than it should        self.font = blf.load("c:/Windows/Fonts/arialbd.ttf")
#        self.font = blf.load("c:/Windows/Fonts/arial.ttf") #this works
#        self.font = blf.load("c:/Windows/Fonts/baln.ttf") #this works but too small
        self.font = blf.load("c:/Windows/Fonts/bod_b.ttf") #this works but too small
        blf.size(self.font, fontsize, 72) #DPI = 72 !!
        self.background_color = (0,0,0)
        self.text = text
        self.words = []
        self.fontname = fontname
        self.fontsize = fontsize
        self.bold = bold
        self.italic = italic
        self.alignment=alignment
#PKHG.??? is complicated   20<= max_width <= world width
        self.max_width = max(20, min(max_width, 800))
        super(Text, self).__init__()
        self.color = (1,1,1) # PKHG.???BLACK pygame.Color(0,0,0)
#PKHG.not yet        self.draw_new()
        self.max_line_width = 0
        self.lines = []
#PKHG>???        
        self.parse() #once?!
        print("\n text init after parse ============lines============",self.lines)
#        w = blf.dimensions(self.font,"Af")
#        hight_line = round(w[1] + 1.51)
        nr_of_lines = len(self.lines)
        print("nr_of_lines", nr_of_lines)
        res = ""
        for el in self.lines:
            print(el)
            if len(el) > len(res):
                res = el
        blf.size(self.font, fontsize, 72) #DPI = 72 !!
        w = blf.dimensions(self.font, res)
        print("res =  and w max_line_width", res, w, self.max_line_width)
        hight_line = round(w[1] + 1.51)
        print("Text init nr of lines, w",nr_of_lines, w)
        wi,hei = int(max(self.max_line_width, w[0]+2)), nr_of_lines * hight_line        
        self.bounds = Point(0,0).corner(Point(wi, hei ))
        print("size of text", self.bounds)


    def __repr__(self):
        return 'Text("' + self.text + '")'

    def parse(self):    
#        print("\n===++++++444444444++++++++DBG parse L1508 w" , self.font, blf.dimensions(self.font,"PKHG "))
        self.words = []
        paragraphs = self.text.splitlines()
        self.max_line_width = 0
        for p in paragraphs:
            self.words.extend(p.split(' '))
            self.words.append('\n')
        '''
        self.font = pygame.font.SysFont(
            self.fontname,
            self.fontsize,
            self.bold,
            self.italic)
        '''
        self.lines = []
        oldline = ''
        for word in self.words:
            if word == '\n':
                self.lines.append(oldline)
#                self.max_line_width = max(self.max_line_width,
#                                          self.font.size(oldline)[0])
                w = blf.dimensions(self.font,oldline)
                self.max_line_width = max(self.max_line_width, w[0])
                oldline = ''
            else:
                if self.max_width > 0:
                    newline = oldline + word + ' '
#                    w = self.font.size(newline)
                    w = blf.dimensions(self.font, newline)                    
                    if w[0] > self.max_width:
                        self.lines.append(oldline)
                        w = blf.dimensions(self.font, oldline)
#                        self.max_line_width = max(self.max_line_width,
#                                                    self.font.size(oldline)[0])
                        self.max_line_width = max(self.max_line_width, w[0])
                        oldline = word + ' '
                    else:
                        oldline = newline
                else:
                    oldline = oldline + word + ' '
        print("\n---DBG L1569 parse text, max_line_width", self.max_line_width)
#Text ...    
    def draw_new(self, event):
#PKHG.??? it is a morph!        surfaces = []
        print("\n\n++++++++++++++++++ text draw new called")
        tmp = self.bounds
        x = self.bounds.origin.x
        y = self.bounds.origin.y
        xx = self.bounds.corner.x
        yy = self.bounds.corner.y 
        hei = yy - y
        nr = len(self.lines)
        lineHei = hei // nr 
        colo = self.color
        color = (colo[0],colo[1],colo[2],1)
        bgcol = self.background_color
        bgl.glEnable(bgl.GL_BLEND) #PKHG. needed for color of rectangle!
        bgl.glColor4f(bgcol[0], bgcol[1], bgcol[2] ,0.1) 
        dime = self.extent().as_list()
        bgl.glRecti(self.position().x, self.position().y, self.position().x + dime[0], self.position().y + dime[1])
        for el in range(nr):
            DrawStringToViewport(self.lines[el], self,24, color, self.font, x, yy - lineHei  - el * lineHei)
        return
    
    #Text menu:

    def developers_menu(self):
        menu = super(Text, self).developers_menu()
        menu.add_line()
        menu.add_item("edit contents...", 'edit_contents')
        menu.add_item("font name...", 'choose_font')
        menu.add_item("font size...", 'choose_font_size')
        menu.add_item("background...", 'choose_background_color')
        menu.add_line()
        if self.bold or self.italic:
            menu.add_item("normal", 'set_to_normal')
        if not self.bold:
            menu.add_item("bold", 'set_to_bold')
        if not self.italic:
            menu.add_item("italic", 'set_to_italic')
        menu.add_line()
        if not self.alignment == 'left':
            menu.add_item("align left", 'set_alignment_to_left')
        if not self.alignment == 'center':
            menu.add_item("centered", 'set_alignment_to_center')
        if not self.alignment == 'right':
            menu.add_item("align right", 'set_alignment_to_right')
        return menu

    def choose_font(self):
        fontname = world.fontname_by_user()
        if fontname != None:
            self.fontname = fontname
            self.changed()
            self.draw_new()
            self.changed()

    def choose_font_size(self):
        fontsize = self.prompt("please enter\n the font size\nin points:",
                               str(self.fontsize),
                               50)
        if fontsize != None:
            self.fontsize = int(fontsize)
            self.changed()
            self.draw_new()
            self.changed()

    def choose_background_color(self):
        result = self.pick_color(self.__class__.__name__ + "\nbackground:",
                            self.background_color)
        if result != None:
            self.background_color = result
            self.draw_new()
            self.changed()

    def edit_contents(self):
        text = self.prompt("edit contents\nof text field:",
                               self.text,
                               400)
        if text != None:
            self.text = text
            self.changed()
            self.draw_new()
            self.changed()

    def set_alignment_to_left(self):
        self.set_alignment('left')

    def set_alignment_to_right(self):
        self.set_alignment('right')

    def set_alignment_to_center(self):
        self.set_alignment('center')

    def set_alignment(self, alignment):
        self.alignment = alignment
        self.draw_new()
        self.changed()

    def set_to_normal(self):
        self.bold = False
        self.italic = False
        self.changed()
        self.draw_new()
        self.changed()

    def set_to_bold(self):
        self.bold = True
        self.changed()
        self.draw_new()
        self.changed()

    def set_to_italic(self):
        self.italic = True
        self.changed()
        self.draw_new()
        self.changed()

    def change_extent_to(self, point):
        self.changed()
        self.max_width = point.x
        self.draw_new()
        self.changed()


