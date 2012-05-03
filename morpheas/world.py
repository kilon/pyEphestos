from .rectangle  import Point
from .hand  import *
#from . class_Frame import Frame
from .morph  import *

class World(Frame):
    "I represent the screen"

    def __init__(self, x=800, y=600):
        super(World, self).__init__()
        self.hand = Hand()
        self.hand.world = self
        self.keyboard_receiver = None
        self.text_cursor = None
        self.bounds = Point(0, 0).corner(Point(x, y))
        self.color = (0.0, 1.0 , 1.0, 0.4)#(130, 130, 130)
#PKHG.INFO World is a Frames, a Frame  is a Morph, a Morh has color and alpha (yet!)
        self.open_menu = None
        self.is_visible = True
        self.is_draggable = False
        self.is_dev_mode = True
        self.is_quitting = False
        #self.draw_new()
        self.broken = []
        self.running = True

    def __repr__(self):
        return 'World(' + self.extent().__str__() + ')'
    '''
    def draw_new(self, event):
        Morph.draw_rounded_morph(self, 0.2, self.color, rectangle = False)
        return
    '''
    def draw_new(self):
        """If ... is running show the world as rounded morph"""
        
        if self.running:            
            Morph.draw_rounded_morph(self, 0.2, self.color, rectangle = False)
            for child in self.children:
                child.draw_new()
                
    
    def broken_for(self, morph):
        "private"
        result = []
        fb = morph.full_bounds()
        for r in self.broken:
            if r.intersects(fb):
                result.append(r)
        return result

    def add(self, morph):
        """if isinstance(morph, Menu):
            if isinstance(self.open_menu, Menu):
                self.open_menu.delete()"""
        super(World, self).add(morph)
        self.open_menu = morph

    #World displaying:

    def full_draw_on(self, surface, rectangle=None):
        if rectangle == None:
            rectangle = self.bounds
        if rectangle.extent() > Point(0,0):
            self.image.fill(self.color, rectangle.as_rect())
            for child in self.children:
                child.full_draw_on(surface, rectangle)
            self.hand.full_draw_on(surface, rectangle)



    #World menus:

    def context_menu(self):
        menu = Menu(self, self.__class__.__name__)
        if self.is_dev_mode:
            menu.add_item("create a morph...", 'user_create_new_morph')
            menu.add_line()
            menu.add_item("hide all", 'hide_all')
            menu.add_item("show all", 'show_all_hiddens')
            menu.add_item("move all inside...", 'keep_all_submorphs_within')
            menu.add_item("color...", 'choose_color')
            menu.add_line()
            menu.add_item("stop all bouncers", 'stop_all_bouncers')
            menu.add_item("start all bouncers", 'start_all_bouncers')
            menu.add_line()
            menu.add_item("switch to user mode", 'toggle_dev_mode')
            menu.add_item("close", 'delete')
        else:
            menu.add_item("enter developer's mode", 'toggle_dev_mode')
        menu.add_line()
        menu.add_item("about...", 'about')
        return menu

    def user_create_new_morph(self):
        menu = Menu(self, "create new")
        menu.add_item("rectangle...", 'user_create_rectangle')
        menu.add_item("ellipse...", 'user_create_ellipse')
        menu.add_item("circle box...", 'user_create_circle_box')
        menu.add_item("rounded box...", 'user_create_rounded_box')
        menu.add_item("polygon...", 'user_create_polygon')
        menu.add_line()
        menu.add_item("string...", 'user_create_string')
        menu.add_item("text...", 'user_create_text')
        menu.add_line()
        menu.add_item("bouncer...", 'user_create_bouncer')
        menu.add_item("frame...", 'user_create_frame')
        menu.add_item("palette...", 'user_create_color_palette')
        menu.add_item("slider...", 'user_create_slider')

        menu.popup_at_hand()

    def user_create_rectangle(self):
        Morph().pick_up()

    def stop_all_bouncers(self):
        for m in self.all_children():
            if isinstance(m, Bouncer):
                m.is_stopped = True

    def start_all_bouncers(self):
        for m in self.all_children():
            if isinstance(m, Bouncer):
                m.is_stopped = False

    #World methods:

    def delete(self):
        if self.ask_yes_no("really quit?"):
            self.is_quitting = True

    def toggle_dev_mode(self):
        self.is_dev_mode = not self.is_dev_mode

    def show_all_hiddens(self):
        for morph in self.children:
            if not morph.is_visible:
                morph.show()

    def hide_all(self):
        for morph in self.children:
            morph.hide()

    def pick_up(self):
        pass

    def edit(self, stringMorph):
        if self.text_cursor != None:
            self.text_cursor.delete()
        self.text_cursor = TextCursor(stringMorph)
        stringMorph.parent.add(self.text_cursor)
        self.keyboard_receiver = self.text_cursor

    def stop_editing(self):
        if self.text_cursor != None:
            self.text_cursor.delete()
        self.keyboard_receiver = None

    def about(self):
        self.inform("morphic.py\n\n\
a lively GUI for Blender\ninspired by Squeak\nbased on Pygame\n\
" + version + "\n\nwritten by k & p ")

    #World utilities:

    def fontname_by_user(self):
        names = sorted(pygame.font.get_fonts())
        choice = ListMenu(names,
                          'choose font').get_user_choice()
        if choice == False:
            return None
        else:
            return choice



    #World events / dragging and dropping:

    def wants_drop_of(self, morph):
        return True

    def handles_mouse_click(self):
        return True

    #World mainloop:

    def loop(self):
        self.full_draw_on()
