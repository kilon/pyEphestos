debug050512_0900 = False #060512, seems to be OK now (problem with test_Menu)

import bgl, blf
from .rectangle import *
from .node import *
#from .world import * #error ==> 050512_1225
'''
  File "C:\BlenderSVN\cmake_all3\bin\2.63\scripts\addons\Ephestos\morpheas\hand.py", line 28, in <module>
    class Hand(Morph):
NameError: name 'Morph' is not defined
'''

#PKHG.circular  from . class_Text import Text
from math import radians, sin, cos, sqrt
debug_world = False


#for the moment
#from .  morpheas import Frame, Menu

class Morph(Node ): 
    def __init__(self, bounds = None, rounded = False, with_name = False):
        super(Morph, self).__init__()
        if bounds:
            self.bounds = bounds
        else:
            self.bounds = Point(0, 0).get_corner(Point(100,60))
        self.color = (0.3, 0.3, 0.3, 1.0)
        self.is_visible = True
        self.is_draggable = True
        self.fps = 0
        self.rounded = rounded
        # self.last_time = pygame.time.get_ticks()
        self.with_name = with_name
        self.path_to_local_fonts  = self.get_local_font_path()
        self.default_font = self.path_to_local_fonts + "/verdana.ttf"
        self.font_id = blf.load(self.default_font)
        
    def __repr__(self):
        return self.__class__.__name__ + "(" + self.name + ")"

    def get_local_font_path(self):
        import  addon_utils
        result = addon_utils.paths()[0] + "/Ephestos/fonts"
        return result
    
    def delete(self):
        if self.parent != None:
            self.full_changed()
            self.parent.remove_child(self)
    
    def get_color(self):
        """ getter: get the color of the morph"""
        return self.color
    
    def set_color(self,r,g,b,alpha):
        """ getter : (red , green , blue , alpha ) Set the color of the morph RGB plus alpha for transparency , all floats starting from 0 (0.0) and ending in 1 (1.0)"""
        self.color=(r,g,b,alpha)
        
    #stepping:

    def get_wants_to_step(self):
        return self.is_visible

    def get_step(self):
        pass

    #Morph accessing - geometry getting:

    def get_left(self):
        return self.bounds.get_left()

    def get_right(self):
        return self.bounds.get_right()

    def get_top(self):
        return self.bounds.get_top()

    def get_bottom(self):
        return self.bounds.get_bottom()

    def get_center(self):
        return self.bounds.get_center()

    def get_bottom_center(self):
        return self.bounds.get_bottom_center()

    def get_bottom_left(self):
        return self.bounds.get_bottom_left()

    def get_bottom_right(self):
        return self.bounds.get_bottom_right()

    def get_bounding_box(self):
        return self.bounds

    def get_corners(self):
        return self.bounds.get_corners()

    def get_left_center(self):
        return self.bounds.get_left_center()

    def get_right_center(self):
        return self.bounds.get_right_center()

    def get_top_center(self):
        return self.bounds.get_top_center()

    def get_top_left(self):
        return self.bounds.get_top_left()

    def get_top_right(self):
        return self.bounds.get_top_right()

    def get_position(self):
        return self.bounds.origin

    def get_extent(self):
        return self.bounds.get_extent()

    def get_width(self):
        return self.bounds.get_width()

    def get_height(self):
        return self.bounds.get_height()

    def get_full_bounds(self):
        result = self.bounds
        for child in self.children:
            result = result.get_merge(child.get_full_bounds())
        return result

    #Morph accessing - changing:

    def set_position(self, aPoint):
        delta = aPoint - self.get_bottom_left()
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
        self.bounds = self.bounds.get_translate_by(delta)
        for child in self.children:
            child.move_by(delta)
        self.changed()

    def keep_within(self, morph):
        "make sure I am completely within another morph's bounds"
        left_off = self.get_full_bounds().left() - morph.left()
        if left_off < 0:
            self.move_by(Point(-left_off, 0))
        right_off = self.get_full_bounds().get_right() - morph.get_right()
        if right_off > 0:
            self.move_by(Point(-right_off, 0))
        top_off = self.get_full_bounds().get_top() - morph.get_top()
        if top_off < 0:
            self.move_by(Point(0, -top_off))
        bottom_off = self.get_full_bounds().get_bottom() - morph.get_bottom()
        if bottom_off > 0:
            self.move_by(Point(0, -bottom_off))

    #Morph displaying:
    def draw(self):
