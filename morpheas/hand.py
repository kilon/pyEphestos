#PKHG debuginfo, please do not remove! Later ok ...
debug_left_mouse_click_060512_1048 = False
debug_get_morph_at_pointer = False
debug_kbd_listener = False #18-06
debug_typedtext = False #24-06 PKHG

import bpy

from .rectangle import *
from .morph import *
from .menu import *

class Hand(Morph):
    "A hand is a morph that is not visual and represent the mouse cursor. It hadles and process all events as long as the mouse cursor is on top of another moprh and also trigger the approriate event methods of each morph"

    def __init__(self):
        super(Hand, self).__init__()
        self.mouse_over_list = []
        self.mouse_down_morph = None
        self.morph_to_grab = None
        self.moving_morph= False
        self.bounds = Rectangle(Point(0, 0), Point(0,0))
        self.grabed_morph_offset_x = 0 # the relative position of the morph to the mouse cursor x axis
        self.grabed_morph_offset_y = 0 # the relative position of the morph to the mouse cursor y axis
        self.active_text_input_morph = None
        self.temp_text_list = []
        self.mouse_x = 0
        self.mouse_y = 0
        self.kbd_listener = KeyboardListener()

    def __repr__(self):
        return 'Hand(' + self.get_center().__str__() + ')'

    def changed(self):
        "method called when something is changed"
        if self.parent != None:
            b = self.get_full_bounds()

            if b.get_extent() != Point(0, 0):
                self.parent.broken.append(self.get_full_bounds())


    def draw(self):
        """ hand has nothing more to draw than its children which is the morph that is marked for grab """
        for child in self.children:
            child.draw()


    def process_all_events(self, event):
        """ Central method for processing all kind of events and calling approriate methods for different kind of events """

        result = {'PASS_THROUGH'} #PKHG default value

        #PKHG mouse_x and mouse_y needed for CrossHair
        old_mouse_x = self.mouse_x
        old_mouse_y = self.mouse_y
  #      oldPoint = Point(old_mouse_x, old_mouse_y)
        self.mouse_x = event.mouse_region_x
        self.mouse_y = event.mouse_region_y
  #      newPoint = Point(self.mouse_x, self.mouse_y)

########PKHG question #############################################
#       why does MOUSEMOVE be called even the mouse is NOT moved???
###################################################################

        if event.type == 'MOUSEMOVE':
            if (self.mouse_x != old_mouse_x) or (self.mouse_y != old_mouse_y):
                result = self.process_mouse_move(event)
        elif event.value=='PRESS':
            result = self.detect_press_event(event)
        elif event.value=='RELEASE':
            result =  self.detect_release_event(event)
        return result


    def detect_press_event(self, event):
        """mouse down, or keys to do"""

        self.kbd_listener.keyPressed(event)
        result = {'RUNNING_MODAL'}

        if event.type in ['MIDDLEMOUSE','LEFTMOUSE',
                          'RIGHTMOUSE', 'WHEELDOWNMOUSE','WHEELUPMOUSE']:
            result =  self.process_mouse_down(event)
        return result



    def detect_release_event(self, event):
        """handle keyboard release"""

        if event.type in ['MIDDLEMOUSE','LEFTMOUSE',
                          'RIGHTMOUSE', 'WHEELDOWNMOUSE','WHEELUPMOUSE']:
            return self.process_mouse_up(event)
        else:
            self.kbd_listener.keyReleased(event)
            tmp = self.get_morph_at_pointer()    #PKHG. at least world?!
#PKHG.for debug interesting:
#            print("\nhand L104 ",tmp, " 's key_release called!!")
            key_release = tmp.key_release(event) #key_release() takes exactly 2 arguments (1 given)
            if key_release == True :
                return {'RUNNING_MODAL'}
            else:
                return {'PASS_THROUGH'}

