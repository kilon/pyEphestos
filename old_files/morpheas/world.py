debug_check_world_draws = False
from .rectangle  import Point
from .morph  import *
from .hand  import *
from .menu import Menu
#pkhg.090612??? from .stringfield import *
#from . class_Frame import Frame

class World(Frame):
    "I represent the screen"

    def __init__(self, x=800, y=600):
        super(World, self).__init__()
        self.hand = Hand()
        self.hand.parent = self
        self.hand.world = self
        self.children.append(self.hand)
        self.kbd_listener = self.hand.kbd_listener
        self.text_cursor = None
        self.bounds = Rectangle(Point(0, 0), Point(x, y))
        self.color = (0.0, 1.0 , 1.0, 0.4)
        self.open_menu = None
        self.is_visible = True
        self.is_draggable = False
        self.is_dev_mode = True
        self.is_quitting = False
        self.broken = [] #PKHG.??? what for?
        self.running = True

    def __repr__(self):
        return 'World(' + self.get_extent().__str__() + ')'
    '''
    def draw_new(self, event):
        Morph.draw_rounded_morph(self, 0.2, self.color, rectangle = False)
        return
    '''
    def draw(self):
        """If ... is running show the world as rounded morph"""

        if self.running:

            for child in self.children:
                if debug_check_world_draws:
                    print("====world: checking ", child, " to draw")
                if child.is_visible:
                    child.draw()


    def broken_for(self, morph):
        "private"
        result = []
        fb = morph.get_full_bounds()
        for r in self.broken:
            if r.intersects(fb):
                result.append(r)
        return result

    def add(self, morph):
        """if isinstance(morph, Menu):
            if isinstance(self.open_menu, Menu):
                self.open_menu.delete()"""
        super(World, self).add(morph)
        morph.world = self
        self.open_menu = morph

    #World displaying:
#PKHG.??? surface superfluous???
    def full_draw_on(self, surface, rectangle=None):
        if rectangle == None:
            rectangle = self.bounds
        if rectangle.get_extent() > Point(0,0):
#PKHG.??? image???            self.image.fill(self.color, rectangle.as_rect())
            for child in self.children:
                child.full_draw_on(surface, rectangle)
            self.hand.full_draw_on(surface, rectangle)



    #World menus:

    def context_menu(self):
        menu = Menu(self, self.__class__.__name__)
        menu.add_item("create a morph...", 'user_create_new_morph')
        menu.add_line()
        menu.add_item("hide all", 'hide_all')
        menu.add_item("show all", 'show_all_hiddens')
#        menu.add_item("move all inside...", 'keep_all_submorphs_within')#PKHG not yet
#        menu.add_item("color...", 'choose_color')#PKHG not yet
#        menu.add_line()
#        menu.add_item("stop all bouncers", 'stop_all_bouncers')
#        menu.add_item("start all bouncers", 'start_all_bouncers')
#        menu.add_line()
        menu.add_item("switch to user mode", 'toggle_dev_mode')
        menu.add_line()
        menu.add_item("input",'StringField')
        menu.add_item("enter developer's mode", 'toggle_dev_mode')
        menu.add_line()
        menu.add_item("about...", 'about')
        return menu #PKHG needed 24-6 in test_PKHG_stringinput*.py TODO?!

#PKHG>TODO  repeated code =>> make a suitable def?!
    def user_create_new_morph(self):
        """user_create_new_morph is one of the menu functions"""
        menu = Menu(target = self, title = "create new") #PKHG self is world!
        menu.is_draggable = True
        #PKHG>??? does not work: menu.with_name = True
        menu.counter = 0 #PKHG show or show no content counter times
        self.add(menu)
        pair_item_0_counter = 0

#        menu.children.append(item_rectangle)
#        menu.add_item("ellipse...", 'user_create_ellipse')
#PKHG not yet        menu.add_item("circle box...", 'user_create_circle_box')
#        menu.add_item("rounded box...", 'user_create_rounded_box')
#PKHG not yet        menu.add_item("polygon...", 'user_create_polygon')
        menu.add_line() #PKHG.??? with creation of object??
        pair_item_0_counter += 1
        item = Morph()
        item.name = str(pair_item_0_counter) + "_type_item"
        item.color = (0,0,1,1) #debug050512_1659 self.bordercolor
        item.set_height(+2) #PKHG 10 = 2 normal
        menu.add(item)

        #'''
        menu.add_item("rectangle...", 'user_create_rectangle')
        item_rectangle = MenuItem(self,'user_create_rectangle',"rectangle...")
        item_rectangle.name = "rectangle..."
        item_rectangle.with_name = True
        menu.add(item_rectangle)
        #'''

        pair_item_0_counter += 1
        menu.add_line() #PKHG.??? with creation of object??
        item = Morph()
        item.name = str(pair_item_0_counter) + "_type_item"
        item.color = (0,0,1,1) #debug050512_1659 self.bordercolor
        item.set_height(+10) #PKHG 10 = 2 normal
        menu.add(item)

        menu.add_item("rounded...", 'user_create_rounded')
        item_rounded = MenuItem(self,'user_create_rounded',"rounded...")
        item_rounded.name = "rounded..."
        item_rounded.with_name = True
