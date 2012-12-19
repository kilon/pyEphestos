debug140512_delete_children = False
debug050512_maxwidth = False         #True #width checking ...
debug050512_1659 = False             #MenuItem test
debug_stringfield_060512_0723 = False #for stringfield test
debug_mouseclick_060812_0756 = False #self and pos
debug_roundedbox_160512_1837 = False
debug_trigger_size_17_05_1618 = False
debug_ips = False #True #searching for strange error 
L221_counter = 0  #PKHG for debugging create morph menu

import blf
from random import random
from .roundedbox import *
from .text import *
from .stringfield import * #see Menu add_input_StringField

class Menu(RoundedBox):  #PKHG.??? does Morph suffice?
    """a menu is needed"""
    
    def __init__(self, target=None, title=None):
        self.target = target
#        self.title = title #PKHG I usede name not title yet
        self.name = title
        if target == None:
            self.target = self
        self.items = []
        self.user_items = [] #PKHG for two types of this menu: user
        self.dev_items =  [] #PKHG for two types of this menu: developer
        self.user_children = []
        self.dev_children =  []

        self.label = None
        super(Menu, self).__init__()
        self.is_draggable = False
        self.my_width = 100
        self.stringfield_ID = None
        self.counter = 1
        self.color = (1, 1, 1, 0.2) #outer color of RoundedBox nearly invisible
        self.bordercolor = (1, 0, 0., 0) #PKHG a = 0 MUST?!? inner color RoundedBox invisble


    def add_item(self, label="close", action='nop'):
        """add an item to the list of actions of a menu"""
        self.items.append((label, action))

    def add_line(self, width=1):
        """add a line as seperator"""
        self.items.append((0,width))

        
#    def add_color_picker(self, default=(0,0,0,0)):
#        field = ColorPicker(default)
#        field.is_draggable = False
#        self.items.append(field)

#PKHG.TODO if needed
    '''
    def get_entries(self):
        entries = []
        for item in self.items:
            if isinstance (item, StringField):
                entries.append(item.string())
        return entries
    '''
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
#        print("--->>>---perform-------Menu L75 item = ", item,item.action, self, "\n--->>>--- self and its world ", self, self.world)
        if not (item.action == "StringField"):            
            res = self.world.__getattribute__(item.action)
#            print("--->>>--- menu L78 item action and code = ",item.action," will be called now:")
            res()
        
        
    def nop(self):
        pass

    #PKHG not used
    
    def create_label(self):
        '''PKHG 050512_1516 because of error message ValueError: list.remove(x): x not in list
        if self.label != None:
            self.label.delete()
        '''
#PKHG.TODO
#        if self.label != None:
#            self.label.delete()
        
        text = Text(self.title,
                    fontname="verdana.ttf",
                    fontsize=10,
                    bold=True,
                    italic=False,
                    alignment='center')
        text.color = (1.0, 1.0, 1.0, 1.0)
        text.background_color = self.bordercolor

        text.draw()

#PKHG. test!!!! works
        self.label = RoundedBox(3,0)
        self.label.color = self.bordercolor
        self.label.set_extent(text.get_extent() + 4)
        self.label.draw()
        self.label.add(text)
        self.label.text = text

#PKHG on 18-06-2012 Menu needs to have this def??
    def full_changed(self):
        pass
        
    def draw(self):
        """draw the menu"""
        global L221_counter #for debugging create_menu
        if self.name.startswith("MAIN"):
            if self.counter > 0:
                print("\n------> menu L126 self is now",self)
                self.counter = 0
            if debug_roundedbox_160512_1837:
                print("-------L112 menu.draw--------->Menu roundedbox width =", self.bounds.get_width())
            if debug140512_delete_children:
                print("======L120 menu.draw============m.delete = ",len(self.children[:]),self.children[:],"\n")
            self.edge = 5
            self.border = 2
