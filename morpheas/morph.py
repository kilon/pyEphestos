#PKHG Set debug values!
debug_color = 5
debug050512_0900 = False #060512, seems to be OK now (problem with test_Menu)
debug_changed_130512_0810 = False #all items seem to have world as root
#do not use ^^^^^^^^^^^^^^^^^^^ too much output
import bgl, blf, bpy
from .rectangle import *
from .node import *

#PKHG to be OS independent
from os import path
path_sep = path.sep

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

    """ Morph class is the most important class of all. This is the central class used for any graphical element inside Morpheas. So any graphical element is a morph class that inherits from this class. The class inherits from the node class which is responsible for all parenting functionality. Via node any morph can be either a parent or the child of another morph. The central method of morph class is the draw method that feeds with opengl instruction for creating the visual representation of the morph. Other methods are handling a huge array of features like making a morph dragable, hidden, change position , trigger its own mouse and keyboard events and many many more. See docs for each method"""

    def __init__(self, bounds = None, rounded = False, with_name = False):

        """ constructor of morph class it can be called with no parameters or using the following keywords ->

        bounds : bounds set the bounds of the morph. It can be created using the Rect and Point  classes
        eg. morph = Morph( bounds = Rect(Point(0,0),Point(100,100)) will create a morph with weight and width of 100 pixels

        rounded : rounded is a boolean , if true will create a rounded morph

        with_name : This one set a name for the morph for easy access """

        super(Morph, self).__init__()
        if bounds: #PKHG>???28jun  and isinstance(bounds, Rectangle):
            self.bounds = bounds
        else:
            self.bounds = Rectangle(Point(0, 0), Point(100,60))
#PKHG test 3jul        self.color = (0.3, 0.3, 0.3, 1.0)
#sometimes working ???
        self.color = (1, 1, 1, 1)
        self.is_visible = True
        self.is_draggable = True
        self.fps = 0
        self.rounded = rounded
        # self.last_time = pygame.time.get_ticks()
        self.with_name = with_name
        self.path_to_local_fonts  = self.get_local_font_path()
        self.default_font = self.path_to_local_fonts + "/verdana.ttf"
        self.font_id = blf.load(self.default_font)
        self.my_name_size = 0
        self.texture_path = bpy.utils.script_paths()[0] + \
                          "/addons/Ephestos/data/images/".replace("/",path_sep)
        self.world = None
        self.texture = None
        self.is_textured = False



    def set_texture(self,file_name):
        """setter : set_texture(file_name). Set the texture to be used by the morph, the file_name is just the name of the file, path used is the folder images inside Ephestos in data"""
        file_path = self.texture_path + file_name
        self.texture= bpy.data.images.load(filepath = file_path)
        self.is_textured = True
        #self.texture.gl_load()
       # bgl.glBindTexture(bgl.GL_TEXTURE_2D, self.texture.bindcode)
        #bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MIN_FILTER, bgl.GL_NEAREST)

        #bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MAG_FILTER, bgl.GL_NEAREST) #GL_LINEAR seems to be used in Blender for background images

    def __repr__(self):
        """set how a morph is printed to the console and represented"""
        return self.__class__.__name__ + "(" + self.name + ")"

    def get_local_font_path(self):
        """getter: Returns the path where fonts used by Ephestos can be found"""
        import  addon_utils
        result = addon_utils.paths()[0] + "/Ephestos/fonts"
        return result

    def get_my_name_size(self):
        """getter: Returns then size of them morph's name"""
        return self.my_name_size

    def delete(self):
        """Removes the morph as child from any parent morph"""
        if self.parent != None:
            self.full_changed()
            self.parent.remove_child(self)

    def get_color(self):
        """ getter: get the color of the morph"""
        return self.color

