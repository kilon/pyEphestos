debug050512_0908 = False #reason test_Menu
#at creation time childrens are [] => True to False set
'''
++++L80+++++ draw_new of Menu called
node.py remove_child; node =   RoundedBox(node)
node.py remove_child; node =   MenuItem(node)
morpy.py add; morph =  StringField(node)  parent of morph Menu(I am a Menu)
node.py remove_child; node =   StringField(node)
Traceback (most recent call last):
  File "C:\BlenderSVN\cmake_all3\bin\2.63\scripts\addons\Ephestos\test_2_morpheas.py", line 147, in draw_ephestos
    world.draw_new()
  File "C:\BlenderSVN\cmake_all3\bin\2.63\scripts\addons\Ephestos\morpheas\world.py", line 41, in draw_new
    child.draw_new()
  File "C:\BlenderSVN\cmake_all3\bin\2.63\scripts\addons\Ephestos\morpheas\menu.py", line 111, in draw_new
    self.add(item)
  File "C:\BlenderSVN\cmake_all3\bin\2.63\scripts\addons\Ephestos\morpheas\morph.py", line 286, in add
    parent.remove_child(morph)
  File "C:\BlenderSVN\cmake_all3\bin\2.63\scripts\addons\Ephestos\morpheas\node.py", line 25, in remove_child
    self.children.remove(node)
ValueError: list.remove(x): x not in list
++++L80+++++ draw_new of Menu called
'''
debug050512 = False #width checking ...


from .roundedbox import *
from .text import *
from .stringfield import * #see Menu add_entry


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
        if debug050512_0908:
            print("menu.py Menu: children: ", self.children[:])

    def add_item(self, label="close", action='nop'):
        self.items.append((label, action))

    def add_line(self, width=1):
        self.items.append((0,width))

    def add_entry(self, default='', width=100):
        field = StringField(default, width)
        field.is_editable = True
        self.items.append(field)

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

        text.draw_new()
        self.label = RoundedBox(3,0)
        self.label.color = self.bordercolor
        self.label.set_extent(text.extent() + 4)
        self.label.draw_new()
        self.label.add(text)
        self.label.text = text
        
    def draw_new(self):
        print("++++L80+++++ draw_new of Menu called")
        for m in self.children:
            m.delete()
        self.children = []
        self.edge = 5
        self.border = 2
        self.color = (1.0, 1.0, 1.0, 1.0) #pygame.Color(254,254,254)
        self.bordercolor = (0.4, 0.4, 0.4, 0.4) #pygame.Color(60,60,60)
        self.set_extent(Point(0, 0))
        if self.title != None:
            self.create_label()
            self.label.set_position(self.bounds.origin + 4)
            self.add(self.label)
            y = self.label.bottom()
        else:
            y = self.top() + 4
        x = self.left() + 4
        for pair in self.items:
            if isinstance(pair,StringField): #PKHG.TODO or isinstance(pair,ColorPicker):
                item = pair
            elif pair[0] == 0:
                item = Morph()
                item.color = self.bordercolor
                item.set_height(pair[1])
            else:
                item = MenuItem(self.target, pair[1], pair[0])
            item.set_position(Point(x, y))
            self.add(item)
            y += item.height()
        fb = self.full_bounds()
        self.set_extent(fb.extent() + 4)
        self.adjust_widths()
        super(Menu, self).draw_new()

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
            w = max(w, item.width())
            if debug050512:
                print("Menu max_width w = ", w)
        if self.label != None:
            if debug050512:
                print("Menu max_width label.width = ", self.label.width())
            w = max(w, self.label.width())
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
                item.draw_new()
                if item is self.label:
                    item.text.set_position(
                        item.center() - (item.text.extent() // 2))

    def popup(self, world, pos):
        self.draw_new()
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
        self.draw_new()
        self.popup(world, (world.hand.position() - (self.extent() // 2)))

    def popup_centered_in_world(self):
        self.draw_new()
        self.popup(world, (world.center() - (self.extent() // 2)))

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
        super(Trigger, self).__init__()
#        self.color = pygame.Color(254,254,254)
        self.color = (.5, .5, .0 , .5)
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
        super(Trigger, self).draw_new()
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
        self.label.set_position(self.center() - (self.label.extent() // 2))
        self.add(self.label)

    #Trigger events:

    def handles_mouse_over(self):
        return True

    def handles_mouse_click(self):
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
        print("mouse_down_left of Trigger")
        self.changed()

    def mouse_click_left(self, pos):
#PKHG.TODO        self.target.__getattribute__(self.action)()
        print("mouse_click_left of Trigger called")
        print("pymorpheas calls", self.target.__getattribute__(self.action))
        
class MenuItem(Trigger, Morph): #PKHG>TODOWidget):

    def create_label(self):
        if self.label != None:
            self.label.delete()
        self.label = String(self.label_string,
                                 self.fontname,
                                 self.fontsize,
                                 self.bold,
                                 self.italic)
        self.set_extent(self.label.extent() + Point(8,0))
        np = self.position() + Point(4,0)
        self.label.bounds = np.extent(self.label.extent())
        self.add(self.label)

    def mouse_click_left(self, pos):
        if isinstance(self.parent, Menu):
            self.world().open_menu = None
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
                if (self.full_bounds().top() < self.parent.top()
                    and self.direction == "up"):
                    self.direction = "down"
                if (self.full_bounds().bottom() > self.parent.bottom()
                    and self.direction == "down"):
                    self.direction = "up"
            elif self.type == "horizontal":     
                if self.direction == "right":
                    self.move_right()
                else:
                    self.move_left()
                if (self.full_bounds().left() < self.parent.left()
                    and self.direction == "left"):
                    self.direction = "right"
                if (self.full_bounds().right() > self.parent.right()
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
