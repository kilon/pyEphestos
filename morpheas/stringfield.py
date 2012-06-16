from .morph import *
from .rectangle import *

import addon_utils
import re

re_CAS = re.compile("^(LEFT|RIGHT)_CTRL$|^(LEFT|RIGHT)_ALT$|^(LEFT|RIGHT)_SHIFT$")


class OneLineText(Morph):
    """I am a single line to input text, NEEDS an owner with kbd_listener"""
                      
    def __init__(self, owner = None,
                 text = "",
                 fontname="verdana.ttf",
                 fontsize=12,
                 bold=False,
                 italic=False):
        super(OneLineText, self).__init__()
#PKHG.OK         print("OneLineText created = ", text)
        self.owner = owner
        self.text = text
        self.fontname = fontname
        self.fontsize=fontsize
        self.bold = bold
        self.italic = italic
        self.is_editable = False
        self.width = 10
#        super(OneLineText, self).__init__()
        self.color = (1, 1, 1, 1) 
        tmp = addon_utils.paths()[0] + "/Ephestos/fonts/" + fontname
        self.font = blf.load(tmp)
#PKHG.TODO DPI = ???        
        blf.size(self.font, self.fontsize, 72) #DPI default 72?
        self.kbd_listener = self.owner.kbd_listener
        
    def __repr__(self):
        return 'OneLineText("' + self.text + '")'

    def draw(self):
        """draw, if visible, my text"""
    
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
            blf.draw(self.font, self.text)
    
    def get_width(self):
        """ the width of the text at actual font-size"""
        return self.width
    
    #OneLineText menu:

    def add_keystroke(self):
        pass
        
    
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

    def edit(self):
        """change text for each kbd-releas"""
        
        self.text = self.kbd_listener.text_input
        print("///////////////OneLineText L85: I am about to be edited")
        return

###### PKHG TODO font-stuff ##############33
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


class StringField( Morph):
    """StringField is used to get/show a one-line input text-string"""
    
    def __init__(self, kbd_listener = None, default='I am the default',
                 minwidth=100,
                 fontname="verdana.ttf",
                 fontsize=12,
                 bold=False,
                 italic=False):
        
        self.kbd_listener = kbd_listener
        super(StringField, self).__init__()
        self.default = default
        self.minwidth = minwidth
        self.fontname = fontname
        self.fontsize = fontsize
        self.bold = bold
        self.italic = italic
        self.color = (0.1, 0.1, 0.1, 0.1)
        #onlinetext needs a keyboardlistener! thus
        self.onelinetext = OneLineText(self, self.default,\
                 self.fontname, self.fontsize, self.bold, self.italic)
        self.add(self.onelinetext)
        self.is_activated = False
        self.activation_info = Morph(bounds = Rectangle(Point(0,0),Point(20,20)), with_name = True)
        self.activation_info.name = "active"
        self.activation_info.set_position(self.bounds.corner)
        self.activation_info.is_visible = False
        self.activation_info.set_color("green")
        self.add(self.activation_info)        

    def draw(self):
        "draw and adjust size of morph, input_text dependant"
        super(StringField, self).draw()
        self.onelinetext.draw()

        input_width = self.onelinetext.width
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
        for child in children:
            if child.is_visible:
                child.draw()        
        super(StringField, self).draw()
        self.onelinetext.draw()                 
        return 

    def get_string(self):
        """ getter of input-text at THIS moment"""
        return self.text.text

    def get_handles_mouse_click(self):
#dbg    print("\n\n get_handles_mouse_click called in stringfield.py")
        return True

    def mouse_click_left(self, pos):
        """start editing of text via a mouse-click"""
        self.is_activated = not self.is_activated
        print("\n>>>>>> stringfield.py L210 mouse_click_left is_editable", self.is_activated)
        '''
        if self.is_activated:
            self.onelinetext.edit()
            self.onelinetext.is_editable = True
            self.activation_info.is_visible = False #PKHG???True
        else:
            self.onelinetext.is_editable = False
            self.activation_info.is_visible = True #PKHG???False
          '''
        
    def mouse_enter(self):
        self.is_activated = True
        self.onelinetext.is_editable = True
        self.activation_info.is_visible = True #PKHG???False
        
    def mouse_leave(self):
        self.is_activated = False
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
           print("StringField.insert_committed_text (stringfield.py L241) text = ", text)
