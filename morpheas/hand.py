debug_left_mouse_click_060512_1048 = True
import bpy

from .rectangle import *
from .morph import *

#PKHG.???temp_text_list =[]
import re
re_CAS = re.compile("^(LEFT|RIGHT)_CTRL$|^(LEFT|RIGHT)_ALT$|^(LEFT|RIGHT)_SHIFT$")

used_keyboard_dict_for_digits = { 'ONE':'1', 'ONE_SHIFT':'!', 'TWO':'2', \
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
     

numpad_dict_specials = {'NUMPAD_PERIOD':'.', 'NUMPAD_SLASH':'/',\
     'NUMPAD_ASTERIX':'*',  'NUMPAD_MINUS':'-',  'NUMPAD_PLUS':'+'}
delete_list= ['DEL','BACK_SPACE']

class Hand(Morph):
    "I represent the mouse cursor"

    def __init__(self):
        super(Hand, self).__init__()
        self.mouse_over_list = []
        self.mouse_down_morph = None
        self.morph_to_grab = None
        self.moving_morph= False
#        self.bounds = Point(0, 0).get_corner(Point(0,0))
        self.bounds = Rectangle(Point(0, 0), Point(0,0))
        self.grabed_morph_offset_x = 0 # the relative position of the morph to the mouse cursor x axis
        self.grabed_morph_offset_y = 0 # the relative position of the morph to the mouse cursor y axis
        self.active_text_input_morph = None
        self.temp_text_list = []
        
    def __repr__(self):
        return 'Hand(' + self.get_center().__str__() + ')'

    def changed(self):
        print("--info-- hand.py L47;  changed called from self = ", self)
        if self.parent != None:
            b = self.get_full_bounds()
            print("--info-- hand.py L50; self.get_full_bounds()", b," extent= ", b.get_extent())
            if b.get_extent() != Point(0, 0):
                self.parent.broken.append(self.get_full_bounds())
                print("--info-- hand.py L53; world.broken", self.parent.broken[:])
   
    def draw(self):
        """ hand has nothing more to draw than its children which are the morph that are marked for grab """
        for child in self.children:
            child.draw()
            
    def draw_on(self, rectangle=None):
        pass

    def process_all_events(self, event):
        """ Central method for processing all kind of events and calling approriate methods for different kind of events """
        
        if event.type == 'MOUSEMOVE':
            return self.process_mouse_move(event)
        elif event.value=='PRESS':
            return self.distinguish_press_event(event)
        
        elif event.value=='RELEASE':            
            return self.distinguish_release_event(event)
        else:
            return {'PASS_THROUGH'}
                
            
    def distinguish_press_event(self, event):
        """mouse down, or keys to do"""
        
        result = {'RUNNING_MODAL'}
        
        if event.type in ['MIDDLEMOUSE','LEFTMOUSE',
                          'RIGHTMOUSE', 'WHEELDOWNMOUSE','WHEELUPMOUSE']:
            result =  self.process_mouse_down(event)
        return result  



    def distinguish_release_event(self, event):
        """handle keyboard release"""
        
        def set_Info_input(tmp, visi):
            info_morph = [child for child in tmp.children if child.name == "Info_input"]
            if info_morph:
                info_morph[-1].is_visible = visi
                info_morph[-1].draw_new()

        print("distinguish_release_event called")
        if event.type in ['MIDDLEMOUSE','LEFTMOUSE',
                          'RIGHTMOUSE', 'WHEELDOWNMOUSE','WHEELUPMOUSE']:
            return self.process_mouse_up(event)
        else:
#PKHG.activate for tests            return {'RUNNING_MODAL'}
            tmp = self.get_morph_at_pointer() #PKHG. at least world?!
            print("\n--------------------------- L101 distinguish_release_event(hand.py) event.type =", event.type, " who =", tmp.name)
            if tmp.name.startswith("input"):
                set_Info_input(tmp, True)                
                if self.active_text_input_morph and tmp.name == \
                       self.active_text_input_morph.name:
#                    if event.type == 'RET':
                    if event.type in {'RET','NUMPAD_ENTER'}:
                        self.insert_committed_text(tmp)
                        set_Info_input(tmp, False)
#PKHG.attention  return used:                        
                        return {'RUNNING_MODAL'} #keys eaton up
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
                    
#??                self.active_text_input_morph = tmp
                
                return {'RUNNING_MODAL'}
            else:                                  
                return {'PASS_THROUGH'}
        
    
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
    
    def process_mouse_event(self, event):
        """ Central method for processing all kind of events and calling approriate methods for different kind of events """

        if event.type == 'MOUSEMOVE':
            return self.process_mouse_move(event)
        elif event.value in 'PRESS':
            return self.process_mouse_down(event)
        elif event.value=='RELEASE':
            return self.process_mouse_up(event)
        
    def get_morph_at_pointer(self):
        """ return the top morph that is under the current position of the mouse cursor """
    
        morphs = self.parent.children
        for m in morphs: # morphs[::-1]:
            if m.get_full_bounds().get_contains_point(self.bounds.origin) and m.is_visible and not isinstance(m,Hand):
                return m.get_morph_at(self.bounds.origin)
        return self.parent

    def get_all_morphs_at_pointer(self):
        """ return all the morphs are under the current position of the mouse cursor """
    
        answer = []
        # morphs = self.world.all_children()
        morphs = self.parent.children
        for m in morphs:
            if m.is_visible and (m.get_full_bounds().get_contains_point(self.bounds.origin)):
                answer.append(m)
        return answer

    #Hand dragging and dropping:

    def drop_target_for(self, morph):
        target = self.get_morph_at_pointer()
        print("DBG handle drop_target_for L63 morph = ", morph)
        while target.get_wants_drop_of(morph) == False:
            target = target.parent
        return target
#Hand
    def grab(self, morph):
        """ Grab morph . That means that the morph is removed as a child of the world and added as a child of the hand """
        if self.children == []:
            #self.world.stop_editing()
            self.add(morph)
            self.changed()
            self.grabed_morph_offset_x =  morph.bounds.origin.x - self.bounds.origin.x 
            self.grabed_morph_offset_y =  morph.bounds.origin.y - self.bounds.origin.y 
            print("morph has been grabbed")

    def drop(self):
        """ Drop morph. The morph is removed as a child of the hand and added back to its world."""
        
        if self.children != []:
            morph = self.children[0]
            target = self.drop_target_for(morph)
            self.changed()
            target.add(morph)
            morph.changed()
            self.get_morph_to_grab = None
            self.children = []
            self.set_extent(Point(0, 0))

            print("morph has been droped")


    #Hand event dispatching:

    def process_mouse_down(self, event):
        """ This method handles any kind of mouse button presses """
        
        returned_value = {'PASS_THROUGH'}
        
        if self.children != []:
            self.drop()
        else:
            
            morph = self.get_morph_at_pointer()
            pos = self.bounds.origin
            
            if event.type == 'LEFTMOUSE':                
                
                # mark morph for drag only if mouse cursor is top of it
                self.morph_to_grab = morph.get_root_for_grab()
            
                if morph.is_draggable:
                    self.moving_morph = True
                #searh for a morph(parent) to handle a click!
                while not morph.get_handles_mouse_click():
                    if debug_left_mouse_click_060512_1048:
                        print("-L96-> hand.py; morph" , morph, " does not handle left_mouse_click")
                    morph = morph.parent
                if debug_left_mouse_click_060512_1048:
                    print("-L299-> hand.py; morph" , morph, "  handles lef_mouse_click")
                self.mouse_down_morph = morph                
                # trigger also the approriate morph event
                if debug_left_mouse_click_060512_1048:
                    print("-L303-> hand.py; pos for morph.mouse_down_left(pos) " , morph, "  pos = ", pos)
                morph.mouse_down_left(pos)


            elif event.type == 'MIDDLEMOUSE':
                morph.mouse_down_middle(pos)
            elif event.type == 'RIGHTMOUSE':
                morph.mouse_down_right(pos)
            
        return returned_value

    def process_mouse_up(self, event):
        """ here we process all the mouse_up events and trigger approriate events of the morph depending on the specific action performed """
        # if hand has children in case of a mouse button release remove all its children
        if self.children != []:
            self.drop()
            if self.moving_morph == True:
                    self.moving_morph = False
                    print("movement finished")
        else:
            pos = Point(event.mouse_region_x,
                        event.mouse_region_y)
            morph = self.get_morph_at_pointer()

            while not morph.get_handles_mouse_click():
                morph = morph.parent

            if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                morph.mouse_up_left(pos)

                if morph is self.mouse_down_morph:
                    # this morph event means that the left mouse button has been pressed and released, resulting in a single click
                    morph.mouse_click_left(pos) 

            elif event.type == 'MIDDLEMOUSE' and event.value == 'RELEASE':
                morph.mouse_up_middle(pos)
                if morph is self.mouse_down_morph:
                    # this morph event means that the middle mouse button has been pressed and released, resulting in a single click
                    morph.mouse_click_middle(pos) 
            
            elif event.type == 'RIGHTMOUSE' and event.value =='RELEASE' :
                morph.mouse_up_right(pos)
                if morph is self.mouse_down_morph:
                    # this morph event means that the right mouse button has been pressed and released, resulting in a single click
                    morph.mouse_click_right(pos) 
            
        return {'PASS_THROUGH'}

    def process_mouse_move(self, event):
        """ here we process all the mouse_move events and trigger approriate events of the morph depending on the specific action performed """
        
        value_returned = {'PASS_THROUGH'}
        mouse_over_new = self.get_all_morphs_at_pointer()
        
        # trigger mouse move event and trigger the approriate mouse move event of the morph
        
        if self.children == [] and event.type == 'MOUSEMOVE':
            top_morph = self.get_morph_at_pointer()
            
            if top_morph.get_handles_mouse_move():
                pos = Point(event.mouse_region_x,
                            event.mouse_region_y)
                top_morph.mouse_move(pos)
            morph = top_morph.get_root_for_grab()
            
            # if morph is marked for grab and the mouse moves then drag it
            
            if morph is self.morph_to_grab and morph.is_draggable:

                self.grab(morph)
                value_returned = {'RUNNING_MODAL'}


        # trigger the mouse_leave event of the morph in case mouse cursro enters morph
        for old in self.mouse_over_list:
            if old not in mouse_over_new :
                old.mouse_leave()
                if event.type == 'MOUSEMOVE':
                    old.mouse_leave_dragging()
                    print("I am dragging the old morph")
        
        # trigger mouse_enter_dragging of the morph in case mouse cursor enters a morph
        
        for new in mouse_over_new:
            if new not in self.mouse_over_list:
                new.mouse_enter()
                if event.type == 'MOUSEMOVE':
                    new.mouse_enter_dragging()

                    print("I am dragging the  new morph")


        # and finally if the moph is marked for drag and mouse moves , changes morph's position to match the movement of the mouse, taking into the account the offset of the mouse cursor so the mouse cursor stay always in the same position relative to them morph as the first time it was clicked. 
        if self.children != [] and event.type == 'MOUSEMOVE' and self.moving_morph == True:
            morph_position = Point(self.bounds.origin.x + self.grabed_morph_offset_x , self.bounds.origin.y + self.grabed_morph_offset_y) 
            self.morph_to_grab.set_position(morph_position)
            print("WARNING !!!! morph move : ",self.morph_to_grab)
            value_returned = {'RUNNING_MODAL'}
        
        self.mouse_over_list = mouse_over_new
        
        return value_returned

    #Hand testing:

    def is_dragging(self, morph):
        if self.children != []:
            return morph is self.children[0]
        else:
            return False

    


