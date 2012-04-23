import bgl, blf
from .rectangle import *
from .morph import *



class Text(Morph):
    "I am a mult line, word wrapping string"

    def __init__(self,
                 text,
                 fontname="verdana",
                 fontsize=24,
                 bold=False,
                 italic=False,
                 alignment='left',
#PKHG.INFO a real Text nees a with > 0 !!!
                 max_width=200):
#        pygame.font.init()
#PKHG.TODO or always only font_id = 0 the default??
#PKHG.works        self.font = blf.load("c:/Windows/Fonts/Verdana.ttf")
#        self.font = blf.load("c:/Windows/Fonts/Verdana.ttf") #this works
#no becomes bigger than it should        self.font = blf.load("c:/Windows/Fonts/arialbd.ttf")
#        self.font = blf.load("c:/Windows/Fonts/arial.ttf") #this works
#        self.font = blf.load("c:/Windows/Fonts/baln.ttf") #this works but too small
#PKHG.TODO font stuff
        self.font = blf.load("c:/Windows/Fonts/bod_b.ttf") #this works but too small
        blf.size(self.font, fontsize, 72) #DPI = 72 !!
        self.background_color = (0,0,0, 0.5)
        self.text = text
        self.words = []
        self.fontname = fontname
        self.fontsize = fontsize
        self.bold = bold
        self.italic = italic
        self.alignment=alignment
#PKHG.??? is complicated   20<= max_width <= world width
        self.max_width = max(20, min(max_width, 800))
        super(Text, self).__init__()
        self.color = (1.0, 1.0, 1.0, 1.0) # PKHG.???BLACK pygame.Color(0,0,0)
#PKHG.not yet        self.draw_new()
        self.max_line_width = 0
        self.lines = []
#PKHG>???        
        self.parse() #once?!
#        w = blf.dimensions(self.font,"Af")
#        hight_line = round(w[1] + 1.51)
        nr_of_lines = len(self.lines)
#        print("nr_of_lines", nr_of_lines)
        res = ""
        for el in self.lines:
#            print(el)
            if len(el) > len(res):
                res = el
        blf.size(self.font, fontsize, 72) #DPI = 72 !!
        w = blf.dimensions(self.font, res)
#        print("res =  and w max_line_width", res, w, self.max_line_width)
        hight_line = round(w[1] + 1.51)
#        print("Text init nr of lines, w",nr_of_lines, w)
        wi,hei = int(max(self.max_line_width, w[0]+2)), nr_of_lines * hight_line        
        self.bounds = Point(0,0).corner(Point(wi, hei ))
#        print("size of text", self.bounds)


    def __repr__(self):
        return 'Text("' + self.text + '")'

    def parse(self):    
#        print("\n===++++++444444444++++++++DBG parse L1508 w" , self.font, blf.dimensions(self.font,"PKHG "))
        self.words = []
        paragraphs = self.text.splitlines()
        self.max_line_width = 0
        for p in paragraphs:
            self.words.extend(p.split(' '))
            self.words.append('\n')
        '''
        self.font = pygame.font.SysFont(
            self.fontname,
            self.fontsize,
            self.bold,
            self.italic)
        '''
        self.lines = []
        oldline = ''
        for word in self.words:
            if word == '\n':
                self.lines.append(oldline)
#                self.max_line_width = max(self.max_line_width,
#                                          self.font.size(oldline)[0])
                w = blf.dimensions(self.font,oldline)
                self.max_line_width = max(self.max_line_width, w[0])
                oldline = ''
            else:
                if self.max_width > 0:
                    newline = oldline + word + ' '
#                    w = self.font.size(newline)
                    w = blf.dimensions(self.font, newline)                    
                    if w[0] > self.max_width:
                        self.lines.append(oldline)
                        w = blf.dimensions(self.font, oldline)
#                        self.max_line_width = max(self.max_line_width,
#                                                    self.font.size(oldline)[0])
                        self.max_line_width = max(self.max_line_width, w[0])
                        oldline = word + ' '
                    else:
                        oldline = newline
                else:
                    oldline = oldline + word + ' '
#        print("\n---DBG L1569 parse text, max_line_width", self.max_line_width)
#Text ...    
    def draw_new(self, event):
#PKHG.??? it is a morph!        surfaces = []
#        print("\n\n++++++++++++++++++ text draw new called")
        tmp = self.bounds
        x = self.bounds.origin.x
        y = self.bounds.origin.y
        xx = self.bounds.corner.x
        yy = self.bounds.corner.y 
        hei = yy - y
        nr = len(self.lines)
        lineHei = hei // nr 
        color = self.color
        bgcol = self.background_color
        bgl.glEnable(bgl.GL_BLEND) #PKHG. needed for color of rectangle!
        bgl.glColor4f(*bgcol)
        dime = self.extent().as_list()
        bgl.glRecti(self.position().x, self.position().y, self.position().x + dime[0], self.position().y + dime[1])
        for el in range(nr):
            Morph.draw_string_to_viewport(self.lines[el], self,24, color, self.font, x, yy - lineHei  - el * lineHei)
        return
    
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

