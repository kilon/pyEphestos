

import bgl
import copy
import math
version = '2009-Nov-06'
TRANSPARENT = 0

class Point:
    """ Point Class , defining the behavior of points """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        "representation of Point Class"
        return self.x.__str__() + '@' + self.y.__str__()

    #Point comparison:

    def __eq__(self, other):
        "getter: (point1 , point2) are the two points equal  ? "
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __ne__(self, other):
        "getter: (point1 , point2) are the two points not equal ?"
        return not self.__eq__(other)

    def __lt__(self, other):
        "getter: (point1 , point2) are the first point less than the second point ?"
        if isinstance(other, Point):
            return self.x < other.x and self.y < other.y
        return NotImplemented

    def __gt__(self, other):
        "getter: (point1 , point2) is the first point greater than the second point ?"
        if isinstance(other, Point):
            return self.x > other.x and self.y > other.y
        return NotImplemented

    def __le__(self, other):
        "getter: (point1 , point2) is the first point equal or less than second point ?"
        if isinstance(other, Point):
            return self.x <= other.x and self.y <= other.y
        return NotImplemented

    def __ge__(self, other):
        "getter: (point1 , point2) is the first point equal or greater than the second point ?"
        if isinstance(other, Point):
            return self.x >= other.x and self.y >= other.y
        return NotImplemented

    def __round__(self):
        "getter: (point1 , point2) return the round of the point "
        return Point(round(self.x), round(self.y))

    def max(self, other):
        "getter: (point1 , point2) return the max between 2 points"
        return Point(max(self.x, other.x), max(self.y, other.y))
    
    def min(self, other):
        "getter: (point1 , point2) return the min between 2 points"
        return Point(min(self.x, other.x), min(self.y, other.y))

    #Point arithmetic:

    def __add__(self, other):
        "getter: (point1 , point2) add 2 points and return the result"
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        return Point(self.x + other, self.y + other)
        
    def __sub__(self, other):
        "getter: (point1 , point2) substract 2 points and return the result"
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        return Point(self.x - other, self.y - other)

    def __mul__(self, other):
        "getter: (point1 , point2) perform a mulitplication of 2 points and return the result"
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y)
        return Point(self.x * other, self.y * other)

    def __div__(self, other):
        "getter: (point1 , point2) perform a division of 2 points and return the result"
        if isinstance(other, Point):
            return Point(self.x / other.x, self.y / other.y)
        return Point(self.x / other, self.y / other)

    def __floordiv__(self, other):
        "getter: (point1 , point2) perform a floor division of 2 points and return the result"
        if isinstance(other, Point):
            return Point(self.x // other.x, self.y // other.y)
        return Point(self.x // other, self.y // other)

    def __abs__(self):
        return Point(abs(self.x), abs(self.y))

    def __neg__(self):
        "getter: return the negative of a point"
        return Point(-self.x, -self.y)

    #Point functions:

    def dot_product(self, other):
        "getter: (point1 , point2) return the dot product"
        return self.x * other.x + self.y * other.y
    
    def cross_product(self, other):
        "getter: (point1 , point2) return the cross product"
        return self.x * other.y - self.y * other.x

    def distance_to(self, other):
        "getter: (point1 , point2) return the distance between 2 points"
        return (other - self).r()

    def rotate(self, direction, center):
        "getter: (direction, center) rotate a point realtive to a center with a specific direction and return the result. direction must be 'right', 'left' or 'pi'"
        offset = self - center
        if direction == 'right':
            return Point(-offset.y, offset,y) + center
        elif direction == 'left':
            return Point(offset.y, -offset.y) + center
        elif direction == 'pi':
            return center - offset
        else:
            return NotImplemented
    
    def flip(self, directon, center):
        " getter: (direction , center) flip a point to a direction relative to a center and return the result. The direction can be either vertical or horizontal, of string typ"

        if direction == 'vertical':
            return Point(self.x, center.y * 2 - self.y)
        elif direction == 'horizontal':
            return Point(center,x * 2 - self.x, self.y)
        else:
            return NotImplemented

    #Point polar coordinates:

    def r(self):
        "getter: return polar cordinates"
        return math.sqrt(self.dot_product(self))

    #Point transforming:

    def scale_by(self, scalePoint):
        "getter: (point) scale the point by another point and return the result"
        return Point(scalePoint.x * self.x, scalePoint.y * self.y)

    def translate_by(self, deltaPoint):
        "getter: (point) perform a mulitplication of 2 points and return the result"
        return Point(deltaPoint.x + self.x, deltaPoint.y + self.y)

    #Point converting:

    def as_list(self):
        "getter:  return point coordinates (x,y) as a list"
        return [self.x, self.y]

    def corner(self, cornerPoint):
        "getter: (point) return a rectangle between the point and another point"
        return Rectangle(self, cornerPoint)

    def rectangle(self, aPoint):
        "getter: (point) return a rectangle between the point and another point using min and max"
        return Rectangle(self.min(aPoint), self.max(aPoint))

    def extent(self, extentPoint):
        "getter: (point) return a rectangle between the point and another point taking the new point as an extension"
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
            return max(w * self.height, 0)

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
            return Rectangle(self.origin + delta.origin)
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

"""
    #Rectangle converting:

    def as_rect(self):
        return pygame.Rect(self.left(),
                           self.top(),
                           self.width(),
                           self.height())
"""

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
        self.color = (0.3, 0.3,  0.3, 1)
        self.alpha = 1 
        self.is_visible = True
        self.is_draggable = True
        self.draw_new()
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


    """def step_frame(self):
        if not self.wants_to_step():
            return
        current = pygame.time.get_ticks()
        elapsed = current - self.last_time
        if self.fps > 0:
            leftover = (1000 // self.fps) - elapsed
        else:
            leftover = 0
        if leftover < 1:
            self.last_time = current
            self.step()
            for child in self.children:
                child.step_frame()"""


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
        """
        self.image = pygame.Surface(self.extent().as_list())
        self.image.fill(self.color)
        self.image.set_alpha(self.alpha)
        """
        bgl.glColor4f(self.colort,self, self.alpha)
        bgl.glRecti(self.extent().as_list())
        
        
    def draw_on(self, surface, rectangle=None):
        if not self.is_visible:
            return
        if rectangle == None:
            rectangle = self.bounds
        area = rectangle.intersect(self.bounds)
        if area.extent() > Point(0,0):
            p = area.origin.as_list()
            area.origin = area.origin - self.bounds.origin
            area.corner = area.corner - self.bounds.origin
            surface.blit(self.image, p, area.as_rect())

    def full_draw_on(self, surface, rectangle=None):
        if not self.is_visible:
            return
        if rectangle == None:
            rectangle = self.full_bounds()
        self.draw_on(surface, rectangle)
        for child in self.children:
            child.full_draw_on(surface, rectangle)

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

    #Morph conversion:

    def full_surface(self):
        img = pygame.Surface(self.full_bounds().extent().as_list())
        img.fill(TRANSPARENT)
        img.set_colorkey(TRANSPARENT)
        img.set_alpha(self.alpha)
        for morph in self.all_children():
            pos = morph.position() - self.position()
            img.blit(morph.image, pos.as_list())
        return img
        img = pygame.Surface(self.full_bounds().extent().as_list())

    def shadow_surface(self, offset, alpha):
        img = self.full_surface()
        tmp = pygame.Surface(self.full_bounds().extent().as_list())
        sha = pygame.Surface(self.full_bounds().extent().as_list())
        pygame.transform.threshold(tmp, img, (1,1,1))
        tmp.blit(img, (-offset).as_list())
        pygame.transform.threshold(sha, tmp, (0,0,0),(0,0,0), (1,1,1))
        sha.set_colorkey(TRANSPARENT)
        sha.set_alpha(alpha)
        return sha

    def shadow(self, offset, alpha):
        shadow = Shadow()
        shadow.set_extent(self.full_bounds().extent())
        shadow.draw_new()
        shadow.image = self.shadow_surface(offset, alpha)
        shadow.set_position(self.position() + offset)
        return shadow

    def add_shadow(self, name="shadow", offset=Point(7,7), alpha=50):
        shadow = self.shadow(offset, alpha)
        shadow.name = name
        self.add(shadow)
        self.full_changed()

    def get_shadow(self):
        for child in self.children[::-1]:
            if isinstance (child, Shadow):
                return child
        return None
    
    def remove_shadow(self):
        self.full_changed()
        shadow = self.get_shadow()
        if shadow != None:
            self.remove_child(shadow)

    #Morph updating:

    def changed(self):
        w = self.root()
        if isinstance(w, World):
            w.broken.append(copy.copy(self.bounds))

    def full_changed(self):
        w = self.root()
        if isinstance(w, World):
            w.broken.append(copy.copy(self.full_bounds()))

    #Morph accessing - structure:

    def world(self):
        if isinstance(self.root(), World):
            return self.root()

    def add(self, morph):
        parent = morph.parent
        if parent is not None:
            parent.remove_child(morph)
        self.add_child(morph)

    def morph_at(self, point):
        morphs = self.all_children()
        for m in morphs[::-1]:
            if m.full_bounds().contains_point(point) and not(
                isinstance(m, Shadow)):
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

    def pick_color(self, msg, default=pygame.Color(0,0,0,)):
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

class Resizer(Morph):

    def __init__(self, target=None):
        self.target = target
        super(Resizer, self).__init__()
        self.is_draggable = False
        self.color = TRANSPARENT
        self.set_extent(Point(15,15))
        self.draw_new()

    def draw_new(self):
        super(Resizer, self).draw_new()
        self.image.set_colorkey(TRANSPARENT)
        p1 = self.bottom_left() - self.position()
        p2 = self.top_right() - self.position()
        for offset in range(0,5):
            p1 += Point(3, 0)
            p2 += Point(3, 0)
            pygame.draw.line(self.image,
                             pygame.Color(0,0,0),
                             p1.as_list(),
                             p2.as_list(),
                             2)
        p1 = self.bottom_left() - self.position()
        p2 = self.top_right() - self.position()
        for offset in range(1,6):
            p1 += Point(3, 0)
            p2 += Point(3, 0)
            pygame.draw.line(self.image,
                             pygame.Color(128,128,128),
                             p1.as_list(),
                             p2.as_list(),
                             1)
        self.set_position(self.target.bottom_right() - self.extent())
        self.target.add(self)
        self.target.changed()

    def root_for_grab(self):
        return self

    def handles_mouse_click(self):
        return True

    def mouse_down_left(self, pos):
        offset = pos - self.bounds.origin
        while pygame.mouse.get_pressed() == (1,0,0):
            mousepos = pygame.mouse.get_pos()
            self.set_position(Point(mousepos[0], mousepos[1]) - offset)
            self.target.change_extent_to(self.bottom_right()
                                         - self.target.bounds.origin)
            world.do_one_cycle()

class Blinker(Morph):
    "can be used for text cursors"

    def __init__(self, rate=2):
        super(Blinker, self).__init__()
        self.color = pygame.Color(0,0,0,)
        self.fps = rate
        self.draw_new()

    def wants_to_step(self):
        return True

    def step(self):
        self.toggle_visibility()

class Shadow(Morph):

    def __init__(self):
        super(Shadow, self).__init__()

class Widget(Morph):
    
    def __init__(self):
        super(Widget, self).__init__()

class ColorPalette(Morph):

    def __init__(self, target=None, size=Point(80,50)):
        super(ColorPalette, self).__init__()
        self.target = target
        self.set_extent(size)
        self.choice = None
        self.draw_new()

    def draw_new(self):
        "initialize my surface"
        self.image = pygame.Surface(self.extent().as_list())
        self.image.set_alpha(self.alpha)
        self.image.lock()
        ext_x = self.extent().x
        ext_y = self.extent().y
        y2 = ext_y // 2
        choice = pygame.Color(255,255,255)
        for x in range(0,ext_x):
            h = int(360 * x / ext_x)
            clr = pygame.Color(0,0,0)
            for y in range(0,y2):
                s = int(100 * y / y2)
                clr.hsva = (h,s,100,100)
                self.image.set_at((x,y), clr)
            for y in range(y2, ext_y):
                v = 100 - int(100 * (y - y2) / y2)
                clr.hsva = (h,100,v,100)
                self.image.set_at((x,y), clr)
        self.image.unlock()

    def color_at(self, pos):
        if self.bounds.contains_point(pos):
            return self.image.get_at((pos - self.bounds.origin).as_list())
        else:
            return self.choice

    def handles_mouse_click(self):
        return True

    def handles_mouse_move(self):
        return True

    def mouse_down_left(self, pos):
        self.choice = self.color_at(pos)
        self.update_target()

    def mouse_move(self, pos):
        self.choice = self.color_at(pos)
        self.update_target()

    def update_target(self):
        if isinstance(self.target, Morph) and self.choice != None:
            self.target.color = self.choice
            self.target.draw_new()
            self.target.changed()

    def developers_menu(self):
        menu = super(ColorPalette, self).developers_menu()
        for item in menu.items:
            if item[1] == 'choose_color':
                menu.items.remove(item)
        menu.add_line()
        menu.add_item("show color...", 'show_color')
        menu.add_item("set target...", 'choose_target')
        return menu

    def show_color(self):
        self.inform(self.choice)

    def choose_target(self):
        self.target = self.choose_morph()
        self.update_target()
        self.is_draggable = False

class GrayPalette(ColorPalette):

    def draw_new(self):
        "initialize my surface"
        self.image = pygame.Surface(self.extent().as_list())
        self.image.set_alpha(self.alpha)
        self.image.lock()
        for x in range(0,self.extent().x):
            c = int(256 * x / self.extent().x)
            clr = pygame.Color(c,c,c)
            for y in range(0,self.extent().y):
                self.image.set_at((x,y), clr)
        self.image.unlock()

class ColorPicker(Widget):

    def __init__(self, default=pygame.Color(255,255,255)):
        self.choice=default
        super(ColorPicker, self).__init__()
        self.color = pygame.Color(255,255,255)
        self.set_extent(Point(80,80))
        self.draw_new()

    def draw_new(self):
        super(ColorPicker, self).draw_new()
        self.build_submorphs()

    def build_submorphs(self):
        for m in self.children:
            m.delete()
        self.children = []
        self.feedback = Morph()
        self.feedback.set_extent(Point(20,20))
        self.feedback.color = self.choice
        self.feedback.draw_new()
        cpal = ColorPalette(self.feedback, Point(self.width(), 50))
        gpal = GrayPalette(self.feedback, Point(self.width(),5))
        cpal.set_position(self.bounds.origin)
        self.add(cpal)
        gpal.set_position(cpal.bottom_left())
        self.add(gpal)
        x = (gpal.left() + ((gpal.width() - self.feedback.width()) // 2))
        y = gpal.bottom() + ((self.bottom()
                                - gpal.bottom()
                                - self.feedback.height())
                                // 2)
        self.feedback.set_position(Point(x,y))
        self.add(self.feedback)

    def get_choice(self):
        return self.feedback.color

    def root_for_grab(self):
        return self
        
class Ellipse(Morph):

    def draw_new(self):
        "private initialize my surface"
        self.image = pygame.Surface(self.extent().as_list())
        self.image.set_colorkey(TRANSPARENT)
        self.image.set_alpha(self.alpha)
        self.image.fill(TRANSPARENT)
        pygame.draw.ellipse(self.image,
                            self.color,
                            (Point(0,0,).corner(self.extent())).as_rect(),
                            0)
    
class Polygon(Morph):

    def __init__(self, vertices=None):
        self.set_vertices(vertices)
        super(Polygon, self).__init__()
        self.change_extent_to(self.shape_extent)

    def set_vertices(self, vertices):
        self.vertices = vertices
        self.shape = self.relative_vertices()
        self.shape_extent = self.rectangle(self.shape).extent()
        
    def rectangle(self, pointlist):
        "private - answer my bounds from the vertices"
        minpoint = maxpoint = self.vertices[0]
        for p in self.vertices:
            minpoint = minpoint.min(p)
            maxpoint = maxpoint.max(p)
        return minpoint.corner(maxpoint)

    def relative_vertices(self):
        result = []
        r = self.rectangle(self.vertices)
        for p in self.vertices:
            result.append(p - r.origin)
        return result

    def draw_new(self):
        "initialize my surface"
        rect = self.rectangle(self.vertices)
        self.image = pygame.Surface(rect.extent().as_list())
        self.image.fill(TRANSPARENT)
        plist = []
        for p in self.vertices:
            plist.append((p - rect.origin).as_list())
        pygame.draw.polygon(self.image, self.color, plist, 0)
        self.image.set_colorkey(TRANSPARENT)
        self.image.set_alpha(self.alpha)
        self.bounds = rect.translate_by(self.bounds.origin)

    def change_extent_to(self, point):
        pt = Point(max(point.x,1), max(point.y,1))
        scale = pt.__div__(self.shape_extent)
        self.vertices = []
        for p in self.shape:
            self.vertices.append(p.scale_by(scale))
        self.changed()
        self.draw_new()
        self.changed()

    def developers_menu(self):
        menu = super(Polygon, self).developers_menu()
        menu.add_line()
        menu.add_item("add vertice...", 'user_add_vertice')
        if len(self.vertices) > 3:
            menu.add_item("remove vertice...", 'user_remove_vertice')
        return menu

    def user_remove_vertice(self):
        m = SelectionMenu()
        m.title = 'remove:'
        idx = 0
        for v in self.vertices:
            m.add_item(v.__str__(), idx)
            idx += 1
        m.add_line()
        m.add_item("Cancel", False)
        m.is_draggable = True
        choice = m.get_user_choice()
        if choice != False:
            self.changed()
            self.vertices.pop(choice)
            self.set_vertices(self.vertices)
            self.draw_new()
            self.changed()

    def user_add_vertice(self):
        while pygame.mouse.get_pressed() == (0,0,0):
            world.do_one_cycle()
        mousepos = pygame.mouse.get_pos()
        self.changed()
        self.vertices.append(Point(mousepos[0], mousepos[1]) - self.bounds.origin)
        self.set_vertices(self.vertices)
        self.draw_new()
        self.changed()

class CircleBox(Morph):
    " I can be used for sliders "

    def __init__(self):
        super(CircleBox, self).__init__()
        self.set_extent(Point(20, 100))
        self.draw_new()

    def auto_orientation(self):
        if self.height() > self.width():
            self.orientation = 'vertical'
        else:
            self.orientation = 'horizontal'
        
    def draw_new(self):
        self.auto_orientation()
        self.image = pygame.Surface(self.extent().as_list())
        self.image.set_colorkey(TRANSPARENT)
        self.image.set_alpha(self.alpha)
        self.image.fill(TRANSPARENT)
        if self.orientation == 'vertical':
            radius = self.width() // 2
            x = self.center().x
            center1 = Point(x, self.top() + radius)
            center2 = Point(x, self.bottom() - radius)
            rect = (self.bounds.origin + Point(0, radius)).corner(
                self.bounds.corner - Point(0, radius))
        else:
            radius = self.height() // 2
            y = self.center().y
            center1 = Point(self.left() + radius, y)
            center2 = Point(self.right() - radius, y)
            rect = (self.bounds.origin + Point(radius, 0)).corner(
                self.bounds.corner - Point(radius, 0))
        points = (center1 - self.bounds.origin,
                  center2 - self.bounds.origin)
        for center in points:
            pygame.draw.circle(
                self.image,
                self.color,
                center.as_list(),
                radius,
                0)
        pygame.draw.rect(
            self.image,
            self.color,
            rect.translate_by(-self.bounds.origin).as_rect(),
            0)

    #CircleBox menu:

    def developers_menu(self):
        menu = super(CircleBox, self).developers_menu()
        menu.add_line()
        if self.orientation == 'vertical':
            menu.add_item("horizontal", 'toggle_orientation')
        else:
            menu.add_item("vertical", 'toggle_orientation')
        return menu

    def toggle_orientation(self):
        self.changed()
        if self.orientation == 'vertical':
            self.orientation = 'horizontal'
        else:
            self.orientation = 'vertical'
        center = self.center()
        self.set_extent(Point(self.height(), self.width()))
        self.set_center(center)
        self.draw_new()
        self.changed()

class SliderButton(CircleBox):

    def __init__(self):
        self.orientation = 'vertical'
        super(SliderButton, self).__init__()

    def auto_orientation(self):
        pass

    def draw_new(self):
        super(SliderButton, self).draw_new()
        if self.orientation == 'vertical':
            if self.height() > 8 and self.width() > 4:
                p1 = Point(2, self.center().y - self.top() - 7)
                p2 = Point(self.width() - 4, self.center().y - self.top() - 7)
                for offset in range(0,3):
                    p1 += Point(0, 3)
                    p2 += Point(0, 3)
                    pygame.draw.line(self.image,
                                     pygame.Color(0,0,0),
                                     p1.as_list(),
                                     p2.as_list(),
                                     2)
                p1 = Point(2, self.center().y - self.top() - 7)
                p2 = Point(self.width() - 4, self.center().y - self.top() - 7)
                for offset in range(1,4):
                    p1 += Point(0, 3)
                    p2 += Point(0, 3)
                    pygame.draw.line(self.image,
                                     pygame.Color(128,128,128),
                                     p1.as_list(),
                                     p2.as_list(),
                                     1)
        else:
            if self.width() > 8 and self.height() > 4:
                p1 = Point(self.center().x - self.left() - 7, 2 )
                p2 = Point(self.center().x - self.left() - 7, self.height() - 4)
                for offset in range(0,3):
                    p1 += Point(3, 0)
                    p2 += Point(3, 0)
                    pygame.draw.line(self.image,
                                     pygame.Color(0,0,0),
                                     p1.as_list(),
                                     p2.as_list(),
                                     2)
                p1 = Point(self.center().x - self.left() - 7, 2 )
                p2 = Point(self.center().x - self.left() - 7, self.height() - 4)
                for offset in range(1,4):
                    p1 += Point(3, 0)
                    p2 += Point(3, 0)
                    pygame.draw.line(self.image,
                                     pygame.Color(128,128,128),
                                     p1.as_list(),
                                     p2.as_list(),
                                     1)

class Slider(CircleBox):

    def __init__(self, start=1, stop=100, value=50, size=10):
        self.start=start
        self.stop=stop
        self.value=value
        self.size=size
        self.button = SliderButton()
        self.button.color = pygame.Color(200,200,200)
        self.button.is_draggable = False
        self.orientation = 'vertical'
        super(Slider, self).__init__()
        self.add(self.button)
        self.alpha = 80
        self.color = pygame.Color(0,0,0)
        self.draw_new()

    def auto_orientation(self):
        pass

    def range_size(self):
        return self.stop - self.start

    def ratio(self):
        return self.size / self.range_size()

    def unit_size(self):
        if self.orientation == 'vertical':
            return self.height() / self.range_size()
        else:
            return self.width() / self.range_size()

    def draw_new(self):
        super(Slider, self).draw_new()
        self.button.orientation = self.orientation
        if self.orientation == 'vertical':
            bw = self.width()
            bh = max(bw, self.height() * self.ratio())
            self.button.set_extent(Point(int(bw),int(bh)))
            pos_x = 0
            pos_y = min(int(self.value * self.unit_size()),
                        self.height() - self.button.height())
        else:
            bh = self.height()
            bw = max(bh, self.width() * self.ratio())
            self.button.set_extent(Point(int(bw),int(bh)))
            pos_y = 0
            pos_x = min(int(self.value * self.unit_size()),
                        self.width() - self.button.width())
        self.button.set_position(Point(pos_x, pos_y) + self.bounds.origin)
        self.button.draw_new()
        self.button.changed()

    def update_value(self):
        if self.orientation == 'vertical':
            rel_pos = self.button.top() - self.top()
        else:
            rel_pos = self.button.left() - self.left()
        self.value = rel_pos / self.unit_size()

    def handles_mouse_click(self):
        return True

    def mouse_down_left(self, pos):
        if self.button.bounds.contains_point(pos):
            old_flag = self.is_draggable
            self.is_draggable = False
            offset = pos - self.button.bounds.origin
            while pygame.mouse.get_pressed() == (1,0,0):
                mousepos = pygame.mouse.get_pos()
                if self.orientation == 'vertical':
                    new_x = self.button.bounds.origin.x
                    new_y = max(min(mousepos[1] - offset.y,
                                    self.bottom() - self.button.height()),
                                self.top())
                else:
                    new_y = self.button.bounds.origin.y
                    new_x = max(min(mousepos[0] - offset.x,
                                    self.right() - self.button.width()),
                                self.left())
                self.button.set_position(Point(new_x, new_y))
                self.update_value()
                world.do_one_cycle()
            self.is_draggable = old_flag

    def developers_menu(self):
        menu = super(Slider, self).developers_menu()
        menu.add_item("value...", 'show_value')
        return menu

    def show_value(self):
        self.inform(self.value)

class RoundedBox(Morph):

    def __init__(self, edge=4, border=2, bordercolor=pygame.Color(0,0,0)):
        self.edge = edge
        self.border = border
        self.bordercolor = bordercolor
        super(RoundedBox, self).__init__()

    def draw_new(self):
        self.image = pygame.Surface(self.extent().as_list())
        self.image.set_colorkey(TRANSPARENT)
        self.image.set_alpha(self.alpha)
        self.image.fill(TRANSPARENT)
        self.fill_rounded(self.edge, self.bordercolor, 0)
        self.fill_rounded(max(self.edge - (self.border // 2),0),
                          self.color, self.border)

    def fill_rounded(self, edge, color, inset):
        "private"
        fillrect = self.bounds.inset_by(inset)
        inner = fillrect.inset_by(edge)
        
        for center in inner.corners():
            pygame.draw.circle(
                self.image,
                color,
                (center - self.bounds.origin).as_list(),
                edge,
                0)
        pygame.draw.rect(
            self.image,
            color,
            (fillrect.origin - self.bounds.origin + Point(edge, 0)).corner(
                fillrect.corner - self.bounds.origin - Point(edge, 0)).as_rect(),
            0)
        pygame.draw.rect(
            self.image,
            color,
            (fillrect.origin - self.bounds.origin + Point(0, edge)).corner(
                fillrect.corner - self.bounds.origin - Point(0, edge)).as_rect(),
            0)

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

class Menu(RoundedBox):

    def __init__(self, target=None, title=None):
        self.target = target
        self.title = title
        if target == None:
            self.target = self
        self.items = []
        self.label = None
        super(Menu, self).__init__()
        self.is_draggable = False

    def add_item(self, label="close", action='nop'):
        self.items.append((label, action))

    def add_line(self, width=1):
        self.items.append((0,width))

    def add_entry(self, default='', width=100):
        field = StringField(default, width)
        field.is_editable = True
        self.items.append(field)

    def add_color_picker(self, default=pygame.Color(0,0,0)):
        field = ColorPicker(default)
        field.is_draggable = False
        self.items.append(field)

    def get_entries(self):
        entries = []
        for item in self.items:
            if isinstance (item, StringField):
                entries.append(item.string())
        return entries

    def get_color_picks(self):
        picks = []
        for item in self.items:
            if isinstance (item, ColorPicker):
                picks.append(item.get_choice())
        return picks

    def index_of(self, item):
        list = []
        for child in self.children:
            if isinstance(child, MenuItem):
                list.append(child)
        return list.index(item)
       
    def perform(self, item):
        self.delete()
        item.target.__getattribute__(item.action)()

    def nop(self):
        pass

    def create_label(self):
        if self.label != None:
            self.label.delete()
        text = Text(self.title,
                    fontname="verdana",
                    fontsize=10,
                    bold=True,
                    italic=False,
                    alignment='center')
        text.color = pygame.Color(254,254,254)
        text.background_color = self.bordercolor

        text.draw_new()
        self.label = RoundedBox(3,0)
        self.label.color = self.bordercolor
        self.label.set_extent(text.extent() + 4)
        self.label.draw_new()
        self.label.add(text)
        self.label.text = text
        
    def draw_new(self):
        for m in self.children:
            m.delete()
        self.children = []
        self.edge = 5
        self.border = 2
        self.color = pygame.Color(254,254,254)
        self.bordercolor = pygame.Color(60,60,60)
        self.set_extent(Point(0, 0))
        if self.title != None:
            self.create_label()
            self.label.set_position(self.bounds.origin + 4)
            self.add(self.label)
            y = self.label.bottom()
        else:
            y = self.top() + 4
        x = self.left() + 4
        for pair in self.items:
            if isinstance(pair,StringField) or isinstance(pair,ColorPicker):
                item = pair
            elif pair[0] == 0:
                item = Morph()
                item.color = self.bordercolor
                item.set_height(pair[1])
            else:
                item = MenuItem(self.target, pair[1], pair[0])
            item.set_position(Point(x, y))
            self.add(item)
            y += item.height()
        fb = self.full_bounds()
        self.set_extent(fb.extent() + 4)
        self.adjust_widths()
        super(Menu, self).draw_new()

    def max_width(self):
        w = 0
        for item in self.children:
            if isinstance(item, Widget):
                w = max(w, item.width())
        if self.label != None:
            w = max(w, self.label.width())
        return w

    def adjust_widths(self):
        w = self.max_width()
        for item in self.children:
            item.set_width(w)
            if isinstance(item, MenuItem):
                item.create_backgrounds()
            else:
                item.draw_new()
                if item is self.label:
                    item.text.set_position(
                        item.center() - (item.text.extent() // 2))

    def popup(self, world, pos):
        self.draw_new()
        self.set_position(pos)
        self.add_shadow("shade", Point(2,2), 80)
        self.keep_within(world)
        world.add(self)
        world.open_menu = self
        self.full_changed()
        for item in self.items:
            if isinstance(item, StringField):
                item.text.edit()
                return

    def popup_at_hand(self):
        self.popup(world, world.hand.position())

    def popup_centered_at_hand(self):
        self.draw_new()
        self.popup(world, (world.hand.position() - (self.extent() // 2)))

    def popup_centered_in_world(self):
        self.draw_new()
        self.popup(world, (world.center() - (self.extent() // 2)))

class SelectionMenu(Menu):

    def __init__(self, target=None, title=None):
        super(SelectionMenu, self).__init__(None, title)
        self.choice = None

    def perform(self, item):
        if item.action != 'nop':
            self.choice = item.action
        else:
            self.choice = item.label_string

    def get_user_choice(self):
        self.choice = None
        self.popup_at_hand()
        while self.choice == None:
            world.do_one_cycle()
        self.delete()
        return self.choice

class ListMenu(object):

    def __init__(self,
                 list=['one' 'two' 'three'],
                 label=None,
                 maxitems=30):
        self.list = list
        self.maxitems = maxitems
        self.label = label
        self.build_menus()

    def build_menus(self):
        self.menus = []
        count = 0
        sm = SelectionMenu()
        if self.label != None:
            sm.title = self.label
            sm.is_draggable = True
        for item in self.list:
            count += 1
            if count > self.maxitems:
                self.menus.append(sm)
                count = 1
                sm = SelectionMenu()
                sm.add_item("back...", self.menus[len(self.menus) - 1])
                sm.add_line()
                if self.label != None:
                    sm.title = self.label
                    sm.is_draggable = True
            sm.add_item(item)
        self.menus.append(sm)
        for menu in self.menus[:len(self.menus) - 1]:
            menu.add_line()
            menu.add_item("more...", self.menus[self.menus.index(menu) + 1])

    def get_user_choice(self):
        choice = self.menus[0].get_user_choice()
        while isinstance(choice, SelectionMenu):
            choice = choice.get_user_choice()
        return choice        

class Trigger(Morph):
    "basic button functionality"

    def __init__(self, target=None,
                 action=None,
                 label=None,
                 fontname="verdana",
                 fontsize=10,
                 bold=False,
                 italic=False):
        self.name = "trigger"
        self.hilite_color = pygame.Color(192,192,192)
        self.press_color = pygame.Color(128,128,128)
        self.label_string = label
        self.fontname = fontname
        self.fontsize = fontsize
        self.bold = bold
        self.italic = italic
        self.label = None
        super(Trigger, self).__init__()
        self.color = pygame.Color(254,254,254)
        self.draw_new()
        self.target = target
        self.action = action
        self.is_draggable = False

    def draw_new(self):
        "initialize my surface"
        self.create_backgrounds()
        if self.label_string != None:
            self.create_label()

    def create_backgrounds(self):
        self.normal_image = pygame.Surface(self.extent().as_list())
        self.normal_image.fill(self.color)
        self.normal_image.set_alpha(self.alpha)
        self.hilite_image = pygame.Surface(self.extent().as_list())
        self.hilite_image.fill(self.hilite_color)
        self.hilite_image.set_alpha(self.alpha)
        self.press_image = pygame.Surface(self.extent().as_list())
        self.press_image.fill(self.press_color)
        self.press_image.set_alpha(self.alpha)
        self.image = self.normal_image

    def create_label(self):
        if self.label != None:
            self.label.delete()
        self.label = String(self.label_string,
                                 self.fontname,
                                 self.fontsize,
                                 self.bold,
                                 self.italic)
        self.label.set_position(self.center() - (self.label.extent() // 2))
        self.add(self.label)

    #Trigger events:

    def handles_mouse_over(self):
        return True

    def handles_mouse_click(self):
        return True

    def mouse_enter(self):
        self.image = self.hilite_image
        self.changed()

    def mouse_leave(self):
        self.image = self.normal_image
        self.changed()

    def mouse_down_left(self, pos):
        self.image = self.press_image
        self.changed()

    def mouse_click_left(self, pos):
        self.target.__getattribute__(self.action)()

class MenuItem(Trigger, Widget):

    def create_label(self):
        if self.label != None:
            self.label.delete()
        self.label = String(self.label_string,
                                 self.fontname,
                                 self.fontsize,
                                 self.bold,
                                 self.italic)
        self.set_extent(self.label.extent() + Point(8,0))
        np = self.position() + Point(4,0)
        self.label.bounds = np.extent(self.label.extent())
        self.add(self.label)

    def mouse_click_left(self, pos):
        if isinstance(self.parent, Menu):
            self.world().open_menu = None
        self.parent.perform(self)

class Bouncer(Morph):

    def __init__(self, type="vertical", speed=1):
        super(Bouncer, self).__init__()
        self.is_stopped = False
        self.fps = 50
        self.type = type
        if self.type == "vertical":
            self.direction = "down"
        else:
            self.direction = "right"
        self.speed = speed

    def move_up(self):
        self.move_by(Point(0, -self.speed))

    def move_down(self):
        self.move_by(Point(0, self.speed))

    def move_right(self):
        self.move_by(Point(self.speed, 0))

    def move_left(self):
        self.move_by(Point(-self.speed, 0))

    def step(self):
        if not self.is_stopped:
            if self.type == "vertical":     
                if self.direction == "down":
                    self.move_down()
                else:
                    self.move_up()
                if (self.full_bounds().top() < self.parent.top()
                    and self.direction == "up"):
                    self.direction = "down"
                if (self.full_bounds().bottom() > self.parent.bottom()
                    and self.direction == "down"):
                    self.direction = "up"
            elif self.type == "horizontal":     
                if self.direction == "right":
                    self.move_right()
                else:
                    self.move_left()
                if (self.full_bounds().left() < self.parent.left()
                    and self.direction == "left"):
                    self.direction = "right"
                if (self.full_bounds().right() > self.parent.right()
                    and self.direction == "right"):
                    self.direction = "left"

    #Bouncer menu:

    def developers_menu(self):
        menu = super(Bouncer, self).developers_menu()
        menu.add_line()
        if self.is_stopped:
            menu.add_item("go!", 'toggle_motion')
        else:
            menu.add_item("stop!", 'toggle_motion')
        menu.add_item("speed...", 'choose_speed')
        if self.type == "vertical":
            menu.add_item("horizontal", 'toggle_direction')
        else:
            menu.add_item("vertical", 'toggle_direction')
        return menu

    def choose_speed(self):
        result = self.prompt("speed:",
                            str(self.speed),
                            50)
        if result != None:
            self.speed = min(max(int(result),0),self.width()//3)

    def toggle_direction(self):
        if self.type == "vertical":
            self.type = "horizontal"
            self.direction = "right"
        else:
            self.type = "vertical"
            self.direction = "up"

    def toggle_motion(self):
        self.is_stopped = not self.is_stopped


class String(Morph):
    "I am a single line of text"
                      
    def __init__(self,
                 text,
                 fontname="verdana",
                 fontsize=12,
                 bold=False,
                 italic=False):
        self.text = text
        self.fontname = fontname
        self.fontsize=fontsize
        self.bold = bold
        self.italic = italic
        self.is_editable = False
        super(String, self).__init__()
        self.color = pygame.Color(0,0,0)
        self.draw_new()

    def __repr__(self):
        return 'String("' + self.text + '")'

    def draw_new(self):
        self.font = pygame.font.SysFont(
            self.fontname,
            self.fontsize,
            self.bold,
            self.italic)
        self.image = self.font.render(self.text, 1, self.color)
        self.image.set_alpha(self.alpha)
        corner = Point(self.image.get_width(),
                                   self.image.get_height())
        self.bounds.corner = self.bounds.origin + corner

    #String menu:

    def developers_menu(self):
        menu = super(String, self).developers_menu()
        menu.add_line()
        if not self.is_editable:
            menu.add_item("edit...", 'edit')
        menu.add_item("font name...", 'choose_font')
        menu.add_item("font size...", 'choose_font_size')
        menu.add_line()
        if self.bold or self.italic:
            menu.add_item("normal", 'set_to_normal')
        if not self.bold:
            menu.add_item("bold", 'set_to_bold')
        if not self.italic:
            menu.add_item("italic", 'set_to_italic')
        return menu

    def edit(self):
        world.edit(self)

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

    #String events:

    def handles_mouse_click(self):
        return self.is_editable

    def mouse_click_left(self, pos):
        self.edit()
        world.text_cursor.goto_pos(pos)

class TextCursor(Blinker):
    """I am a String editing widget"""

    def __init__(self, stringMorph):
        self.target = stringMorph
        self.original_string = stringMorph.text
        self.pos = len(stringMorph.text)
        super(TextCursor, self).__init__()
        ls = self.target.font.get_linesize()
        self.set_extent(Point(max(ls // 20, 1), ls ))
        self.draw_new()
        self.goto(self.pos)

    #TextCursor event-processing:

    def process_keyboard_event(self, event):
        code = event.dict["key"]
        if code == 276:
            self.go_left()
        elif code == 275:
            self.go_right()
        elif code == 278:
            self.go_home()
        elif code == 279:
            self.goto_end()
        elif code == 127:
            self.delete_right()
        elif code == 8:
            self.delete_left()
        elif code == 13:
            self.accept()
        elif code == 27:
            self.cancel()
        elif 31 < code < 128:
            self.insert(event.dict["unicode"])

    #TextCursor navigation:

    def goto(self, newpos):
        dest = newpos
        text = self.target.text
        font = self.target.font
        if dest < 0:
            dest = 0
        elif dest > len(text):
            dest = len(text)
        x_offset = 0
        for idx in range(0, dest):
            x_offset += font.metrics(text)[idx][4]
        self.pos = dest
        x = self.target.left() + x_offset
        y = self.target.top()
        self.set_position(Point(x,y))

    def go_left(self):
        self.goto(self.pos - 1)
        
    def go_right(self):
        self.goto(self.pos + 1)

    def go_home(self):
        self.goto(0)
    
    def goto_end(self):
        self.goto(len(self.target.text))

    def goto_pos(self, point):
        idx = 0
        char_x = 0
        while point.x - self.target.left() > char_x:
            char_x += self.target.font.metrics(self.target.text)[idx][4]
            idx += 1
        self.goto(idx - 1)
        self.show()

    def accept(self):
        world.stop_editing()

    def cancel(self):
        self.target.text = self.original_string
        self.target.changed()
        self.target.draw_new()
        self.target.changed()
        world.stop_editing()

    def insert(self, char):
        text = self.target.text
        text = text[:self.pos] + char + text[self.pos:]
        self.target.text = text
        self.target.draw_new()
        self.target.changed()
        self.go_right()
        
    def delete_right(self):
        self.target.changed()
        text = self.target.text
        text = text[:self.pos] + text[(self.pos + 1):]
        self.target.text = text
        self.target.draw_new()

    def delete_left(self):
        self.target.changed()
        text = self.target.text
        text = text[:max(self.pos - 1, 0)] + text[self.pos:]
        self.target.text = text
        self.target.draw_new()
        self.go_left()

class Text(Morph):
    "I am a mult line, word wrapping string"

    def __init__(self,
                 text,
                 fontname="verdana",
                 fontsize=12,
                 bold=False,
                 italic=False,
                 alignment='left',
                 width=0):
        pygame.font.init()
        self.background_color = pygame.Color(254,254,254)
        self.text = text
        self.words = []
        self.fontname = fontname
        self.fontsize = fontsize
        self.bold = bold
        self.italic = italic
        self.alignment=alignment
        self.max_width = width
        super(Text, self).__init__()
        self.color = pygame.Color(0,0,0)
        self.draw_new()

    def __repr__(self):
        return 'Text("' + self.text + '")'

    def parse(self):
        self.words = []
        paragraphs = self.text.splitlines()
        self.max_line_width = 0
        for p in paragraphs:
            self.words.extend(p.split(' '))
            self.words.append('\n')
        self.font = pygame.font.SysFont(
            self.fontname,
            self.fontsize,
            self.bold,
            self.italic)
        self.lines = []
        oldline = ''
        for word in self.words:
            if word == '\n':
                self.lines.append(oldline)
                self.max_line_width = max(self.max_line_width,
                                          self.font.size(oldline)[0])
                oldline = ''
            else:
                if self.max_width > 0:
                    newline = oldline + word + ' '
                    w = self.font.size(newline)
                    if w[0] > self.max_width:
                        self.lines.append(oldline)
                        self.max_line_width = max(self.max_line_width,
                                                    self.font.size(oldline)[0])
                        oldline = word + ' '
                    else:
                        oldline = newline
                else:
                    oldline = oldline + word + ' '
    
    def draw_new(self):
        surfaces = []
        height = 0
        self.parse()
        for line in self.lines:
            s = self.font.render(line, 1, self.color)
            surfaces.append(s)
            height += s.get_height()
        if self.max_width == 0:
            self.set_extent(Point(self.max_line_width, height))
        else:
            self.set_extent(Point(self.max_width, height))
        self.image = pygame.Surface(self.extent().as_list())
        self.image.fill(self.background_color)
        self.image.set_alpha(self.alpha)
        y = 0
        for s in surfaces:
            if self.alignment == 'right':
                x = self.max_line_width - s.get_width()
            elif self.alignment == 'center':
                x = (self.max_line_width - s.get_width()) // 2
            else:
                x = 0
            self.image.blit(s, (x,y))
            y += s.get_height()

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

class Hand(Morph):
    "I represent the mouse cursor"

    def __init__(self):
        super(Hand, self).__init__()
        self.world = None
        self.mouse_over_list = []
        self.mouse_down_morph = None
        self.morph_to_grab = None
        self.bounds = Point(0, 0).corner(Point(0,0))

    def __repr__(self):
        return 'Hand(' + self.center().__str__() + ')'

    def changed(self):
        if self.world != None:
            b = self.full_bounds()
            if b.extent() != Point(0, 0):
                self.world.broken.append(self.full_bounds())

    def draw_on(self, surface, rectangle=None):
        pass

    def process_mouse_event(self, event):
        if event.type == 4:
            self.process_mouse_move(event)
        elif event.type == 5:
            self.process_mouse_down(event)
        elif event.type == 6:
            self.process_mouse_up(event)

    def morph_at_pointer(self):
        morphs = self.world.children
        for m in morphs[::-1]:
            if m.full_bounds().contains_point(self.bounds.origin) and not(
                isinstance(m, Shadow)) and m.is_visible:
                return m.morph_at(self.bounds.origin)
        return self.world

    def all_morphs_at_pointer(self):
        answer = []
        morphs = self.world.all_children()
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

    def grab(self, morph):
        if self.children == []:
            world.stop_editing()
            morph.add_shadow()
            self.add(morph)
            self.changed()

    def drop(self):
        if self.children != []:
            morph = self.children[0]
            target = self.drop_target_for(morph)
            self.changed()
            target.add(morph)
            morph.changed()
            morph.remove_shadow()
            self.children = []
            self.set_extent(Point(0, 0))

    #Hand event dispatching:

    def process_mouse_down(self, event):
        if self.children != []:
            self.drop()
        else:
            pos = Point(event.dict["pos"][0],
                        event.dict["pos"][1])
            morph = self.morph_at_pointer()

            is_menu_click = False
            for m in morph.all_parents():
                if isinstance(m, Menu) or isinstance(m, Widget):
                    is_menu_click = True
            if not is_menu_click:
                if isinstance(world.open_menu, SelectionMenu):
                    world.open_menu.choice = False
                elif isinstance(world.open_menu, Menu):
                    world.open_menu.delete()

            if world.text_cursor != None:
                if morph is not world.text_cursor.target:
                    world.stop_editing()

            self.morph_to_grab = morph.root_for_grab()
            while not morph.handles_mouse_click():
                morph = morph.parent
            self.mouse_down_morph = morph
            if event.dict["button"] == 1:
                morph.mouse_down_left(pos)
            elif event.dict["button"] == 2:
                morph.mouse_down_middle(pos)
            elif event.dict["button"] == 3:
                morph.mouse_down_right(pos)
            else:
                pass

    def process_mouse_up(self, event):
        if self.children != []:
            self.drop()
        else:
            pos = Point(event.dict["pos"][0],
                        event.dict["pos"][1])
            morph = self.morph_at_pointer()

            is_menu_click = False
            for m in morph.all_parents():
                if isinstance(m, Menu) or isinstance(m, Widget):
                    is_menu_click = True

            if event.dict["button"] == 3 and not is_menu_click:
                menu = morph.context_menu()
                if menu != None:
                    menu.popup_at_hand()
            
            while not morph.handles_mouse_click():
                morph = morph.parent
            if event.dict["button"] == 1:
                morph.mouse_up_left(pos)
                if morph is self.mouse_down_morph:
                    morph.mouse_click_left(pos)
            elif event.dict["button"] == 2 and not is_menu_click:
                morph.mouse_up_middle(pos)
                if morph is self.mouse_down_morph:
                    morph.mouse_click_middle(pos)
            elif event.dict["button"] == 3 and not is_menu_click:
                morph.mouse_up_right(pos)
                if morph is self.mouse_down_morph:
                    morph.mouse_click_right(pos)
            else:
                pass

    def process_mouse_move(self, event):
        mouse_over_new = self.all_morphs_at_pointer()
        if self.children == [] and event.dict["buttons"][0] == 1:
            top_morph = self.morph_at_pointer()
            if top_morph.handles_mouse_move():
                pos = Point(event.dict["pos"][0],
                            event.dict["pos"][1])
                top_morph.mouse_move(pos)
            morph = top_morph.root_for_grab()
            if morph is self.morph_to_grab and morph.is_draggable:
                self.grab(morph)
        for old in self.mouse_over_list:
            if old not in mouse_over_new and old.handles_mouse_over():
                old.mouse_leave()
                if event.dict["buttons"][0] == 1:
                    old.mouse_leave_dragging()
        for new in mouse_over_new: 
            if new not in self.mouse_over_list and new.handles_mouse_over():
                new.mouse_enter()
                if event.dict["buttons"][0] == 1:
                    new.mouse_enter_dragging()
        self.mouse_over_list = mouse_over_new

    #Hand testing:

    def is_dragging(self, morph):
        if self.children != []:
            return morph is self.children[0]
        else:
            return False        

class Frame(Morph):
    """ I clip my submorphs at my bounds """

    def full_bounds(self):
        shadow = self.get_shadow()
        if shadow != None:
            return self.bounds.merge(shadow.bounds)
        else:
            return self.bounds

    def wants_drop_of(self, morph):
        return True

    def full_draw_on(self, surface, rectangle=None):
        if rectangle == None:
            rectangle = self.full_bounds()
        rectangle = rectangle.intersect(self.full_bounds())
        self.draw_on(surface, rectangle)
        for child in self.children:
            if isinstance (child, Shadow):
                child.full_draw_on(surface, rectangle)
            else:
                child.full_draw_on(surface, self.bounds.intersect(rectangle))

    def developers_menu(self):
        menu = super(Frame, self).developers_menu()
        menu.add_line()
        menu.add_item("move all inside...", 'keep_all_submorphs_within')
        return menu

    def keep_all_submorphs_within(self):
        for m in self.children:
            if not isinstance(m, Shadow):
                m.keep_within(self)

class StringField(Frame, Widget):

    def __init__(self, default='',
                 minwidth=100,
                 fontname="verdana",
                 fontsize=12,
                 bold=False,
                 italic=False):
        self.default = default
        self.minwidth = minwidth
        self.fontname = fontname
        self.fontsize = fontsize
        self.bold = bold
        self.italic = italic
        super(StringField, self).__init__()
        self.color = pygame.Color(254,254,254)
        self.draw_new()

    def draw_new(self):
        "initialize my surface"
        super(StringField, self).draw_new()
        self.text = None
        for m in self.children:
            m.delete()
        self.children = []
        self.text = String(self.default,
                           self.fontname,
                           self.fontsize,
                           self.bold,
                           self.italic)
        self.text.is_editable = True
        self.text.is_draggable = False
        self.set_extent(Point(self.minwidth, self.text.height()))
        self.text.set_position(self.position())
        self.add(self.text)

    def string(self):
        return self.text.text

    def handles_mouse_click(self):
        return False

    def mouse_click_left(self, pos):
        self.text.edit()


class World(Frame):
    "I represent the screen"
                      
    def __init__(self, x=800, y=600):
        super(World, self).__init__()
        self.hand = Hand()
        self.hand.world = self
        self.keyboard_receiver = None
        self.text_cursor = None
        self.bounds = Point(0, 0).corner(Point(x, y))
        self.color = pygame.Color(130, 130, 130)
        self.open_menu = None
        self.is_visible = True
        self.is_draggable = False
        self.is_dev_mode = True
        self.is_quitting = False
        self.draw_new()
        self.broken = []

    def __repr__(self):
        return 'World(' + self.extent().__str__() + ')'

    def draw_new(self):
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
        if isinstance(morph, Menu):
            if isinstance(self.open_menu, Menu):
                self.open_menu.delete()
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

    def update_broken(self):
        rects = []
        for r in self.broken:
            if r.extent() > Point(0,0):
                rects.append(r.as_rect())
                self.full_draw_on(self.image, r)
        pygame.display.update(rects)
        self.broken = []

    def wait_for_next_frame(self):
        current = pygame.time.get_ticks()
        elapsed = current - self.last_time
        leftover = (1000 // self.fps) - elapsed
        if leftover > 0:
            pygame.time.wait(leftover)
        self.last_time = current

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

    def user_create_ellipse(self):
        ellipse = Ellipse()
        ellipse.color = pygame.Color(40,40,40)
        ellipse.draw_new()
        ellipse.pick_up()

    def user_create_circle_box(self):
        box = CircleBox()
        box.color = pygame.Color(120,120,120)
        box.draw_new()
        box.pick_up()

    def user_create_rounded_box(self):
        box = RoundedBox()
        box.color = pygame.Color(110,110,110)
        box.draw_new()
        box.pick_up()

    def user_create_polygon(self):
        self.hint('left click to add vertices\nmiddle click to complete')
        oldpos = None
        vertices = []
        while pygame.mouse.get_pressed() != (0,1,0):
            while pygame.mouse.get_pressed() == (0,0,0):
                world.do_one_cycle()
            mousepos = pygame.mouse.get_pos()
            world.do_one_cycle()
            if mousepos != oldpos:
                vertices.append(Point(mousepos[0], mousepos[1]))
                oldpos = mousepos
        if len(vertices) > 2:
            polygon = Polygon(vertices)
            polygon.color = pygame.Color(70,70,70)
            polygon.draw_new()
            self.add(polygon)
            polygon.changed()
        else:
            self.inform("please specify\nat least 3 vertices")

    def user_create_string(self):
        string = String("Hello, World!")
        string.is_editable = True
        string.pick_up()

    def user_create_text(self):
        text = Text("Ich wei nicht, was soll es bedeuten, das ich so traurig bin, at mit ihrem Singen, die Loreley getan. ")
        text.max_width = 400
        text.draw_new()
        text.pick_up()

    def user_create_bouncer(self):
        bouncer = Bouncer()
        bouncer.color = pygame.Color(30,30,30)
        bouncer.draw_new()
        bouncer.is_stopped = True
        bouncer.pick_up()

    def user_create_frame(self):
        frame = Frame()
        frame.color = pygame.Color(100,100,100)
        frame.set_extent(Point(150,100))
        frame.draw_new()
        frame.pick_up()

    def user_create_color_palette(self):
        ColorPalette().pick_up()

    def user_create_slider(self):
        Slider().pick_up()

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
" + version + "\n\nwritten by Jens @moenig.org")

    #World utilities:

    def fontname_by_user(self):
        names = sorted(pygame.font.get_fonts())
        choice = ListMenu(names,
                          'choose font').get_user_choice()
        if choice == False:
            return None
        else:
            return choice

    #World stepping & event dispatching:

    def step_frame(self):
        event = pygame.event.poll()
        if event.type != 0:
            if event.type in range(4, 7):
                self.hand.process_mouse_event(event)
            elif event.type == 2 and self.keyboard_receiver != None:
                self.keyboard_receiver.process_keyboard_event(event)
            elif event.type == 12:
                return "quit"
            elif event.type == 16:
                self.change_extent_to(Point(event.size[0],
                                            event.size[1]))
        super(World, self).step_frame()

    #World events / dragging and dropping:

    def wants_drop_of(self, morph):
        return True

    def handles_mouse_click(self):
        return True

    #World mainloop:

    def loop(self):
        self.full_draw_on(self.image)
        pygame.display.update()
        self.last_time = pygame.time.get_ticks()
        while not self.is_quitting:
            self.do_one_cycle()
        pygame.quit()

    def do_one_cycle(self):
        mpos = list(pygame.mouse.get_pos())
        self.hand.set_position(Point(mpos[0], mpos[1]))
        if self.step_frame() == "quit":
            self.delete()
        self.update_broken()
        if self.fps > 0:
            self.wait_for_next_frame()

world = World()
world.loop()