#            self.color = (1.0, 1.0, .0, .3) #outer color of RoundedBox nearly invisible
#            self.bordercolor = (0., 0., 0., 0.0) #PKHG a = 0 MUST! inner color RoundedBox invisble
            self.set_extent(Point(0, 0))
            y = self.get_top() + 4
            x = self.get_left() + 4
            if debug050512_1659:
                print("will be position ",(x,y))
            item = None
            #Switch the visible menu corresponding to the mode 
            my_mode = self.world.is_dev_mode
            if my_mode:
                self.items = self.dev_items
                self.children = self.dev_children
            else:
                self.items = self.user_items
                self.children = self.user_children
    
            pair_item_0_counter = 0
            for pair in self.items:
                if debug050512_1659:
                    print("pair is",pair)
                if isinstance(pair,StringInput): #PKHG.TODO or isinstance(pair,ColorPicker):
                    item = pair
                    item.with_name = True
                    if not debug_stringfield_060512_0723: #show properties of a StringField
                        print("\n--------stringfield.bounds = ", item.bounds)
                        debug_stringfield_060512_0723 += 1
                elif pair[0] == 0:
                    pair_item_0_counter += 1
                    name = str(pair_item_0_counter) + "_type_item"
                    for el in self.children:
                        if el.name == name:
                            item = el
#???today4jul
                    item.color = (1,1,1,1) #debug050512_1659 self.bordercolor
                    item.set_height(pair[1]+2)
                else:                
                    for el in self.children:
                        if el.name == pair[0]:
                            item = el
#???today4jul                    item.color = (1,0,0,0) #PKHG test
                    item.name = pair[0]
                    item.with_name = True
                    if item.is_visible:
                        item.set_position(Point(x, y))
    #PKHG is_movable is set to false at creation time, so not needed here
                y += item.get_height()        
    
            fb = self.get_full_bounds()
            self.set_extent(fb.get_extent() + 10)
            self.adjust_widths()
            super(Menu, self).draw()
            if debug140512_delete_children:
                print("+++++++L174 Menu end of draw len and children ",len(self.children), self.children[:])
######### now normal menu's are handled here                
        else:
            self.is_visible = True
            if self.counter > 0:
                print("I am an", self)
                self.counter -= 1
                print(dir(self))
            self.edge = 5
            self.border = 2
            #PKHG>??? 1jul color problem
            self.color = (1, 1, 1, .2) #outer color of RoundedBox nearly invisible
            self.bordercolor = (0, 1., 1., 0.2) #PKHG a = 0 MUST! inner color RoundedBox invisible
            self.set_extent(Point(0, 0))
            y = self.get_top() + 4
            x = self.get_left() + 4
            if debug050512_1659:
                print("will be position ",(x,y))
            item = None
            pair_item_0_counter = 0
            if L221_counter > 0:
                print(">>>> for dbg  menu L221")
                print("self.items =", self.items[:])
                print("self.children =", self.children[:])
                L221_counter -= 1

            for pair in self.items:            
                if pair[0] == 0:
                    pair_item_0_counter += 1
                    name = str(pair_item_0_counter) + "_type_item"
                    for el in self.children:
                        if el.name == name:
                            item = el
                    item.color = (0,0,1,1) #debug050512_1659 self.bordercolor
                    item.set_height(pair[1]+2)
                else:  

                    for el in self.children:
                        if el.name == pair[0]:
                            item = el
                    #PKHG>???  30jun12 item.color = (1,0,0,1) #PKHG test
                    item.name = pair[0]
                    item.with_name = True
                    if item.is_visible: item.set_position(Point(x, y))
                    #PKHG is_movable is set to false at creation time, so not needed here
                y += item.get_height()        
    
            fb = self.get_full_bounds()
            self.set_extent(fb.get_extent() + 10)
            self.adjust_widths()
            super(Menu, self).draw()
            if debug140512_delete_children:
                print("+++++++L174 Menu end of draw len and children ",len(self.children), self.children[:])