##0.1 version    def set_color(self,r,g,b,alpha):
    def set_color(self,*rgba):
        """ setter : (red , green , blue , alpha )
        Set the color of the morph RGB plus alpha for transparency ,
        all floats starting from 0 (0.0) and ending in 1 (1.0)
        If no rgba is available and the key-value-pair is
        'color':"known color", that color is returned
        Errors in use will give the default (1,0,0,0.5), half visible red!
        """
        color_dict = {'red':(1, 0, 0, 1),'green':(0, 1, 0, 1), 'blue':(0, 0, 1, 1),'ERROR': (1,0,0,0.5)} #PKHG red may indicate an ERROR alpha = 0.5
        result = color_dict['ERROR'] #PKHG to be overwritten by good color
        if rgba:
            rgba = rgba[0]  #PKHG remove the * so to say
#PKHG.works
            if type(rgba) == type(""):
                if rgba in color_dict.keys():
                    result = color_dict[rgba]
                else:
                    print("\n***ERROR*** ", rgba ," not in colordictionary")
            else:
                if len(rgba) == 2  or len(rgba) > 4 and (min(rgba) < 0.0 or max(rgba) > 1.0):
                    print("\n***ERROR*** set_color argument must be either 1 or 4 see function documentation")
                elif len(rgba) == 3:
                    result = (rgba[0],rgba[1],rgba[2],1)
                elif len(rgba) == 4:
                    result  = rgba
        self.color = result #set a valid color!
        return result


    #stepping:

    def get_wants_to_step(self):
        return self.is_visible

    def get_step(self):
        pass

    #Morph accessing - geometry getting:

    def get_left(self):
        """ getter : Return the left side coordinates"""
        return self.bounds.get_left()

    def get_right(self):
        """ getter: Return the right side coordinates"""
        return self.bounds.get_right()

    def get_top(self):
        """ getter : Return the top side coordinates"""
        return self.bounds.get_top()

    def get_bottom(self):
        """ getter : Return the bottom side coordinates"""
        return self.bounds.get_bottom()

    def get_center(self):
        """ getter : Return the center  coordinates"""
        return self.bounds.get_center()

    def get_bottom_center(self):
        """ getter : Return the bottom center coordinates"""
        return self.bounds.get_bottom_center()

    def get_bottom_left(self):
        """ getter : Return the bottom left coordinates"""
        return self.bounds.get_bottom_left()

    def get_bottom_right(self):
        """ getter : Return the bottom right coordinates"""
        return self.bounds.get_bottom_right()

    def get_bounding_box(self):
        """ getter : Return the bounding box rect of the morph"""
        return self.bounds

    def get_corners(self):
        """ getter: Return corners coordinates"""
        return self.bounds.get_corners()

    def get_left_center(self):
        """ getter: Return left center coordinates"""
        return self.bounds.get_left_center()

    def get_right_center(self):
        """ getter: Return right center coordinates"""
        return self.bounds.get_right_center()

    def get_top_center(self):
        """ getter: Return top center coordinates"""
        return self.bounds.get_top_center()

    def get_top_left(self):
        """ getter: Return top left coordinates"""
        return self.bounds.get_top_left()

    def get_top_right(self):
        """ getter: Return top right coordinates"""
        return self.bounds.get_top_right()

    def get_position(self):
        """ getter: Return position coordinates"""
        return self.bounds.origin

    def get_extent(self):
        """ getter: Return extent coordinates"""
        return self.bounds.get_extent()

    def get_width(self):
        """ getter: Return width in pixels"""
        return self.bounds.get_width()

    def get_height(self):
        """ getter: Return height in pixels"""
        return self.bounds.get_height()

    def get_full_bounds(self):
        """ getter: Return full bounds which include morph bounds and all its childrend bounds"""
        result = self.bounds
        for child in self.children:
            result = result.get_merge(child.get_full_bounds())
        return result

    #Morph accessing - changing:

    def set_position(self, aPoint):
        """ setter: Set the position of morph. Can be used for moving morph on screen."""
        delta = aPoint - self.get_bottom_left()
        if delta.x != 0 or delta.y != 0:
            self.move_by(delta)

    def set_center(self, aPoint):
        """ setter: Set the position of morph setting moving its center """
        self.set_position(aPoint - (self.extent() // 2))

    def set_full_center(self, aPoint):
        """ setter: Set the position of morph setting the center of its full bounds which includes children bounds as well."""
        self.set_position(aPoint - (self.full_bounds().extent() // 2))

    def set_width(self, width):
        """ setter: Set width in pixels"""
        self.changed()
        self.bounds.corner = Point(self.bounds.origin.x + width,
                                   self.bounds.corner.y)
        self.changed()

    def set_height(self, height):
        """ setter: Set height in pixels"""
        self.changed()
        self.bounds.corner = Point(self.bounds.corner.x,
                                   self.bounds.origin.y + height)
        self.changed()

    def set_extent(self, aPoint):
        """ setter: Set extent ( set width and height ) using the Point class as the only argument"""
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
        left_off = self.get_full_bounds().get_left() - morph.get_left()
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
        """ the draw function of the morph """
        if self.is_textured:
            self.draw_textured()
        else:
            self.draw_untextured()

        for el in self.children:
            el.draw()

    def draw_textured(self):
        """ call this draw function only if morphs uses texture """
        if self.texture != None:

            self.texture.gl_load()
            bgl.glBindTexture(bgl.GL_TEXTURE_2D, self.texture.bindcode)
            bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MIN_FILTER, bgl.GL_NEAREST)

            bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MAG_FILTER, bgl.GL_NEAREST) #GL_LINEAR seems to be used in Blender for background images

            bgl.glEnable(bgl.GL_TEXTURE_2D)

            #bgl.glBlendFunc(bgl.GL_SRC_ALPHA, bgl.GL_ONE_MINUS_SRC_ALPHA)


            bgl.glColor4f(*self.color)
            bgl.glBegin(bgl.GL_QUADS)
            bgl.glTexCoord2d(0,0)
            bgl.glVertex2d(self.get_position().x,self.get_position().y)
            bgl.glTexCoord2d(0,1)
            bgl.glVertex2d(self.get_position().x,self.get_position().y+self.get_height())
            bgl.glTexCoord2d(1,1)
            bgl.glVertex2d(self.get_position().x+self.get_width(),self.get_position().y+self.get_height())
            bgl.glTexCoord2d(1,0)
            bgl.glVertex2d(self.get_position().x+self.get_width(),self.get_position().y)
            bgl.glEnd()
            bgl.glDisable(bgl.GL_BLEND)
            bgl.glDisable(bgl.GL_TEXTURE_2D)
            self.texture.gl_free()

        return

    def draw_untextured(self):
        """ call this draw function only if morph does not use texture"""
        global debug_color
#        print("morph", self, "visibility = ", self.is_visible)
#        if not self.is_visible:
#            return

#        print(">>>>>>>>>>> self and color = ",self, self.color)
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
#PKHG should be done elsewhere!        self.my_name_size = int(dims_x) + 2
        x = self.bounds.origin.x
        xx = self.bounds.corner.x
        difx = xx - x
        if dims_x > difx:
            quot = difx/dims_x
            size = int(size * quot)
        y = self.bounds.corner.y - size

#PKHG. bounds should include name of morph
#PKHG 040612 does not work???!           self.bounds = Rectangle(self.bounds.origin,Point(int(dims_x) + 2,\
#                                    self.bounds.corner.y))
#PKHG.1jun12 the foregoing line causes strange behavior!
        if self.with_name:
            Morph.draw_string_to_viewport(self.name, self, size , (1,1,1,1), font_id, x , y)
        if debug_color and self.name == "toggle editing: LM-click!":
            tmp = [self]
            tmp.extend(self.children[:])
            print(">....color debug draw in morph\nself and chidren",tmp)
            tmpcol = [el.color for el in tmp]
            print("their color = ", tmpcol)
            print(debug_color)
            debug_color -=1

    def hide(self):
        """hide me and all my children"""
        self.is_visible = False
        self.changed()
#        print("*INFO PKHG* hide in morph.py L302:   how to do hide now??? self =", self, type(self) )
#        return
        ##PKHG.??? needed?
        for morph in self.children:
            morph.hide()

    def show(self):
        """show me and all my children"""
        self.is_visible = True
        self.changed()
        for morph in self.children:
            morph.show()

    def toggle_visibility(self):
        """ toggle between visible and invisible"""
        self.is_visible = not self.is_visible
        self.changed()
        for morph in self.children:
            morph.toggle_visibility()

    #Morph updating:

    def changed(self):
        """event called when morph is changed"""
        w = self.get_root() #PKHG recursive parent of self
        if debug_changed_130512_0810:
            print("changed_130512_0810 morph.py, root of", self,"is", w)
        '''
        if isinstance(w, World):
            w.broken.append(copy.copy(self.bounds))
            if debug_changed_130512_0810:
                print("debug_changed_130512_0810 changed, self.bounds saved in world", self.bounds)
        '''


    def get_world(self):
        """ getter : gets the world """
        if isinstance(self.root(), World):
            return self.root()

    def add(self, morph):
        """ add a morph as a child"""
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
        """ getter (Point) : return the moprh that is located in a specific Point"""
        morphs = self.get_all_children()
        for m in morphs[::-1]:
            if m.get_full_bounds().get_contains_point(point):
                return m

    #Morph duplicating:

    def full_copy(self):
        """ make a full copy of the morphs with all its children"""
        new = copy.copy(self)
        lst = []
        for m in self.children:
            new_child = m.full_copy()
            new_child.parent = new
            lst.append(new_child)
        new.children = lst
        return new


    #Morph dragging and dropping:

    def get_root_for_grab(self):
        """ getter: get the world of the morph"""
        if self.parent == None or isinstance(self.parent, Frame):
            return self
        else:
            return self.parent.get_root_for_grab()

    def get_wants_drop_of(self, morph):
        """ getter : Returns whethere the morph wants to drop or not. Default is False - change for subclasses """
        return False


    #Morph events:

    def get_handles_mouse_over(self):
        """ getter : Returns True or False for whether the morphs handles mouse_over events"""
        return False

    def get_handles_mouse_click(self):
        """ getter : Returns True or False for whether the morphs handles mouse_clicks events"""
        return False

    def get_handles_mouse_move(self):
        """ getter : Returns True or False for whether the morphs handles mouse_move events """
        return False

    def mouse_down_left(self, pos):
        """ Event method to be called when the left mouse button is pressed"""
        pass

    def mouse_up_left(self, pos):
        """ Event method to be called when the left mouse button is released"""
        pass

    def mouse_click_left(self, pos):
        """ Event method to be called when the left mouse button is pressed and released"""
        pass


    def mouse_down_middle(self, pos):
        """ Event method to be called when the middle  mouse button is pressed """
        pass

    def mouse_up_middle(self, pos):
        """ Event method to be called when the middle mouse button is released"""
        pass

    def mouse_click_middle(self, pos):
        """ Event method to be called when the middlle mouse button is pressed and released"""
        pass

    def mouse_down_right(self, pos):
        """ Event method to be called when the right mouse button is pressed"""
        pass

    def mouse_up_right(self, pos):
        """ Event method to be called when the right mouse button is released"""
        pass

    def mouse_click_right(self, pos):
        """ Event method to be called when the right mouse button is pressed and released"""
        pass

    def mouse_enter(self):
        """ Event method to be called when the mouse cursor enters the bounts of the morph"""
        pass

    def mouse_enter_dragging(self):
        pass

    def mouse_leave(self):
        """ Event method to be called when the mouse cursor exits the bounts of the morph"""
        pass

    def mouse_leave_dragging(self):
        pass

    def mouse_move(self,pos):
        """ Event method to be called when the mouse cursor tried to move the moprh"""
        pass

    def key_press(self,event):
        """ event method trigger when a key is pressed while morph has focus, returns True only if the event is processed"""
        return False

    def key_release(self,event):
        """ event methode triggered when a key is released while morph has focus, returns True only if the event is processed"""
        return False

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

    def draw_line(self,f_x,f_y,t_x,t_y, line_width = 2, color = (0,0,0,1)):
        """Draw a line from (f_x,f_y) to (t_x,t_y), width and color"""
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glColor4f(*color)
        bgl.glLineWidth(line_width)
        bgl.glBegin(bgl.GL_LINES)
        bgl.glVertex2f(f_x, f_y)
        bgl.glVertex2f(t_x, t_y)
        bgl.glEnd()

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
