from .morph import *
from .rectangle import *
import addon_utils
#PKHG for Blinker we need time-measurements
from time import time

import re
#### maybe other re's ??? to be used
#re_CAS = re.compile("^(LEFT|RIGHT)_CTRL$|^(LEFT|RIGHT)_ALT$|^(LEFT|RIGHT)_SHIFT$")
#re_LEFT_ARROW = re.compile(" \*LEFT_ARR0W\* *$")
#re_RIGHT_ARROW = re.compile(" \*RIGHT_ARR0W\* *$")

re_RL_ARROW = re.compile(" \*(LEFT|RIGHT)_ARROW\*  *$")

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
        bgl.glColor4f(*self.color) #PKHG color changed by timedependant step!
        [x,y] = [self.get_position().x, self.get_position().y]
        bgl.glRecti(x, y, x + 3, y + 20) #PKHG of blinker:(0,0) x (3,20)

class StringInput(Morph):
    def __init__(self, hand, blinker,  default='mouse here to activates me',
                 fontname="verdana.ttf",
                 fontsize=12,
                 bold=False,
                 italic=False):
        bounds = Rectangle(Point(0,0),Point(800,30))
        super(StringInput, self).__init__(bounds = bounds)
        tmp = addon_utils.paths()[0] + "/Ephestos/fonts/verdana.ttf"
        self.font = blf.load(tmp)
        self.info = default
        self.activated = False
        self.hand = hand
        self.blinker = blinker
        self.kbd_listener = hand.kbd_listener
        self.default = default
        self.fontname = fontname
        self.fontsize = fontsize
        self.bold = bold
        self.italic = italic
#        self.color = (0.9, 0.1, 0.1, 1) #??? why standard color? shown????
        self.add(blinker) #PKHG>??? 3jul, yes wanted ...        
        self.is_activated = False
        self.activation_info = Morph(bounds = Rectangle(Point(0,0),Point(20,20)), with_name = False)
        self.activation_info.set_position(self.bounds.origin - Point(0,25)) 
        self.activation_info.is_visible = False
        self.activation_info.set_color("red")
        self.add(self.activation_info)
        self.relative_pos_of_chars = [0]
        self.mouse_click_left_toggle = False
        self.prefix = ""
        self.postfix = ""
        self.text = ""
        self.width = 0

    def draw(self):
        """StringInput draw and adjust size of morph, input_text dependant"""
#PKHG NO! super(...).draw()!!!

#        bgl.glColor4f(*self.color) #PKHG color changed by timedependant step!
        bgl.glColor4f(0.6, 0.6, 0.3, 1) #PKHG color changed by timedependant step!
        [x,y] = [self.get_position().x, self.get_position().y]
        bgl.glRecti(x, y, x + self.width + 20, y + 25) #PKHG of blinker:(0,0) x (3,20)        
        self.blinker.draw()
        x = self.bounds.origin.x + 1
        y = self.bounds.origin.y + 1
        self.activation_info.draw()
        if self.activation_info.color == (0, 0, 1, 1): #blue => insert mode
            mouse_x = self.hand.mouse_x
            if self.postfix == "": #start of inser?
                text_now = self.hand.kbd_listener.text_input
                len_text_now = len(text_now)
                tmp = ""
                for i in range(len_text_now):
                    tmp += text_now[i]
                    t_width, t_height  = blf.dimensions(self.font, tmp)
                    if (x + int(t_width) + 7) > mouse_x:
                        self.prefix = tmp
                        self.postfix = text_now[i + 1:]
                        break
                self.hand.kbd_listener.text_input = tmp
            
