

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
    
    def __truediv__(self, other):
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
            return Point(-offset.y, offset.y) + center
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
        """
        new_position = Point(self.position().x+100,self.position().y+100)
        
        self.set_position(new_position)
        """
        
        dimensions = self.extent().as_list()
        
        print("dimensions : ", dimensions)
        
        bgl.glRecti(self.position().x, self.position().y, self.position().x+dimensions[0], self.position().y+dimensions[1])  
        print ("I draw a rect : ", [self.position().x, self.position().y, self.position().x+dimensions[0], self.position().y+dimensions[1]])
        
        
        
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
        self.bounds = Point(0, 0).corner(Point(0,0))

    def __repr__(self):
        return 'Hand(' + self.center().__str__() + ')'

    def changed(self):
        if self.world != None:
            b = self.full_bounds()
            if b.extent() != Point(0, 0):
                self.world.broken.append(self.full_bounds())

    def draw_on(self, rectangle=None):
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


    