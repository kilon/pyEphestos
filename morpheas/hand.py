#PKHG debuginfo, please do not remove! Later ok ...
debug_left_mouse_click_060512_1048 = False

import bpy

from .rectangle import *
from .morph import *



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
        
    def __repr__(self):
        return 'Hand(' + self.get_center().__str__() + ')'

    def changed(self):
        "method called when something is changed"
        if self.parent != None:
            b = self.get_full_bounds()
            
            if b.get_extent() != Point(0, 0):
                self.parent.broken.append(self.get_full_bounds())
                
   
    def draw(self):
        """ hand has nothing more to draw than its children which are the morph that are marked for grab """
        for child in self.children:
            child.draw()
            
    
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
        
                
        if event.type in ['MIDDLEMOUSE','LEFTMOUSE',
                          'RIGHTMOUSE', 'WHEELDOWNMOUSE','WHEELUPMOUSE']:
            return self.process_mouse_up(event)
        else:

            tmp = self.get_morph_at_pointer() #PKHG. at least world?!
            key_release = tmp.key_release()
            
            if key_release == True :
                return {'RUNNING_MODAL'}
            else:
                return {'PASS_THROUGH'}
            
            
        
    
        
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
        """ return all the morphs that are under the current position of the mouse cursor """
    
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

    