#            print("\n now blue action>", self.prefix,"<>", self.postfix,"<")
            text =  self.kbd_listener.text_input
            t_width, t_height  = blf.dimensions(self.font, text)
            self.width = int(t_width + 2.0)
            x = self.bounds.origin.x + 2
            y = self.bounds.origin.y + 2
            bgl.glColor4f(1.0, 1.0, 1.0, 1.0) #PKHG: 28jun12 always white
            blf.position(self.font,x ,y, 0)   #PKHG.??? 0 is z-depth?!
            if self.is_visible:
                self.blinker.set_position(Point(x + int(t_width + 1), y - 1))
                blf.draw(self.font, text + self.postfix) #PKHG>test 12-7-2012
                mouse_location = Point(self.hand.mouse_x, self.hand.mouse_y)
                #PKHG is show_all is pressed set me to invisible!
                if not self.bounds.get_contains_point(mouse_location):
                    self.activation_info.is_visible = False            
            
        else: # elif self.activation_info.color == (0, 1, 0, 1): #green normal
            if len(self.postfix) > 0:
                self.kbd_listener.text_input += self.postfix
                self.postfix = ""
                self.prefix = ""
                #back to normal processing
            text =  self.kbd_listener.text_input
            t_width, t_height  = blf.dimensions(self.font, text)
            self.width = int(t_width + 2.0)
            x = self.bounds.origin.x + 2
            y = self.bounds.origin.y + 2
            bgl.glColor4f(1.0, 1.0, 1.0, 1.0) #PKHG: 28jun12 always white
            blf.position(self.font,x ,y, 0)   #PKHG.??? 0 is z-depth?!
            if self.is_visible:
                self.blinker.set_position(Point(x + int(t_width + 1), y - 1))
                blf.draw(self.font, text)
                mouse_location = Point(self.hand.mouse_x, self.hand.mouse_y)
                #PKHG is show_all is pressed set me to invisible!
                if not self.bounds.get_contains_point(mouse_location):
                    self.activation_info.is_visible = False            
    #PKHG.not yet used
    #            text_length_on_sreen  = self.bounds.get_width() - 2
    
        if self.activated:
#            print("\n\n\n++++ active+++")
            if self.activation_info.color == (1, 0, 0, 1): #red
                self.activation_info.set_color("green")
            if self.activation_info.color == (0, 0, 1, 1): #blue insertmode
                if self.postfix:
                    self.blinker.set_position(Point(x + self.width, y))
                else:
                    self.blinker.set_position(Point(self.hand.mouse_x, y))
            else: #green
                self.blinker.set_position(Point(x + self.width, y))
            self.blinker.is_visible = True
        else:
#            print("\n\n\n---- INACTIVE")
            t_width, t_height  = blf.dimensions(self.font, text)
            bgl.glColor4f(0, 1, 0, 1) #green
            blf.position(self.font,x ,y + 25 , 0)   #PKHG.??? 0 is z-depth?!
            blf.draw(self.font, self.default)
            self.activation_info.set_color("red")
            self.blinker.is_visible = False            
        self.text = self.hand.kbd_listener.text_input
        
    def get_string(self):
        """ getter of input-text at THIS moment"""
        return self.text

    def get_handles_mouse_click(self):
#        print("\n\n>>>stringfield L162 get_handles_mouse_click called in StringInput.py")
        return True

#PKHG 07jul12 TODO using blinker!
    def mouse_click_left(self, pos):
        """??? not used PKHG start editing of text via a mouse-click"""
        ####### test and info########
        self.mouse_click_left_toggle = not self.mouse_click_left_toggle
        if self.mouse_click_left_toggle:
            mouse_position = pos
            self.activation_info.set_color('blue')
        else:
            self.activation_info.set_color('green')
        ####### test end ############33
        pass

    def mouse_enter(self):
        self.activated = True
        self.kbd_listener.users += 1

    def mouse_leave(self):
        self.activated = False
        self.kbd_listener.users -= 1

########PKHG.TODO what to do with RET ... and arrow and Page-down etc???
    def key_release(self,event): 
#PKHG.TODO???        if True: #event.type in {'RET','NUMPAD_ENTER'}:
        tmp = self.kbd_listener.text_input
#        self.insert_committed_text(tmp)
#        print("stringfield key_release", tmp)
        return {'RUNNING_MODAL'} #PKHG.attention  return used: keys eaton up


    def insert_committed_text(self, text):
        print("StringInput.insert_committed_text (L217) text = ", text)
        pass