##### for MAIN menu: other have to create objects themselves too
    def create_my_objects(self):
        """create the menu-objects and the lists to distinguish the mode the menu is in"""
        
        tmp = []
        pair_item_0_counter = 0
        for pair in self.items:
            if debug050512_1659:
                print("pair is",pair)
            if isinstance(pair,StringInput): #PKHG.TODO or isinstance(pair,ColorPicker):
                item = pair
                tmp.append(item)
                item.with_name = True
                if not debug_stringfield_060512_0723: #show properties of a StringField
                    print("\n--------stringfield.bounds = ", item.bounds)
                    debug_stringfield_060512_0723 += 1
            elif pair[0] == 0:
                pair_item_0_counter += 1
                item = Morph()
                item.name = str(pair_item_0_counter) + "_type_item"
                item.color = (0,0,1,1) #debug050512_1659 self.bordercolor
                item.set_height(pair[1]+2)
            else:
                item = MenuItem(self.target, pair[1], pair[0])
#???today4jul                
                item.color = (0, 0, 1, 1) #PKHG test
                item.name = pair[0]
                item.with_name = True
            self.add(item)
            item.is_movable = False #PKHG 110612 do not move items in a Menu
            tmp.append(item)
        small = ["enter developer's mode"]
        self.user_items = [el for el in self.items if el[0] in small]
        self.dev_items =  [el for el in self.items if not( el[0] in small)]
        self.user_children = [el for el in tmp if el.name in small]
        self.dev_children =  [el for el in tmp if not(el.name in small)]
        for el in self.dev_children:
            self.add_child(el)
        self.items = self.dev_items

        
    def max_width(self):
        """compute the maximal width including all childredn"""
        w = self.my_width
        if debug050512_maxwidth:
            print("Menu max_width children", self.children)
        counter = 0
        for item in self.children:
#            item.name = str(counter)
            counter +=1
            if debug050512_maxwidth:
                print("Menu max_width  child", item, " it width =", item.get_width())
#PKHG.TODO no widget at this moment 25Apr12            
#PKHG>???            if isinstance(item, Morph): #PKHG.TODO Widget):
            w = max(w, item.get_width())
            if debug050512_maxwidth:
                print("Menu max_width w = ", w)
        if self.label != None:
            if debug050512_maxwidth:
                print("Menu max_width label.width = ", self.label.get_width())
            w = max(w, self.label.get_width())
            if debug050512_maxwidth:
                print("Menu max_width = ", w)
        self.my_width = w #PKHG.??? 160512_1831
        return w

    def adjust_widths(self):
        """adjust morph, such that all children of menu are inside its bounds"""
#PKHG>TODO 4jul12???!!check the rest of this def        
        w =  max(self.my_width ,self.max_width()) 
        for item in self.children:
            item.set_width(w)
            if isinstance(item, MenuItem):
                item.create_backgrounds()
            else:
                item.draw()

#PKHG not done, todo???
    def popup(self, world, pos):
#        print("--->>>---  menu L330 popup called")
        self.set_position(pos)
        self.draw()
        ###INFO start########################
#        self.add_shadow("shade", Point(2,2), 80)
        print("***INFO***  menu L335 PYMORPHEAS adds shadow, self = ", self,pos)        
        ###INFO end########################
        self.keep_within(world)
        world.add(self)
        world.open_menu = self
        self.full_changed()
