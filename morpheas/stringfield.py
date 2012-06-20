from .morph import *
from .rectangle import *

import addon_utils
import re

#PKHG for Blinker we need time-measurments
import time
from time import time

re_CAS = re.compile("^(LEFT|RIGHT)_CTRL$|^(LEFT|RIGHT)_ALT$|^(LEFT|RIGHT)_SHIFT$")

#re_LEFT_ARROW = re.compile(" \*LEFT_ARR0W\* *$")
#re_RIGHT_ARROW = re.compile(" \*RIGHT_ARR0W\* *$")
re_RL_ARROW = re.compile(" \*(LEFT|RIGHT)_ARROW\*  *$")
class OneLineText(Morph):
    """I am a single line to input text, NEEDS an owner with kbd_listener"""

    def __init__(self, owner = None,
                 text = "",
#                 fontname="verdana.ttf",
#                 fontsize=12,
#                 bold=False,
#                 italic=False
                 ):
        super(OneLineText, self).__init__()
        self.owner = owner
        self.blinker = self.owner.blinker
#        print("\n>>>>>> owners blinker",self.owner.blinker)
#PKHGOK        print(">>>>>>>>>>> OneLineText root of owner ",owner.get_root(),owner.hand)
        self.text = text
#        self.fontname = "verdana.ttf" #fontname
        self.fontsize =  12 #fontsize
        self.bold = False #bold
        self.italic = False #italic
        self.is_editable = False
        self.width = 10
#        super(OneLineText, self).__init__()
        self.color = (1, 1, 1, 1)
        tmp = addon_utils.paths()[0] + "/Ephestos/fonts/verdana.ttf"# + fontname
        self.font = blf.load(tmp)
#PKHG.TODO DPI = ???
        blf.size(self.font, self.fontsize, 72) #DPI default 72?
        self.kbd_listener = self.owner.kbd_listener
        self.list_of_char_x_values =[]
        self.nr_of_chars = 0

    def __repr__(self):
        return 'OneLineText("' + self.text + '")'

    def draw(self):
        """draw, if visible, my text"""

        tmp = self.kbd_listener.text_input
        #tmp2 = re_LEFT_ARROW.search(tmp)
        res = re_RL_ARROW.search(tmp)
        if res:
            tmp2 = " *" + res.group(1) + "_ARROW* "
            tmp = tmp.replace(res.group(),"<=>")
        self.text = tmp
        self.kbd_listener.text_input = tmp
        t_width, t_height  = blf.dimensions(self.font, self.text)
        self.width = int(t_width + 2.0)
#        if self.is_editable:
        corner = Point(self.width, 2 + int(t_height))
        self.bounds.corner = self.bounds.origin + corner
        x = self.bounds.origin.x + 1
        y = self.bounds.origin.y + 1
        bgl.glColor4f(*self.color)
        blf.position(self.font,x ,y, 0) #PKHG.??? 0 is z-depth?!
        if self.is_visible:
#            origin = self.blinker.bounds.origin
#            new_origin = origin + Point(int(t_width),0)
            self.blinker.set_position(Point(x + int(t_width + 1), y))
            blf.draw(self.font, self.text)

    def get_width(self):
        """ the width of the text at actual font-size"""
        return self.width

#    def place_blinker(self, x, y,  dx):
#        return Point(x + dx, y)


    #OneLineText menu:

    def add_keystroke(self):
        pass

    '''
    def developers_menu(self):
        menu = super(OneLineText, self).developers_menu()
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
    '''

    def edit(self):
        """change text for each kbd-release"""
        tmp = self.kbd_listener.text_input
        if re_LEFT_ARROW(tmp):
            tmp.replace(" *LEFT_ARR0W* ","<=")
        self.text = tmp #self.kbd_listener.text_input
        print("///////////////OneLineText L85: I am about to be edited")
        return

###### PKHG TODO font-stuff ##############33
    '''
    def choose_font(self):
        fontname = world.fontname_by_user()
        if fontname != None:
            self.fontname = fontname
            self.changed()
            self.draw()
            self.changed()

    def choose_font_size(self):
        fontsize = self.prompt("please enter\n the font size\nin points:",
                               str(self.fontsize),
                               50)
        if fontsize != None:
            self.fontsize = int(fontsize)
            self.changed()
            self.draw()
            self.changed()

    def set_to_normal(self):
        self.bold = False
        self.italic = False
        self.changed()
        self.draw()
        self.changed()

    def set_to_bold(self):
        self.bold = True
        self.changed()
        self.draw()
        self.changed()

    def set_to_italic(self):
        self.italic = True
        self.changed()
        self.draw()
        self.changed()
    '''

    #OneLineText events:

    def handles_mouse_click(self):
        return True
#        return self.is_editable

    def mouse_click_left(self, pos):
        print("onelinetext.mouse_click_left (stringfield.py L132) called")
        pass
        return
########???????? does someone else?
        self.edit()
        #PKHG not implemented ...
        world.text_cursor.goto_pos(pos)


