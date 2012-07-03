from .morph import *
from .rectangle import *

import addon_utils

#PKHG for Blinker we need time-measurements
from time import time

import re
#re_CAS = re.compile("^(LEFT|RIGHT)_CTRL$|^(LEFT|RIGHT)_ALT$|^(LEFT|RIGHT)_SHIFT$")
#re_LEFT_ARROW = re.compile(" \*LEFT_ARR0W\* *$")
#re_RIGHT_ARROW = re.compile(" \*RIGHT_ARR0W\* *$")
re_RL_ARROW = re.compile(" \*(LEFT|RIGHT)_ARROW\*  *$")
class OneLineText(Morph):
    """I am a single line to input text, NEEDS an owner with kbd_listener"""

    def __init__(self, owner = None,
                 text = ""):
        super(OneLineText, self).__init__()        
        self.owner = owner
        self.text = text
        self.fontsize =  12 #fontsize
        self.bold = False   #bold
        self.italic = False #italic
        self.width = 10
        #PKHG 3006512 name is written always in WHITE and name is used!
        #PKHG only verdana.ttf used
        tmp = addon_utils.paths()[0] + "/Ephestos/fonts/verdana.ttf"
        self.font = blf.load(tmp)
        blf.size(self.font, self.fontsize, 72) #DPI default 72?
        self.kbd_listener = self.owner.kbd_listener
        self.list_of_char_x_values =[]
        self.nr_of_chars = 0
        self.nr_chars_old = 0
#        self.color = owner.color #PKHG>3jul????
        
    def __repr__(self):
        return 'OneLineText("' + self.text + '")'

    def draw(self):
        """draw, if visible, my text"""
        if len(self.kbd_listener.text_input) !=  self.nr_of_chars:
            self.add_keystroke()
        t_width, t_height  = blf.dimensions(self.font, self.text)
        self.width = int(t_width + 2.0)
        corner = Point(self.width, 2 + int(t_height))
        self.bounds.corner = self.bounds.origin + corner
        x = self.bounds.origin.x + 1
        y = self.bounds.origin.y + 1
        bgl.glColor4f(1.0, 1.0, 1.0, 1.0) #PKHG: 28jun12 always white
        blf.position(self.font,x ,y, 0)   #PKHG.??? 0 is z-depth?!
        if self.is_visible:
            self.owner.blinker.set_position(Point(x + int(t_width + 1), y - 1))
            blf.draw(self.font, self.text)
            mouse_location = Point(self.owner.hand.mouse_x, self.owner.hand.mouse_y)
            #PKHG is show_all is pressed set me to invisible!
            if not self.owner.bounds.get_contains_point(mouse_location):
                self.owner.activation_info.is_visible = False            
            text_end_location = self.bounds.get_bottom_right()
            
    def get_width(self):
        """ the width of the text at actual font-size"""
        return self.width


    #OneLineText menu:

    def add_keystroke(self):
        tmp = self.kbd_listener.text_input        
        res = re_RL_ARROW.search(tmp)
        if res:
            tmp2 = " *" + res.group(1) + "_ARROW* "
            tmp = tmp.replace(res.group(),"<=>")
            self.kbd_listener.text_input = tmp
        if self.nr_chars_old < self.nr_of_chars:
            dif = self.nr_of_chars - self.nr_chars_old
            nn = tmp[-dif:]
            self.text += tmp[-dif:]
            self.nr_chars_old = len(self.text)
        else:
            self.text = tmp
            self.nr_chars_old = len(tmp)
        self.nr_of_chars = len(self.text)
            

class StringInput( Morph):
    """StringInput is used to get/show a one-line input text-string"""

    def __init__(self, hand, blinker,  default='I am the default',
                 minwidth=100,
                 fontname="verdana.ttf",
                 fontsize=12,
                 bold=False,
                 italic=False):
        super(StringInput, self).__init__()
        self.activated = False
        self.hand = hand
        self.blinker = blinker
        self.kbd_listener = hand.kbd_listener
        self.default = default
        self.minwidth = minwidth
        self.fontname = fontname
        self.fontsize = fontsize
        self.bold = bold
        self.italic = italic
#        self.color = (0.9, 0.1, 0.1, 1) #??? why standard color? shown????
#????        self.set_color((0.1, 0.1, 0.1, 0.1)) #PKHG??? 25-06-12
        #onlinetext needs a keyboardlistener! thus
        self.onelinetext = OneLineText(self, self.default)#,\
#                 self.fontname, self.fontsize, self.bold, self.italic)
        self.add(self.onelinetext)
        self.add(blinker) #PKHG>??? 3jul        
        self.onelinetext.set_position(self.get_bottom_left() + 5)
        self.is_activated = False
        self.activation_info = Morph(bounds = Rectangle(Point(0,0),Point(20,20)), with_name = False)
        self.activation_info.set_position(self.bounds.origin - Point(0,25)) 
        self.activation_info.is_visible = False
        self.activation_info.set_color("red")
        self.add(self.activation_info)

    def draw(self):
        "draw and adjust size of morph, input_text dependant"
        
        super(StringInput, self).draw()
#PKHG>??? why not possible???        print("\n????? color super",super(StringInput,self).color)
        input_width = self.onelinetext.width + 5
        #+ 5 PKHG because of offset onelinetext
        if input_width < 100:
            dif = -1 #PKHG 0 was wrong!
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
        x = self.bounds.origin.x + 1
        y = self.bounds.origin.y + 1
        self.activation_info.draw()
        self.onelinetext.draw()

        if self.activated:
#            print("\n\n\n++++ active+++")
            self.activation_info.set_color("green")
            self.blinker.set_position(Point(x + input_width, y))
            self.blinker.is_visible = True
        else:
#            print("\n\n\n---- INACTIVE")
            self.activation_info.set_color("red")
            self.blinker.is_visible = False            
        
    def get_string(self):
        """ getter of input-text at THIS moment"""
        return self.text.text

    def get_handles_mouse_click(self):
#dbg    print("\n\n get_handles_mouse_click called in StringInput.py")
        return True

    def mouse_click_left(self, pos):
        """??? not used PKHG start editing of text via a mouse-click"""
        pass

    def mouse_enter(self):
        self.activated = True
        self.onelinetext.is_visible = True
        self.kbd_listener.users += 1

    def mouse_leave(self):
        self.activated = False
        self.kbd_listener.users -= 1
        self.onelinetext.is_visble = False

########PKHG.TODO what to do with RET ... and arrow and Page-down etc???
    def key_release(self,event): 
        if True: #event.type in {'RET','NUMPAD_ENTER'}:
            tmp = self.kbd_listener.text_input
#            self.insert_committed_text(tmp)
            self.onelinetext.text = tmp
        return {'RUNNING_MODAL'} #PKHG.attention  return used: keys eaton up


    def insert_committed_text(self, text):
        print("StringInput.insert_committed_text (L241) text = ", text)
        pass

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
    
    def step(self):
        """make it blinking by changing color, fps dependant"""
        if not self.is_visible:
            return
        self.time_now = time()
        if (self.time_now - self.start_time) > self.fps :
            self.start_time = self.time_now
            if self.color[0] == 1.0:
                self.set_color((0, 1.0, 0, 0.7))
            else:
                self.set_color((1.0, 0, 0, 0.7))
    
    
    def draw(self):
        """set the blinkers layout"""
        self.step()
        bgl.glColor4f(*self.color) #PKHG color changed by timedepedant step!
        [x,y] = [self.get_position().x, self.get_position().y]
        bgl.glRecti(x, y, x + 3, y + 20) #PKHG of blinker:(0,0) x (3,20)
