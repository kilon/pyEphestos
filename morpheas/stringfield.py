from .morph import *
from .rectangle import *

import addon_utils
import re

class String(Morph):
    "I am a single line of text"
                      
    def __init__(self,
                 text,
                 fontname="verdana.ttf",
                 fontsize=12,
                 bold=False,
                 italic=False):
        super(String, self).__init__()
#PKHG.OK         print("String created = ", text)
        self.text = text
        self.fontname = fontname
        self.fontsize=fontsize
        self.bold = bold
        self.italic = italic
        self.is_editable = False
        super(String, self).__init__()
        self.color = (1,1,1,1)
        tmp = addon_utils.paths()[0] + "/Ephestos/fonts/" + fontname
        self.font = blf.load(tmp)
#PKHG.TODO DPI = ???        
        blf.size(self.font, self.fontsize, 72) #DPI default 72?        

        
    def __repr__(self):
        return 'String("' + self.text + '")'

    def draw(self):
        '''
        self.font = pygame.font.SysFont(
            self.fontname,
            self.fontsize,
            self.bold,
            self.italic)
        '''
        t_width, t_height  = blf.dimensions(self.font, self.text)
        self.width = int(t_width + 2.0)
#        self.image = self.font.render(self.text, 1, self.color)
#        self.image.set_alpha(self.alpha)
#        corner = Point(self.image.get_width(),
#                                   self.image.get_height())
        corner = Point(self.width, 2 + int(t_height))
        self.bounds.corner = self.bounds.origin + corner
        x = self.bounds.origin.x + 1
        y = self.bounds.origin.y + 1
#        bgl.glEnable(bgl.GL_BLEND)
        bgl.glColor4f(*self.color)
        blf.position(self.font,x ,y, 0) #PKHG.??? 0 is z-depth?!
        if self.is_visible:

            blf.draw(self.font, self.text)
    
    def get_width(self):
        return self.width
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

    #String events:

    def handles_mouse_click(self):
        return self.is_editable

    def mouse_click_left(self, pos):
        self.edit()
        world.text_cursor.goto_pos(pos)



class StringField( Morph):
    """StringField is used to get a one-line input text-string"""
    
    def __init__(self, default='I am the default',
                 minwidth=100,
                 fontname="verdana.ttf",
                 fontsize=12,
                 bold=False,
                 italic=False):
        

        super(StringField, self).__init__()
        self.default = default
        self.minwidth = minwidth
        self.fontname = fontname
        self.fontsize = fontsize
        self.bold = bold
        self.italic = italic
        self.color = (1.0, 0.0, 1.0, 0.5) 
        self.text_string = String(self.default, self.fontname, self.fontsize,\
                           self.bold, self.italic)
        self.add(self.text_string)
        self.re_CAS = re.compile("^(LEFT|RIGHT)_CTRL$|^(LEFT|RIGHT)_ALT$|^(LEFT|RIGHT)_SHIFT$")

        self.used_keyboard_dict_for_digits = { 'ONE':'1', 'ONE_SHIFT':'!', 'TWO':'2', \
     'TWO_SHIFT':'@', 'THREE':'3', 'THREE_SHIFT':'#', 'FOUR':'4',\
     'FOUR_SHIFT':'$', 'FIVE':'5', 'FIVE_SHIFT':'%', 'SIX':'6',\
     'SIX_SHIFT':'^', 'SEVEN':'7', 'SEVEN_SHIFT':'&', 'EIGHT':'8',\
     'EIGHT_SHIFT':'*', 'NINE':'9', 'NINE_SHIFT':'(', 'ZERO':')', \
     'MINUS':'-', 'MINUS_SHIFT':'_', 'EQUAL':'=', 'EQUAL_SHIFT':'+',
     'ACCENT_GRAVE':'`', 'ACCENT_GRAVE_SHIFT':'~',\
     'COMMA':',', 'COMMA_SHIFT':'<', 'PERIOD':'.', 'PERIOD_SHIFT':'>',\
     'SLASH':'/', 'SLASH_SHIFT':'?', 'SEMI_COLON':';', 'SEMI_COLON_SHIFT':':',\
     'QUOTE':"'", 'QUOTE_SHIFT':'"', 'TAB':'\t', 'BACK_SLASH':'\\',
     'BACK_SLASH_SHIFT':'|', 'LEFT_BRACKET':'[', 'LEFT_BRACKET_SHIFT':'{',\
     'RIGHT_BRACKET':']', 'RIGHT_BRACKET_SHIFT':'}'}
     

        self.numpad_dict_specials = {'NUMPAD_PERIOD':'.', 'NUMPAD_SLASH':'/',\
     'NUMPAD_ASTERIX':'*',  'NUMPAD_MINUS':'-',  'NUMPAD_PLUS':'+'}
        self.delete_list= ['DEL','BACK_SPACE']


    def draw(self):
        "initialize my surface"
        super(StringField, self).draw()
        self.text_string.draw()

        input_width = self.text_string.width
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

        for child in children:
            if child.is_visible:

                child.draw()
        
        super(StringField, self).draw()
        self.text_string.draw()
                
        return 
        ''' 
        self.text = None
        for m in self.children:
#PKHG.todo            m.delete()
            print("DBG === draw_new(stringfield) === ? should be deleted?  m ", m) 
        self.children = []
        self.text = String(self.default, self.fontname, self.fontsize,\
                           self.bold, self.italic)
        self.text.is_editable = True
        self.text.is_draggable = False
        self.set_extent(Point(self.minwidth, self.text.height()))
        self.text.set_position(self.position())
        self.add(self.text)
        self.text.draw_new()
        '''

    def get_string(self):
        return self.text.text

    def get_handles_mouse_click(self):
        return False

    def mouse_click_left(self, pos):
        self.text_string.edit()
    
    """ I dont think this function is needed , will need to invistigate further     
    
    def set_Info_input(tmp, visi):
        info_morph = [child for child in tmp.children if child.name == "Info_input"]
        if info_morph:
            info_morph[-1].is_visible = visi
            info_morph[-1].draw_new()   
    """        
    
    def key_release(self,event):
        if event.type in {'RET','NUMPAD_ENTER'}:
            self.insert_committed_text(tmp)
            set_Info_input(tmp, False)
