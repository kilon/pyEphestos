
debug050512 = False #width checking ...
debug050512_1659 = False #MenuItem test
debug_stringfield_060512_0723 = 0 #for stringfield test
debug_mouseclick_060812_0756 = True #self and pos

from .roundedbox import *
from .text import *
from .stringfield import * #see Menu add_input_StringField
from .world import * #PKHG test 0505012

class Menu(RoundedBox):

    def __init__(self, target=None, title=None):
        self.target = target
        self.title = title
        if target == None:
            self.target = self
        self.items = []
        self.label = None
        super(Menu, self).__init__()
        self.is_draggable = False
        if debug050512_1659:
            print("menu.py Menu: children: ", self.children[:])

    def add_item(self, label="close", action='nop'):
        self.items.append((label, action))

    def add_line(self, width=1):
        self.items.append((0,width))

    def add_input_StringField(self, default='', width=100):
        field = StringField(default, width)
        field.name = "input"
        field.with_name = True
        field.is_editable = True
        self.items.append(field)
#        field.draw_new() #PKHG.??? needed? Answer no!
        
#    def add_color_picker(self, default=(0,0,0,0)):
#        field = ColorPicker(default)
#        field.is_draggable = False
#        self.items.append(field)

    def get_entries(self):
        entries = []
        for item in self.items:
            if isinstance (item, StringField):
                entries.append(item.string())
        return entries

#    def get_color_picks(self):
#        picks = []
#        for item in self.items:
#            if isinstance (item, ColorPicker):
#                picks.append(item.get_choice())
#        return picks

    def index_of(self, item):
        list = []
        for child in self.children:
            if isinstance(child, MenuItem):
                list.append(child)
        return list.index(item)
       
    def perform(self, item):
        self.delete()
        item.target.__getattribute__(item.action)()

    def nop(self):
        pass

    def create_label(self):
        '''PKHG 050512_1516 because of error message ValueError: list.remove(x): x not in list
        if self.label != None:
            self.label.delete()
        '''

        if self.label != None:
            self.label.delete()
        
        text = Text(self.title,
                    fontname="verdana.ttf",
                    fontsize=10,
                    bold=True,
                    italic=False,
                    alignment='center')
        text.color = (1.0, 1.0, 1.0, 1.0)
        text.background_color = self.bordercolor

        text.draw()
        self.label = RoundedBox(3,0)
        self.label.color = self.bordercolor
        self.label.set_extent(text.get_extent() + 4)
        self.label.draw()
        self.label.add(text)
        self.label.text = text
        
    def draw(self):
        global debug_stringfield_060512_0723 
#PKHG.OK        print("++++L114+++++ draw_new of Menu called")

        #PKHG 050512 seems to be necessary!
        for m in self.children:
            m.delete()
        
#PKHG.050512_1657???        self.children = []

        if debug050512_1659:
            print("debug050512_1659 children = ",self.children[:])
        self.edge = 5
        self.border = 2
        self.color = (1.0, 1.0, .0, 0.3) #outer color of RoundedBox invisible
        self.bordercolor = (0., 0., 0., 0) #inner color RoundedBox invisble
        self.set_extent(Point(0, 0))
        if self.title != None:
            self.create_label()
            self.label.set_position(self.bounds.origin + 4)
            self.add(self.label)
            self.label.draw() #PKHG. to show it?
            y = self.label.get_bottom()
        else:
            y = self.get_top() + 4
        x = self.get_left() + 4
        if debug050512_1659:
            print("will be position ",(x,y))
        for pair in self.items:
            if debug050512_1659:
                print("pair is",pair)
            if isinstance(pair,StringField): #PKHG.TODO or isinstance(pair,ColorPicker):
                item = pair
                item.with_name = True
                if not debug_stringfield_060512_0723: #show properties of a StringField
                    print("\n--------stringfield.bounnds = ", item.bounds)
                    debug_stringfield_060512_0723 += 1
            elif pair[0] == 0:
                item = Morph()
                #item.bounds = Point(0,0).corner(Point(x,y))
                item.name = "0_type_item"
                item.color = (0,0,1,1)#debug050512_1659 self.bordercolor
#debug050512_1659                item.set_height(pair[1])
                item.set_height(pair[1]+2)
            else:
                item = MenuItem(self.target, pair[1], pair[0])
                item.color = (1,0,0,1) #PKHG test
                item.name = pair[0]
                item.with_name = True
#                item.bounds = Point(0,0).get_corner(Point(0,25))
                item.bounds = Rectangle(Point(0,0), Point(0,25))
#                item.name = "item" + str((x,y))
            item.set_position(Point(x, y))
            self.add(item)
            y += item.get_height()
        fb = self.get_full_bounds()
        self.set_extent(fb.get_extent() + 4)
        self.adjust_widths()
        super(Menu, self).draw()
        