class StringInput( Morph):
    """StringInput is used to get/show a one-line input text-string"""

    def __init__(self, hand, blinker,  default='I am the default',
                 minwidth=100,
                 fontname="verdana.ttf",
                 fontsize=12,
                 bold=False,
                 italic=False):
        self.hand = hand
        self.blinker = blinker
        self.kbd_listener = hand.kbd_listener
        super(StringInput, self).__init__()
        self.default = default
        self.minwidth = minwidth
        self.fontname = fontname
        self.fontsize = fontsize
        self.bold = bold
        self.italic = italic
#        self.color = (0.1, 0.1, 0.1, 0.1)
        self.set_color((0.1, 0.1, 0.1, 0.1))
        #onlinetext needs a keyboardlistener! thus
        self.onelinetext = OneLineText(self, self.default)#,\
#                 self.fontname, self.fontsize, self.bold, self.italic)
        self.add(self.onelinetext)
        self.onelinetext.set_position(self.get_bottom_left() + 5)
        self.is_activated = False
        self.activation_info = Morph(bounds = Rectangle(Point(0,0),Point(20,20)), with_name = True)
        self.activation_info.name = "active"
        self.activation_info.set_position(self.bounds.corner)
        self.activation_info.is_visible = False
        self.activation_info.set_color("green")
        self.add(self.activation_info)

    def draw(self):
        "draw and adjust size of morph, input_text dependant"
#        super(StringInput, self).draw()
#        self.onelinetext.draw()
        input_width = self.onelinetext.width + 5 #PKHG because of offset onelinetext
        if input_width < 100:
            dif = 0
            self.minwidth = 100
        else:
            dif = input_width - self.get_width()

        if dif > 0:
            new_corner = self.bounds.corner + Point(dif,0)
            self.bounds = Rectangle(self.bounds.origin, new_corner)
        elif dif < 0:
            x = self.bounds.origin.x
            y = self.bounds.corner.y
            if input_width < 100:

                self.bounds = Rectangle(self.bounds.origin, Point(x + 100, y))
            else:
                self.bounds = Rectangle(self.bounds.origin,Point(x + input_width, y))
        children = self.children
#PKHG.??? next lines really needed?

#        for child in children:
#            if child.is_visible:
#                child.draw()

        super(StringInput, self).draw()
        if self.activation_info.is_visible:
            self.activation_info.draw()
        self.onelinetext.draw()

        x = self.bounds.origin.x + 1
        y = self.bounds.origin.y + 1
        self.blinker.set_position(Point(x + input_width, y))
        self.blinker.draw()
        return

    def get_string(self):
        """ getter of input-text at THIS moment"""
        return self.text.text

    def get_handles_mouse_click(self):
#dbg    print("\n\n get_handles_mouse_click called in StringInput.py")
        return True

    def mouse_click_left(self, pos):
        """start editing of text via a mouse-click"""
        self.is_activated = not self.is_activated
#        print("\n>>>>>> StringInput.py L210 mouse_click_left is_editable", self.is_activated)

    def mouse_enter(self):
        self.is_activated = True
        self.onelinetext.is_editable = True
        self.kbd_listener.users += 1
        self.activation_info.is_visible = True #PKHG???False

    def mouse_leave(self):
        self.is_activated = False
        self.kbd_listener.users -= 1
        self.onelinetext.is_editable = False
        self.activation_info.is_visible = False #PKHG???False


    def key_release(self,event):
#PKHG.TODO what to do with RET ... and arrow and Page-down etc???
        if True: #event.type in {'RET','NUMPAD_ENTER'}:
            tmp = self.kbd_listener.text_input
            self.insert_committed_text(tmp)
            self.onelinetext.text = tmp
        #    set_Info_input(tmp, False)
#PKHG.attention  return used:
        return {'RUNNING_MODAL'} #keys eaton up


    def insert_committed_text(self, text):
           print("StringInput.insert_committed_text (L241) text = ", text)

class Blinker(Morph):
    "can be used for text cursors"

    def __init__(self, rate=0.2):
        super(Blinker, self).__init__()
        self.color = (1.0, 0, 0, .8)
        self.fps = rate
        self.name = "Blinker"
        self.bounds = Rectangle(Point(0,0),Point(3,20))
        self.start_time = time()
        self.time_now = time()
        self.draw() #PKHG must be later then start_time and time_now

    def wants_to_step(self):
        return True

    def step(self):
        self.time_now = time()
        if (self.time_now - self.start_time) > self.fps :
#            self.toggle_visibility()
            self.start_time = self.time_now
            if self.color[0] == 1.0:
                self.set_color((0, 1.0, 0, 0.7))
            else:
                self.set_color((1.0, 0, 0, 0.7))

    def draw(self):
        self.step()
       # bgl.glEnable(bgl.GL_BLEND) #PKHG.??? needed?
        bgl.glColor4f(*self.color)
        [x,y] = [self.get_position().x, self.get_position().y]
#        dimensions = self.get_extent().as_list()
        #if self.rounded:
        #    Morph.draw_rounded_morph(self, 0.3, self.color, rectangle = False)
        #else:
        bgl.glRecti(x, y, x + 3, y + 20)
