import bgl, blf
from .rectangle import *
from .morph import *
import addon_utils

class Text(Morph):
    "I am a mult line, word wrapping string"

    def __init__(self,
                 text,
                 fontname="arialbd.ttf",
                 fontsize=24,
                 bold=False,
                 italic=False,
                 alignment='left',
                 #PKHG.INFO a real Text needs a max_with > 0 !!!
                 max_width=200):
#### PKHG idea to make scrolling easy?
        '''
        max_nr_of_lines >= 1
        show lines from startline >= 0
        show_nr_of_lines
        show_upto = min(startline + show_nr_of_lines, max_nr_of_lines)
        ==> range(startline,show_upto,1)
        problem, if because of width lines were added?!
        '''
        super(Text, self).__init__()
        tmp = addon_utils.paths()[0] + "/Ephestos/fonts/" + fontname
        self.font = blf.load(tmp)
        blf.size(self.font, fontsize, 72) #DPI = 72 !!
        self.background_color = [0, 0, 0, 1]
        #PKHG.??? if a of background_color  not 1 strange things can happen
        #4jul12 show about use input move about =>strange behavior
        self.text = text
        self.words = []
        self.lines = []
        self.fontname = fontname
        self.fontsize = fontsize
        self.bold = bold
        self.italic = italic
        self.alignment=alignment
        self.max_width = max(20, min(max_width, 800))
#        self.color = (.0, 1.0, 1.0, 1.0) #PKHG 7jul12 white forced in draw
        self.max_line_width = 0
        self.adjust_text(text)
        

    def __repr__(self):
        """ Text('myname') returned"""
        return 'Text("' + self.name + '")'

    def parse(self):
        """parsing of text, \n gives newline"""
        self.words = []
        paragraphs = self.text.splitlines()
        self.max_line_width = 0
        for p in paragraphs:
            self.words.extend(p.split(' '))
            self.words.append('\n')
        self.lines = []
        oldline = ''
        for word in self.words:
            if word == '\n':
                self.lines.append(oldline)
                w = blf.dimensions(self.font,oldline)
                self.max_line_width = max(self.max_line_width, w[0])
                oldline = ''
            else:
                if self.max_width > 0:
                    newline = oldline + word + ' '
                    w = blf.dimensions(self.font, newline)
                    if w[0] > self.max_width:
                        self.lines.append(oldline)
                        w = blf.dimensions(self.font, oldline)
                        self.max_line_width = max(self.max_line_width, w[0])
                        oldline = word + ' '
                    else:
                        oldline = newline
                else:
                    oldline = oldline + word + ' '

    def draw(self):
        """a multiline output drawn"""
#        super(Text,self).draw() #PKHG 7jul12 drawn by this draw
        tmp = self.bounds
        x = self.bounds.origin.x
        y = self.bounds.origin.y
        xx = self.bounds.corner.x
        yy = self.bounds.corner.y
        hei = yy - y
        nr = len(self.lines)
        lineHei = -1 +  hei // nr
        #PKHG force a list?? background_color wat not changed it is OK
        bgcol = self.background_color 
        #PKHG no transparency!(strange behavior if allowed)
        bgcol[3] = 1.0
        bgl.glColor4f(*bgcol)
        dime = self.get_extent().as_list()
        bgl.glRecti(self.get_position().x, self.get_position().y, self.get_position().x + dime[0], self.get_position().y + dime[1])
        #PKHG  white color forced
        for el in range(nr):
            Morph.draw_string_to_viewport(self.lines[el], self, 24,\
                    (1, 1, 1 ,1), self.font, x, yy - lineHei  - el * lineHei)
        return

    #Text menu:
    ### a lot of things not yet implemented ###
    '''
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

    def choose_background_color(self):
        result = self.pick_color(self.__class__.__name__ + "\nbackground:",
                            self.background_color)
        if result != None:
            self.background_color = result
            self.draw()
            self.changed()

    def edit_contents(self):
        text = self.prompt("edit contents\nof text field:",
                               self.text,
                               400)
        if text != None:
            self.text = text
            self.changed()
            self.draw()
            self.changed()

    def set_alignment_to_left(self):
        self.set_alignment('left')

    def set_alignment_to_right(self):
        self.set_alignment('right')

    def set_alignment_to_center(self):
        self.set_alignment('center')

    def set_alignment(self, alignment):
        self.alignment = alignment
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

    def change_extent_to(self, point):
        self.changed()
        self.max_width = point.x
        self.draw()
        self.changed()
    '''
    def adjust_text(self, word):
        words = word.replace("\\n","\n")
        position = self.get_position()
        self.text = words
        self.parse() #once?!
        nr_of_lines = len(self.lines)
        res = ""
        for el in self.lines:
            if len(el) > len(res):
                res = el
        blf.size(self.font, self.fontsize, 72) #DPI = 72 !!
        rubbish, use_font_h = blf.dimensions(self.font, ")fg")
        max_width_text, rubbish  = blf.dimensions(self.font, res)
        hight_line = round(use_font_h + 1.51)
        wi,hei = int(min(self.max_line_width, max_width_text)),\
                 nr_of_lines * hight_line
        x = position.x
        y = position.y
#        self.bounds = position.get_corner(Point(wi + x , hei + y ))
        self.bounds = Rectangle(position, Point(wi + x , hei + y ))
    '''
    def wants_drop_of(self, morph): #PKHG.test?
        print("\n\n\n>>>text L229 wants_drop_of called")
        return {'FINISHED'}
    '''
    
    def get_width(self):
        return self.max_line_width

    def mouse_up_left(self,up):
        print("\n\n>>> text L236 mouse_up_left called")        
        self.draw()

    