#        print("menu.py draw_new; super(Menu, self) and type ", super(Menu, self), type(super(Menu, self)))  
#PKHG.errro no bounds        super(Menu, self).bounds = Point(0,0).corner( Point(200,200))
    def max_width(self):
        w = 0
        if debug050512:
            print("Menu max_width children", self.children)
        for item in self.children:
            if debug050512:
                print("Menu max_width item in children", item, " its type is" , type(item))
#PKHG.TODO no widget at this moment 25Apr12            
#PKHG>???            if isinstance(item, Morph): #PKHG.TODO Widget):
#                w = max(w, item.width())
            w = max(w, item.get_width())
            if debug050512:
                print("Menu max_width w = ", w)
        if self.label != None:
            if debug050512:
                print("Menu max_width label.width = ", self.label.width())
            w = max(w, self.label.get_width())
            if debug050512:
                print("Menu max_width = ", w)
        return w

    def adjust_widths(self):
        w = self.max_width()
        for item in self.children:
            item.set_width(w)
            if isinstance(item, MenuItem):
                item.create_backgrounds()
            else:
                item.draw()
                if item is self.label:
                    item.text.set_position(
                        item.get_center() - (item.text.get_extent() // 2))

    def popup(self, world, pos):
        self.draw()
        self.set_position(pos)
        self.add_shadow("shade", Point(2,2), 80)
        self.keep_within(world)
        world.add(self)
        world.open_menu = self
        self.full_changed()
        for item in self.items:
            if isinstance(item, StringField):
                item.text.edit()
                return

    def popup_at_hand(self):
        self.popup(world, world.hand.position())

    def popup_centered_at_hand(self):
        self.draw()
        self.popup(world, (world.hand.get_position() - (self.get_extent() // 2)))

    def popup_centered_in_world(self):
        self.draw()
        self.popup(world, (world.get_center() - (self.get_extent() // 2)))

class SelectionMenu(Menu):

    def __init__(self, target=None, title=None):
        super(SelectionMenu, self).__init__(None, title)
        self.choice = None

    def perform(self, item):
        if item.action != 'nop':
            self.choice = item.action
        else:
            self.choice = item.label_string

    def get_user_choice(self):
        self.choice = None
        self.popup_at_hand()
        while self.choice == None:
            world.do_one_cycle()
        self.delete()
        return self.choice

#PKHG.???class ListMenu(object):
class ListMenu(Morph):

    def __init__(self,
                 list=['one' 'two' 'three'],
                 label=None,
                 maxitems=30):
        super(ListMenu, self).__init__() #PKHG.needed??
        self.list = list
        self.maxitems = maxitems
        self.label = label
        self.build_menus()

    def build_menus(self):
        self.menus = []
        count = 0
        sm = SelectionMenu()
        if self.label != None:
            sm.title = self.label
            sm.is_draggable = True
        for item in self.list:
            count += 1
            if count > self.maxitems:
                self.menus.append(sm)
                count = 1
                sm = SelectionMenu()
                sm.add_item("back...", self.menus[len(self.menus) - 1])
                sm.add_line()
                if self.label != None:
                    sm.title = self.label
                    sm.is_draggable = True
            sm.add_item(item)
        self.menus.append(sm)
        for menu in self.menus[:len(self.menus) - 1]:
            menu.add_line()
            menu.add_item("more...", self.menus[self.menus.index(menu) + 1])

    def get_user_choice(self):
        choice = self.menus[0].get_user_choice()
        while isinstance(choice, SelectionMenu):
            choice = choice.get_user_choice()
        return choice        


class Trigger(Morph):
    "basic button functionality"

    def __init__(self, target=None,
                 action='nop', #PKHG.??? was None
                 label=None,
                 fontname="verdana.ttf",
                 fontsize=10,
                 bold=False,
                 italic=False):
        super(Trigger, self).__init__()
        self.name = "trigger"
#        self.hilite_color = pygame.Color(192,192,192)
        grey_192 = 192./255.
        grey_128 = 0.5
        self.hilite_color = (grey_192, grey_192, grey_192, 1.)
#        self.press_color = pygame.Color(128,128,128)
        self.press_color = (grey_128, grey_128, grey_128, 1.0)
        self.label_string = label
        self.fontname = fontname
        self.fontsize = fontsize
        self.bold = bold
        self.italic = italic
        self.label = None
        
#        self.color = pygame.Color(254,254,254)
        self.color = (.5, .5, .0 , 0) #geel weg 
        self.draw_new()
        self.target = target
        self.action = action
        self.is_draggable = False

    def draw_new(self):
        "initialize my surface"
#PKHG.TODO        
        self.create_backgrounds()
        if self.label_string != None:
            self.create_label()

    def create_backgrounds(self):
#        print("Trigger create_backgrounds called self and type =", self, type(self))
        super(Trigger, self).draw()
#        self.normal_image = pygame.Surface(self.extent().as_list())
#        self.normal_image.fill(self.color)
#        self.normal_image.set_alpha(self.alpha)
#        self.hilite_image = pygame.Surface(self.extent().as_list())
#        self.hilite_image.fill(self.hilite_color)
#        self.hilite_image.set_alpha(self.alpha)
#        self.press_image = pygame.Surface(self.extent().as_list())
#        self.press_image.fill(self.press_color)
#        self.press_image.set_alpha(self.alpha)
#        self.image = self.normal_image
        pass
    
    def create_label(self):
        if self.label != None:
            self.label.delete()
        self.label = String(self.label_string,
                                 self.fontname,
                                 self.fontsize,
                                 self.bold,
                                 self.italic)
        self.label.set_position(self.get_center() - (self.label.get_extent() // 2))
        self.add(self.label)

    #Trigger events:

    def get_handles_mouse_over(self):
        return True

    def get_handles_mouse_click(self):
        return True
#PKHG.TODO self.image ..
    def mouse_enter(self):
#        self.image = self.hilite_image
        print("mouse enter of Trigger")
        self.changed()

    def mouse_leave(self):
#        self.image = self.normal_image
        print("mouse_leave of Trigger")
        self.changed()

    def mouse_down_left(self, pos):
#        self.image = self.press_image
        print("=L365= meny.py mouse_down_left of Trigger; self = ", self, " pos = ", pos)
        print("self.action =", self.action )
        if self.action == "close_my_Menu":
            self.parent.delete()
            print("my parent and root is", self.parent, self.get_root())
            self.parent.is_visible = False
            
#            close_my_Menu(self.root())
#def close_my_Menu(menu):
#    menu.is_visible = False
#    print("Menu made invisible")

        self.changed()

    def mouse_click_left(self, pos):
#PKHG.TODO        self.target.__getattribute__(self.action)()
        print("mouse_click_left of Trigger called")
        print("pymorpheas calls", self.target.__getattribute__(self.action))
        
class MenuItem(Trigger):#test zonder morph via Trigger! seems OK, Morph): #PKHG>TODOWidget):

    def create_label(self):
        if self.label != None:
            self.label.delete()
        self.label = String(self.label_string,
                                 self.fontname,
                                 self.fontsize,
                                 self.bold,
                                 self.italic)
        self.set_extent(self.label.get_extent() + Point(8,0))
        np = self.get_position() + Point(4,0)
        self.label.bounds = np.get_extent(self.label.get_extent())
        self.add(self.label)

    def mouse_click_left(self, pos):
        if debug_mouseclick_060812_0756:
            print("MenuItem L390: mouse_click_left self = ",self," pos = ", pos)
        if isinstance(self.parent, Menu):
            self.get_world().open_menu = None
        self.parent.perform(self)

class Bouncer(Morph):

    def __init__(self, type="vertical", speed=1):
        super(Bouncer, self).__init__()
        self.is_stopped = False
        self.fps = 50
        self.type = type
        if self.type == "vertical":
            self.direction = "down"
        else:
            self.direction = "right"
        self.speed = speed

    def move_up(self):
        self.move_by(Point(0, -self.speed))

    def move_down(self):
        self.move_by(Point(0, self.speed))

    def move_right(self):
        self.move_by(Point(self.speed, 0))

    def move_left(self):
        self.move_by(Point(-self.speed, 0))

    def step(self):
        if not self.is_stopped:
            if self.type == "vertical":     
                if self.direction == "down":
                    self.move_down()
                else:
                    self.move_up()
                if (self.get_full_bounds().get_top() < self.parent.get_top()
                    and self.direction == "up"):
                    self.direction = "down"
                if (self.get_full_bounds().get_bottom() > self.parent.get_bottom()
                    and self.direction == "down"):
                    self.direction = "up"
            elif self.type == "horizontal":     
                if self.direction == "right":
                    self.move_right()
                else:
                    self.move_left()
                if (self.get_full_bounds().get_left() < self.parent.get_left()
                    and self.direction == "left"):
                    self.direction = "right"
                if (self.get_full_bounds().get_right() > self.parent.get_right()
                    and self.direction == "right"):
                    self.direction = "left"

    #Bouncer menu:

    def developers_menu(self):
        menu = super(Bouncer, self).developers_menu()
        menu.add_line()
        if self.is_stopped:
            menu.add_item("go!", 'toggle_motion')
        else:
            menu.add_item("stop!", 'toggle_motion')
        menu.add_item("speed...", 'choose_speed')
        if self.type == "vertical":
            menu.add_item("horizontal", 'toggle_direction')
        else:
            menu.add_item("vertical", 'toggle_direction')
        return menu

    def choose_speed(self):
#PKHG.TODO what is prompt? ==> defined in morph.py        
        result = self.prompt("speed:",
                            str(self.speed),
                            50)
        if result != None:
            self.speed = min(max(int(result),0),self.width()//3)

    def toggle_direction(self):
        if self.type == "vertical":
            self.type = "horizontal"
            self.direction = "right"
        else:
            self.type = "vertical"
            self.direction = "up"

    def toggle_motion(self):
        self.is_stopped = not self.is_stopped