#        item_rounded.outer_per = 0.2
#        item_rounded.inner_per = 0.2
#        item_rounded.border = 0
#        item_rounded.bordercolor = (0, 0, 0, 1)
        menu.add(item_rounded)

        menu.add_line() #PKHG.??? with creation of object??
        pair_item_0_counter += 1
        item = Morph()
        item.name = str(pair_item_0_counter) + "_type_item"
        item.color = (0,0,1,1) #debug050512_1659 self.bordercolor
        item.set_height(+2) #PKHG 10 = 2 normal
        menu.add(item)

        remove_me = MenuItem(self, action = "delete_me_from_worlds_children")
        remove_me.with_name = True
        remove_me.name = "del"
        remove_me.label = "del"
        remove_me.set_color((0, 0, 1, .1)) #PKHG>??? 1jul color???
        remove_me.is_visible = True
        remove_me.set_position(menu.get_bottom_right())
        menu.add(remove_me)
#        print("--->>>--- world L150, menu items",menu.items[:])
#        print("--->>>--- world L151, menu children",menu.children[:])
        fb = menu.get_full_bounds()
        menu.set_extent(fb.get_extent() + 10)
        menu.adjust_widths()
     #   super(Menu, self).draw()

#        menu.add_item("string...", 'user_create_string')
#        menu.add_item("text...", 'user_create_text')
#        menu.add_line()
#PKHG not yet        menu.add_item("bouncer...", 'user_create_bouncer')
#PKHG not yet        menu.add_item("frame...", 'user_create_frame')
#PKHG not yet        menu.add_item("palette...", 'user_create_color_palette')
#PKHG not yet        menu.add_item("slider...", 'user_create_slider')
        menu.popup_at_hand()


    def user_create_rounded(self):
        """user_create_rounded one of main menu actions"""
#        print("create rounded morph world L166")
        rounded = RoundedBox()
        rounded.bounds = rounded.bounds.get_scale_by(0.5)
        rounded.name ="Round"
        rounded.outer_per = 0.5
        rounded.inner_per = 0.499
#        rounded.with_name = True
        rounded.set_color((1, 1, 1, 1))
        rounded.bordercolor = (1, 0, 0, 1)
        rounded.border = 15
        rounded.set_position(Point(400,400))
        self.add(rounded)
        remove_me = MenuItem(rounded, action = "delete_me_from_worlds_children")
#        remove_me.name = "del"
#        remove_me.with_name = True
#        remove_me.set_color((0,0,1,1))
#        remove_me.is_visible = True
        remove_me.set_position(rounded.get_position())
        rounded.add(remove_me)
        self.add(rounded)


    def user_create_rectangle(self):
        rectangle = Morph()
        rectangle.name = "Rectangle"
        rectangle.with_name = True
        rectangle.set_color((0,1,0,0.2))
        rectangle.set_position(Point(500,500))
        #PKHG>TODO add a MenuItem with delete_me_from_worlds_children
        remove_me = MenuItem(rectangle, action = "delete_me_from_worlds_children")
        remove_me.name = "del"
        remove_me.with_name = True
        remove_me.set_color((0,1,1,1))
        remove_me.is_visible = True
        remove_me.set_position(rectangle.get_position())
        rectangle.add(remove_me)
        self.add(rectangle)
        return

#???        Morph().pick_up() #PKHG does only pass at 250612

    def delete_me_from_worlds_children(self, object):
        """returns None if object is not a child of world, otherwise object"""
        result = None
        if self.children.count(object):
            result = object
            index = self.children.index(object)
            del self.children[index]
        return result


#PKHG not yet used 4jul12
    def stop_all_bouncers(self):
        print("error: world has no attribute 'all_children', why?",self,type(self))
        return
        for m in self.all_children():
            if isinstance(m, Bouncer):
                m.is_stopped = True

    def start_all_bouncers(self):
        print("error: world has no attribute 'all_children', why?",self,type(self))
        return
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
            if isinstance(morph, Menu):
#                print("*INFO PKHG* do not hide " , self)
                pass
            elif morph.name.startswith("MAIN"):
#                print("*INFO* world L159 do not hiding", morph)
                pass
            else:
                morph.hide()

    def choose_color(self):
        print("*INFO* no chose_color (yet) implemented")
        pass #PKHG.TODO

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

    #PKHG differently done 4jul12
    def about(self):
        return
        self.inform("morphic.py\n\n\
a lively GUI for Blender\ninspired by Squeak\nbased on Pygame\n\
"  + "\n\nwritten by k & p ")

    #World utilities not used yet

    def fontname_by_user(self):
        names = sorted(pygame.font.get_fonts())
        choice = ListMenu(names,
                          'choose font').get_user_choice()
        if choice == False:
            return None
        else:
            return choice



    #World events / dragging and dropping:

    def get_wants_drop_of(self, morph):
        return True

    def get_handles_mouse_click(self):
        return True
