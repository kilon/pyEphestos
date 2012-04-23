from .point import *
from .morph import *

class Hand(Morph):
    "I represent the mouse cursor"

    def __init__(self):
        super(Hand, self).__init__()
        self.world = None
        self.mouse_over_list = []
        self.mouse_down_morph = None
        self.morph_to_grab = None
        self.moving_morph= False
        self.bounds = Point(0, 0).corner(Point(0,0))

    def __repr__(self):
        return 'Hand(' + self.center().__str__() + ')'

    def attach_to_world(self, world):
        self.world = world

    def changed(self):
        print("\n--dbg pkgh changed called")
        if self.world != None:
            b = self.full_bounds()
            print("--dbg pkhg b = self.full_bounds() extent", b, b.extent())
            if b.extent() != Point(0, 0):
                self.world.broken.append(self.full_bounds())
                print("--dbg pkhg world.broken", self.world.broken[:])

    def draw_on(self, rectangle=None):
        pass

    def process_mouse_event(self, event):
        if event.type == 'MOUSEMOVE':
            return self.process_mouse_move(event)
        elif event.value=='PRESS':
            return self.process_mouse_down(event)
        elif event.value=='RELEASE':
            return self.process_mouse_up(event)

    def morph_at_pointer(self):
        morphs = self.world.children
        for m in morphs[::-1]:
            if m.full_bounds().contains_point(self.bounds.origin) and m.is_visible:
                return m.morph_at(self.bounds.origin)
        return self.world

    def all_morphs_at_pointer(self):
        answer = []
        # morphs = self.world.all_children()
        morphs = self.world.children
        for m in morphs:
            if m.is_visible and (m.full_bounds().contains_point
                                 (self.bounds.origin)):
                answer.append(m)
        return answer

    #Hand dragging and dropping:

    def drop_target_for(self, morph):
        target = self.morph_at_pointer()
        while target.wants_drop_of(morph) == False:
            target = target.parent
        return target
#Hand
    def grab(self, morph):
        if self.children == []:
            self.world.stop_editing()
            self.add(morph)
            self.changed()
            print("morph has been grabbed")

    def drop(self):
        if self.children != []:
            morph = self.children[0]
            target = self.drop_target_for(morph)
            self.changed()
            target.add(morph)
            morph.changed()
            self.morph_to_grab = None
            self.children = []
            self.set_extent(Point(0, 0))

            print("morph has been droped")


    #Hand event dispatching:

    def process_mouse_down(self, event):
        returned_value = {'PASS_THROUGH'}
        if self.children != []:
            self.drop()
        else:
            pos = Point(event.mouse_region_x,
                        event.mouse_region_y)
            morph = self.morph_at_pointer()

            is_menu_click = False

            """for m in morph.all_parents():
                if isinstance(m, Menu) or isinstance(m, Widget):
                    is_menu_click = True
            if not is_menu_click:
                if isinstance(world.open_menu, SelectionMenu):
                    world.open_menu.choice = False
                elif isinstance(world.open_menu, Menu):
                    world.open_menu.delete()

            if world.text_cursor != None:
                if morph is not world.text_cursor.target:
                    world.stop_editing()"""

            self.morph_to_grab = morph.root_for_grab()
            print("self.morph_to_grab : ",self.morph_to_grab )
            if morph.is_draggable:
                self.moving_morph =True
            while not morph.handles_mouse_click():
                morph = morph.parent
            self.mouse_down_morph = morph
            if event.type == 'LEFTMOUSE':
                morph.mouse_down_left(pos)


            elif event.type == 'MIDDLEMOUSE':
                morph.mouse_down_middle(pos)
            elif event.type == 'RIGHTMOUSE':
                morph.mouse_down_right(pos)
            else:
                pass
        return returned_value

    def process_mouse_up(self, event):
        if self.children != []:
            self.drop()
            if self.moving_morph == True:
                    self.moving_morph = False
                    print("movement finished")
        else:
            pos = Point(event.mouse_region_x,
                        event.mouse_region_y)
            morph = self.morph_at_pointer()

            is_menu_click = False
            """for m in morph.all_parents():
                if isinstance(m, Menu) or isinstance(m, Widget):
                    is_menu_click = True"""
            """
            if event.type == 'RIGHTMOUSE' and event.value == 'RELEASE' and not is_menu_click:
                menu = morph.context_menu()
                if menu != None:
                    menu.popup_at_hand()

                    """

            while not morph.handles_mouse_click():
                morph = morph.parent

            if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                morph.mouse_up_left(pos)

                if morph is self.mouse_down_morph:
                    morph.mouse_click_left(pos)

            elif event.type == 'MIDDLEMOUSE' and event.value == 'RELEASE':
                morph.mouse_up_middle(pos)
                if morph is self.mouse_down_morph:
                    morph.mouse_click_middle(pos)
            elif event.type == 'RIGHTMOUSE' and event.value =='RELEASE' and not is_menu_click:
                morph.mouse_up_right(pos)
                if morph is self.mouse_down_morph:
                    morph.mouse_click_right(pos)
            else:
                pass
        return {'PASS_THROUGH'}

    def process_mouse_move(self, event):
        value_returned = {'PASS_THROUGH'}
        mouse_over_new = self.all_morphs_at_pointer()
        if self.children == [] and event.type == 'MOUSEMOVE':
            top_morph = self.morph_at_pointer()
            if top_morph.handles_mouse_move():
                pos = Point(event.mouse_region_x,
                            event.mouse_region_y)
                top_morph.mouse_move(pos)
            morph = top_morph.root_for_grab()
            if morph is self.morph_to_grab and morph.is_draggable:

                self.grab(morph)
                value_returned = {'RUNNING_MODAL'}



        for old in self.mouse_over_list:
            if old not in mouse_over_new :
                old.mouse_leave()
                if event.type == 'MOUSEMOVE':
                    old.mouse_leave_dragging()
                    print("I am dragging the old morph")

        for new in mouse_over_new:
            if new not in self.mouse_over_list:
                new.mouse_enter()
                if event.type == 'MOUSEMOVE':
                    new.mouse_enter_dragging()

            print("I am dragging the  new morph")



        if self.children != [] and event.type == 'MOUSEMOVE' and self.moving_morph == True:
            self.morph_to_grab.set_position(self.bounds.origin)
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

    


