from .morph import *
from .rectangle import *

import addon_utils

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
#        self.draw_new()
        
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
        
#PKHG.??? Frame not ok        super(self, Frame).__init__() #PKHG Frame was Widget in pymorpheas
#        self.widget = Widget()
        super(StringField, self).__init__()
        self.default = default
        self.minwidth = minwidth
        self.fontname = fontname
        self.fontsize = fontsize
        self.bold = bold
        self.italic = italic
        self.color = (1.0, 0.0, 1.0, 0.5) #pygame.Color(254,254,254)
        self.text_string = String(self.default, self.fontname, self.fontsize,\
                           self.bold, self.italic)
        self.add(self.text_string)

    def draw(self):
        "initialize my surface"
        super(StringField, self).draw()
        self.text_string.draw()

        input_width = self.text_string.width
        if input_width < 100:
#PKHG.ok            print("stringfield L158 (dif set to 0) input_width =",input_width)
            dif = 0
            self.minwidth = 100
        else:
            dif = input_width - self.get_width()
#PKHG.ok        print("stringfield L163: dif =", dif)
        if dif > 0:
            #adjust size of morph
#            self.minwidth = input_width
            new_corner = self.bounds.corner + Point(dif,0)
#PKHG.not logical            self.bounds = self.bounds.origin.get_corner(new_corner)
            self.bounds = Rectangle(self.bounds.origin, new_corner)
        elif dif < 0:
            x = self.bounds.origin.x
            y = self.bounds.corner.y
            if input_width < 100:
#                self.bounds = self.bounds.origin.get_corner(Point(x + 100, y))
                self.bounds = Rectangle(self.bounds.origin, Point(x + 100, y))
            else:        
#                self.bounds = self.bounds.origin.get_corner(Point(x + input_width, y))
                self.bounds = Rectangle(self.bounds.origin,Point(x + input_width, y))
        children = self.children
#PKHG.OK        print("\n================stringfield children", children)
        for child in children:
            if child.is_visible:
#PKHG.OK                print("stringfield drawing" , child)
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