#        print("morph", self, "visibility = ", self.is_visible) 
#        if not self.is_visible:
#            return

        "initialize my surface"
        # print("I use color : ", self.color)
        bgl.glEnable(bgl.GL_BLEND) #PKHG.??? needed?
        bgl.glColor4f(*self.color)
        dimensions = self.get_extent().as_list()
        if self.rounded:
            Morph.draw_rounded_morph(self, 0.3, self.color, rectangle = False)
        else:
            bgl.glRecti(self.get_position().x, self.get_position().y, self.get_position().x+dimensions[0], self.get_position().y+dimensions[1])
#PKHG.TODO font stuff
#        font_id = blf.load("c:/Windows/Fonts/arialbd.ttf")
        font_id = self.font_id 
        size = 16
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
            Morph.draw_string_to_viewport(self.name, self, size , (1,1,1,1), font_id, x , y)

    
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
        w = self.get_root()
        
        """if isinstance(w, World):
            w.broken.append(copy.copy(self.bounds))"""
        
    def full_changed(self):
        w = self.get_root()
#PKHG.TODO        if isinstance(w, World):
#            w.broken.append(copy.copy(self.full_bounds()))

    #Morph accessing - structure:
    
    def world(self):
        if isinstance(self.root(), World):
            return self.root()
    
    def add(self, morph):
        parent = morph.parent
        if parent is not None:
            if debug050512_0900:
                print("morph.py add; morph = ", morph, " parent of morph", parent)
            if debug050512_0900:
                print("---------------->>>> morph.py add: not deleting", morph)
                pass
            else:
                parent.remove_child(morph)
        self.add_child(morph)

    def get_morph_at(self, point):
        morphs = self.get_all_children()
        for m in morphs[::-1]:
            if m.get_full_bounds().get_contains_point(point):
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

    def get_root_for_grab(self):
        if self.parent == None or isinstance(self.parent, Frame):
            return self
        else:
            return self.parent.get_root_for_grab()

    def get_wants_drop_of(self, morph):
        "default is False - change for subclasses"
        return False

    def pick_up(self):
        self.set_position(world.hand.position() - (self.extent() // 2))
        world.hand.grab(self)

    #Morph events:

    def get_handles_mouse_over(self):
        return False

    def get_handles_mouse_click(self):
        return False

    def get_handles_mouse_move(self):
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

    def pick_color(self, msg, default=(0,0,0,1)):
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

    def ellipsePoint(center, a, b, t):
        t = radians(t)
        x = a * cos(t)
        y = b * sin(t)
        Pt = Point(x,y)
        return center + Pt


    def draw_rounded_morph(morph, small , color , rectangle = -1):
        def rounded_corners(cornerPT, offset,  NSEW, a):
    #        print("\n === dbg ronded corn", cornerPT, offset, NSEW, a)
            point_list = []
            numb = 10 
            fac = 90./numb
            tvals = [NSEW +  el * fac  for el in range(numb +1)]
            midPt = cornerPT + offset
            for t  in tvals:
                res = Morph.ellipsePoint(midPt,a,a,t)
                point_list.append(res)
            return point_list
#PKHG.ifdebug        if debug_world and not rectangle and  morph.name == "World":
#PKHG.OK            print("\n======DBG my name is", morph.name, " my color is", morph.color)
        small = abs(small)
        if rectangle:
            bounds = morph
        else:
            bounds = morph.bounds
        PNW = bounds.get_top_left()
        PZW = bounds.get_bottom_left()
        PZE = bounds.get_bottom_right()
        PNE = bounds.get_top_right()
        disUp = PNW.get_distance_to(PZW)
        disSide = PZW.get_distance_to(PZE)
        a = min(disUp, disSide) * small
    
        offset = Point(a, a)
        draw_all_points = []
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
            bgl.glColor4f(*color)
        else:
            bgl.glColor4f(*morph.color)
        bgl.glBegin(bgl.GL_POLYGON)
        for el in draw_all_points:
            bgl.glVertex2f(el.x,el.y)
        bgl.glEnd()
        return

    def draw_string_to_viewport(text, morph, size, color, font_id, x, y):
        ''' my_string : the text we want to print
            x, y : coordinates in integer values
            size : font height.
            colour : used for definining the colour'''
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


    