#PKHG.attention  return used:                        
        return {'RUNNING_MODAL'} #keys eaton up
        '''
                    self.add_keys(event, tmp)
                    return {'RUNNING_MODAL'}
                else: #new input morph
                    if self.active_text_input_morph:
                        self.insert_committed_text(self.active_text_input_morph)
                        print("text inserted for ",self.active_text_input_morph)
                    else:
                        self.active_text_input_morph = tmp
                        
                    print("DBG L119 distinguish_release_event(hand.py) new inputmorp")
                    self.temp_text_list = []
                    self.active_text_input_morph = tmp
                    self.add_keys(event, tmp)
           '''           
                    

    def add_keys(self, event, morph):
        """eat a keyboard key"""
#PKHG.???        global temp_text_list
        type_val = "" + event.type
#        if type_val == 'RET' or type_val == "NUMPAD_ENTER":
        if type_val in {'RET','NUMPAD_ENTER'}:
            print("\n===DBG add_keys(hand.py L46)=== (numpad)RETURN SEEN", self.temp_text_list, "for morph", morph)
            self.temp_text_list = []
            self.active_text_input_morph = None
#PKHG.TODO ignor_lst ?!            
        elif re_CAS.search(type_val):
            pass
        elif type_val in delete_list: #remove last key if possible
            if self.temp_text_list:
                del(self.temp_text_list[-1])
            pass
        elif type_val == "SPCACE":
            self.temp_text_list.append(" ")
        else:            
            if event.shift: 
                type_val += "_SHIFT"
            self.temp_text_list.append(type_val)
#        return {'RUNNING_MODAL'} #PKHG.??? DO WE WANT THIS
    

    def insert_committed_text(self, morph):
        def convert_it(element):
            print("element to convert", element)
            result = element
            if result in used_keyboard_dict_for_digits.keys():
                result = used_keyboard_dict_for_digits[result]
            elif result.endswith('_SHIFT'):
                result = result[0]
            elif result == "SPACE":
                result = " "
            elif len(result) == 1:
                result = result.lower()
            elif result.startswith('NUMPAD_'):
                if len(result) == 8:
                    result = result[-1]
                elif result in numpad_dict_specials.keys():
                    result = numpad_dict_specials[result]
            print("converted to ", result)
            return result
            
        def convert_list_to_text(letter_list):
            print("TODO convert ", self.temp_text_list, " into a str")
            converted_list = [convert_it(el) for el in letter_list]
            print("------ converted list=",converted_list)
            result = ""
            for el in converted_list:
                result = result + el
            return result               
        
        result =  convert_list_to_text(self.temp_text_list)
        print("------------ result = ", result)
        morph.text_string.text = result
                                                
        
        self.temp_text_list = []
        return "PKHG finished inputting string"