#PKHG.??? not used, differenly discovered
    '''
    def process_mouse_event(self, event):
        """ Central method for processing all kind of events and calling approriate methods for different kind of events """

        if event.type == 'MOUSEMOVE':
            return self.process_mouse_move(event)
        elif event.value in 'PRESS':
            return self.process_mouse_down(event)
        elif event.value=='RELEASE':
            return self.process_mouse_up(event)
    '''

    def get_morph_at_pointer(self):
        """ return the top morph that is under the current position of the mouse cursor """

        morphs = self.parent.children
        for m in morphs: # morphs[::-1]:
            if m.get_full_bounds().get_contains_point(self.bounds.origin)\
                   and m.is_visible\
                   and not isinstance(m, Hand)\
                   and not( m == self.parent): #PKHG=> exclude world
                return m.get_morph_at(self.bounds.origin)
        return self.parent

    def get_all_morphs_at_pointer(self):
        """ return all the morphs that are under the current position of the mouse cursor """
        answer = []
        morphs = self.parent.children
        for m in morphs:
            if m.is_visible \
              and (m.get_full_bounds().get_contains_point(self.bounds.origin))\
              and not isinstance(m, Hand)\
              and not isinstance(m, type(self.parent)): #PKHG nothing with world!
                answer.append(m)
        return answer

    #Hand dragging and dropping:

    def drop_target_for(self, morph):
        target = self.get_morph_at_pointer()
        while target.get_wants_drop_of(morph) == False:
            target = target.parent
        return target
#Hand
    def grab(self, morph):
        """ Grab morph . That means that the morph is removed as a child of the world and added as a child of the hand """
        if self.children == []:
            morph.parent.remove_child(morph)
            self.add(morph)
            self.changed()
            self.grabed_morph_offset_x =  morph.bounds.origin.x - self.bounds.origin.x
            self.grabed_morph_offset_y =  morph.bounds.origin.y - self.bounds.origin.y

    def drop(self):
        """ Drop morph. The morph is removed as a child of the hand and added back to its world."""
        if self.children != []:
            morph = self.children[0]
            target = self.drop_target_for(morph)
            self.changed()
            target.add(morph)
            morph.changed()
            self.morph_to_grab = None
            self.children = []
            self.set_extent(Point(0, 0))

    #Hand event dispatching:

    def process_mouse_down(self, event):
        """ This method handles any kind of mouse button presses """

        result = {'PASS_THROUGH'}

        if self.children != []:
            self.drop()
        else:
            morph = self.get_morph_at_pointer()
            pos = self.bounds.origin
            if morph != self.parent: #world is it's own parent PKHG???
                if event.type == 'LEFTMOUSE':

                    # mark morph for drag only if mouse cursor is top of it
                    self.morph_to_grab = morph.get_root_for_grab()
#PKHG.todo??? 0606012
                    if morph.is_draggable and not isinstance(morph, MenuItem):
                        self.moving_morph = True
                    #searh for a morph(parent) to handle a click!
                    tmp = morph.get_handles_mouse_click()
                    while not morph.get_handles_mouse_click():
                        morph = morph.parent
                    self.mouse_down_morph = morph
                    # trigger also the approriate morph event
                    morph.mouse_down_left(pos)


                elif event.type == 'MIDDLEMOUSE':
                    morph.mouse_down_middle(pos)
                elif event.type == 'RIGHTMOUSE':
                    morph.mouse_down_right(pos)

                result = {'RUNNING_MODAL'}
        return result

    def process_mouse_up(self, event):
        """ here we process all the mouse_up events and trigger approriate events of the morph depending on the specific action performed """
        # if hand has children in case of a mouse button release remove all its children

        if self.children != []:
            self.drop()
            if self.moving_morph == True:
                    self.moving_morph = False
        else:
            if self.moving_morph == True:
                    self.moving_morph = False

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
                return {'RUNNING_MODAL'}

            elif event.type == 'MIDDLEMOUSE' and event.value == 'RELEASE':
                morph.mouse_up_middle(pos)
                if morph is self.mouse_down_morph:
                    # this morph event means that the middle mouse button has been pressed and released, resulting in a single click
                    morph.mouse_click_middle(pos)
                return {'RUNNING_MODAL'}

            elif event.type == 'RIGHTMOUSE' and event.value =='RELEASE' :
                morph.mouse_up_right(pos)
                if morph is self.mouse_down_morph:
                    # this morph event means that the right mouse button has been pressed and released, resulting in a single click
                    morph.mouse_click_right(pos)
                return {'RUNNING_MODAL'}

        return {'PASS_THROUGH'}

    def process_mouse_move(self, event):
        """ here we process all the mouse_move events and trigger approriate events of the morph depending on the specific action performed """

        value_returned = {'PASS_THROUGH'}

        # trigger mouse move event and trigger the approriate mouse move event of the morph

        if self.children == []:
#PKHG??? is already discovered??        and event.type == 'MOUSEMOVE':
            morph = self.get_morph_at_pointer()
            parent_morph = morph.get_root_for_grab()
            # if morph is marked for grab and the mouse moves then drag it
            if parent_morph is self.morph_to_grab and morph.is_draggable and self.moving_morph:
                self.grab(parent_morph)
                value_returned = {'RUNNING_MODAL'}
            # trigger the mouse_leave event of the morph in case mouse cursor enters morph
            self.detect_mouse_leave(event)
            # trigger mouse_enter_dragging of the morph in case mouse cursor enters a morph
            self.detect_mouse_enter(event)
       # mouse drag the morph if draging is enabled
        if  self.detect_mouse_drag(event):
            value_returned = {'RUNNING_MODAL'}
        return value_returned

#Hand testing:
    def is_dragging(self, morph):
        if self.children != []:
            return morph is self.children[0]
        else:
            return False

# trigger the mouse_enter event of the morph in case mouse cursro enters morph
    def detect_mouse_enter(self,event):
        morphs_at_pointer = self.get_all_morphs_at_pointer()
        for new in morphs_at_pointer:
            if new not in self.mouse_over_list:
                new.mouse_enter()
                self.mouse_over_list.append(new)
                if event.type == 'MOUSEMOVE':
                    new.mouse_enter_dragging()
                    #PKHG morph info too!

# trigger the mouse_leave event of the morph in case mouse cursor leaves morph
    def detect_mouse_leave(self,event):
        morphs_at_pointer = self.get_all_morphs_at_pointer()
        for old in self.mouse_over_list:
            if old not in morphs_at_pointer :
                old.mouse_leave()
                old.mouse_leave_dragging()
                self.mouse_over_list.remove(old)
#                if event.type == 'MOUSEMOVE':
#                    old.mouse_leave_dragging()
#                    print("I am leaving the area of the morph L350", self.get_morph_at_pointer())

    # move morph by mouse drag
    def detect_mouse_drag(self,event):
        if self.children != [] and event.type == 'MOUSEMOVE' and self.moving_morph == True and self.morph_to_grab.is_draggable and self.morph_to_grab.is_visible:
            morph_position = Point(self.bounds.origin.x + self.grabed_morph_offset_x , self.bounds.origin.y + self.grabed_morph_offset_y)
            self.morph_to_grab.set_position(morph_position)
            return  True


#############test for keyboard letteres and digits
lookup_kbd = { 'ONE':'1', 'ONE_SHIFT':'!', 'TWO':'2', \
     'TWO_SHIFT':'@', 'THREE':'3', 'THREE_SHIFT':'#', 'FOUR':'4',\
     'FOUR_SHIFT':'$', 'FIVE':'5', 'FIVE_SHIFT':'%', 'SIX':'6',\
     'SIX_SHIFT':'^', 'SEVEN':'7', 'SEVEN_SHIFT':'&', 'EIGHT':'8',\
     'EIGHT_SHIFT':'*', 'NINE':'9', 'NINE_SHIFT':'(', 'ZERO':'0', 'ZERO_SHIFT':')', \
     'SPACE': ' ', 'SPACE_SHIFT':' ', 'MINUS':'-', 'MINUS_SHIFT':'_', 'EQUAL':'=', 'EQUAL_SHIFT':'+',\
     'COMMA':',', 'COMMA_SHIFT':'<', 'PERIOD':'.', 'PERIOD_SHIFT':'>',\
     'SLASH':'/', 'SLASH_SHIFT':'?', 'SEMI_COLON':';', 'SEMI_COLON_SHIFT':':',\
     'QUOTE':"'", 'QUOTE_SHIFT':'"', 'TAB':'\t', 'BACK_SLASH':'\\',
     'BACK_SLASH_SHIFT':'|', 'LEFT_BRACKET':'[', 'LEFT_BRACKET_SHIFT':'{',\
     'RIGHT_BRACKET':']', 'RIGHT_BRACKET_SHIFT':'}',\
     'ACCENT_GRAVE':'`', 'ACCENT_GRAVE_SHIFT':'~'
               }