#        for item in self.items:
#            if isinstance(item, StringInput):
#                item.text.edit()
#                return

    def popup_at_hand(self):
        print("***INFO*** error?? TODO??? menu L347* popup_at_hand implemented self = ", self, self.get_root())
        world = self.target
        self.popup(world, Point(400,400))

    def popup_centered_at_hand(self):
        self.draw()
        self.popup(world, (world.hand.get_position() - (self.get_extent() // 2)))

    def popup_centered_in_world(self):
        self.draw()
        self.popup(world, (world.get_center() - (self.get_extent() // 2)))

##########not tested othere types of Menu
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
                 label='trigger',
                 fontname="verdana.ttf",
                 fontsize=10,
                 bold=False,
                 italic=False):
        #PKHG>??? once and for all that font stuff?
        super(Trigger, self).__init__()
        import  addon_utils
        path_to_local_fonts  = addon_utils.paths()[0] + "/Ephestos/fonts"
        font = path_to_local_fonts + "/" + fontname
        font_id = blf.load(font)
        blf.size(font_id, 16, 72) #pKHG needed to adjust text with!
        dims_x,dims_y = blf.dimensions(font_id, label)
#        self.my_name_size = dims_x 
#        mylabel_width = int(dims_x) + 75
#        bounds = Rectangle(Point(0,0),Point(mylabel_width, int(dims_y) + 20))
#        super(Trigger, self).__init__(bounds = bounds)
        
        self.set_width(int(dims_x) + 2)
        self.set_height(int(dims_y) + 15)   #PKHG old: 20)
        self.name = label
        self.action = action

        
    def create_backgrounds(self):
#        print("Trigger create_backgrounds called self and type =", self, type(self))
        super(Trigger, self).draw()
        pass

    #PKHG not used?!
    def create_label(self):
        if self.label != None:
            self.label.delete()
#PKHG. String renamed ... TODO if really needed            
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
#        print("=L384= menu.py mouse_down_left of Trigger; self = ", self, " pos = ", pos ,"my action =", self.action )
        world = self.get_root()
#        print("\n\ntest world self.world", self.world)
#        print("=L385= root is ", world, "self.action =", self.action )
        if self.action == "delete":
            world = self.parent.get_root() #PKHG gives back World!
            print("my world is ", world)
            self.parent.delete()            
            world.is_dev_mode = False
            world_menu = world.context_menu()
            world.add(world_menu)
        elif self.action == "toggle_dev_mode":
#PKHG.TODO a general trigger needed            
#            world = self.parent.get_root() #PKHG gives back World ?!
            print("my world is ", world)
            world.toggle_dev_mode()
        elif self.action == "choose_color":
            print("I am ", self)
            col = self.set_color("red")
            print("color became" ,col)
            self.color = col
            pass
        elif self.action == "about":
            world = self.parent.get_root()
            about = [ el for el in world.children if el.name.startswith("About")]
            if about:
                about_text = about[0]
                visibility = about_text.is_visible
                if visibility:
                    about_text.hide()
                else:
                    about_text.show()
#PKHG.TODO clean the rest!                    
        elif self.action == "StringField":
            world = self.parent.get_root()
            inputmorph_id = world.stringinput_ID
            ips_m  = [el for el in world.children if id(el) == inputmorph_id]
            input_morph_tmp = ips_m[0]
#???4jul            input_morph_tmp.set_color((0, 0, .1, 0.1))                
            input_morph_tmp.is_visible = not input_morph_tmp.is_visible #PKHG toggle!
        self.changed()

    def mouse_click_left(self, pos):
#PKHG.TODO        self.target.__getattribute__(self.action)()
        print("mouse_click_left of Trigger called")
        print("pymorpheas calls", self.target.__getattribute__(self.action))
        
class MenuItem(Trigger):#test zonder morph via Trigger! seems OK, Morph): #PKHG>TODOWidget):

    
    def create_label(self):
        #PKHG.09052012_1010
        return
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
            print("\n=MenuItem L506: mouse_click_left self = ",self," pos = ", pos)#, " self.parent", self.parent.world)
            world = self.world
            action_todo = self.action
            res = world.__getattribute__(self.action)
            print("\n===== menu L510",action_todo, res)
            #res() #???
            
        if isinstance(self.parent, Menu):
#PKHG.TODO???            self.get_world().open_menu = None
            print("I am a Menu (menu L456) TODO???")
            pass
            
#        print("\n<<< menu L567, self,",self,"parent=",self.parent,self.get_root())
        if isinstance(self.parent, Menu) and self.parent.name.startswith("MAIN"):
            self.parent.perform(self)
        else:
            world = self.get_root()
            res = world.__getattribute__(self.action)
#            print("\n===== menu L574 self.action and code",self.action, res)
            if self.action == "delete_me_from_worlds_children":
                tmp = res(self.parent)
#                print("\n self=", self, "\n--------- menu L576 result of res(self)",tmp)
            else:
                res()
            
###PKHG Bouncer not done yet
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