keybd =[ 'SPACE', 'ONE', 'TWO', 'THREE', 'FOUR' , 'FIVE', 'SIX', 'SEVEN',\
         'EIGHT', 'NINE' , 'ZERO', 'MINUS', 'EQUAL', 'COMMA', 'PERIOD', 'SLASH',\
         'SEMI_COLON', 'QUOTE', 'BACK_SLASH', 'LEFT_BRACKET', 'RIGHT_BRACKET', 'ACCENT_GRAVE']


numpad_specials = {'NUMPAD_PERIOD':'.', 'NUMPAD_SLASH':'/',\
     'NUMPAD_ASTERIX':'*',  'NUMPAD_MINUS':'-',  'NUMPAD_PLUS':'+'}

def numpad_char(str):
    result = ""
    if len(str)==8:
        result = str[-1:]
    else:
        result = numpad_specials[str]
    return result


delete_dict= ['DEL','BACK_SPACE']


class KeyboardListener:
    def __init__(self):
        self.text_input = ''
        self.shift_seen = False
        self.users = 0
        self.last_result = ''

    def keyPressed(self, event):
        result = {'RUNNING_MODAL'}
        if self.users > 0:
            if debug_kbd_listener:
                print("\n>>>>>>>>>>>>>Keyboardlistener.keyPressed (L372) keyPressed value and type",event.value, event.type, self.users,"\n<<<<<<<<<<<<<")
            if event.type in ["LEFT_SHIFT", "RIGHT_SHIFT"]:
                self.shift_seen = not self.shift_seen
        return result

    def keyReleased(self, event):
        result = {'RUNNING_MODAL'}
        if self.users == 0:
            return result
        if debug_kbd_listener:
            print("KeyboardListener.keyReleased (hand.pyL374) keyReleased called")
        evt_type = event.type
        if event.value in ["LEFT_SHIFT", "RIGHT_SHIFT"]:
            self.shift_seen = not self.shift_seen
        if evt_type in  ["RET", "NUMPAD_ENTER"]:
            pass
        elif len(evt_type) == 1:
            if self.shift_seen:
                self.text_input += evt_type
            else:
                self.text_input += evt_type.lower()
        else:
            if evt_type in ["LEFT_SHIFT", "RIGHT_SHIFT"]:
                self.shift_seen = not self.shift_seen
            elif  evt_type in ["DEL", "BACK_SPACE"]:
                if len(self.text_input) > 0:
                    self.text_input = self.text_input[:-1]
            elif evt_type in keybd:
                if self.shift_seen:
                    evt_type += "_SHIFT"
                self.text_input += lookup_kbd[evt_type]
            elif evt_type == "TAB":
                self.text_input += "    "
            elif evt_type.startswith("NUMPAD"):
                if evt_type in numpad_specials.keys():
                    self.text_input += numpad_specials[evt_type]
                else:
                    self.text_input += evt_type[7:]
            else:
                self.text_input += " *" + evt_type + "* "

        self.displayInfo(event)
        return result

    def displayInfo(self, event):

        if event.type in ["RET", "NUMPAD_ENTER"]:
            #DEL not done! yet
            if self.text_input == "":
                self.text_input = self.last_result
            else:
                self.last_result = self.text_input #PKHG 0707 ??? [:-1]
                self.text_input = ''
        else:
            self.last_result = self.text_input
        if debug_typedtext:
            print("\ntyped text now: ", self.text_input)
#        self.last_result = result
