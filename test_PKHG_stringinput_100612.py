#PKHG: this file to test InputField 100612
debug_show_acttions_of_handle = False

from bpy.props import  StringProperty, BoolProperty

import bpy
import bgl
import blf
from .morpheas import *
#######
def check_contains(cl,name , print_value = True, no_underscore = True):
    dir_class = dir(cl)
    for el in dir_class:
        if el.startswith("_") and no_underscore:
            pass
        else:
            if print_value:
                tmp = getattr(cl,el)
#                if el == 'stringfield_ID':
                print(name , " contains ==>",el," value = ", tmp)
            else:
                print(name , " contains ==>",el)
    print("\ncheck_contains finished\n\n")

##########start of default settings (today example for test_StringInput.py) ##


#This file uses a World-morph on the 3DView screen of Blender
#and all events are handled via the hand (an unvisible morph) but
#can be made visible by a CrossHair-morph
world = World()
hand = world.hand
hand.name = "MAIN hand"
tmp = hand.kbd_listener
world.kbd_listener = tmp #PKHG: this worlds keyboardListener

crosshair = CrossHair(hand)
crosshair.name = "MAIN crosshair"
world.add(crosshair)

#at least one Menu will be visible in the lower left corner
#Big if it is in developpers mode small if not needed
#it is the menu built for the context of the world
world_menu = world.context_menu()
world_menu.target = world
world_menu.name = "MAIN menu of world"
world_menu.create_my_objects()

#test a Text morph as an about, always visible in the world_menu
#Text is a multline morph
about = Text("Ephestos: Age of Morpheas \n (c)  2012 by PKHG and Kilon  [ thekilon@yahoo.co.uk ] .GPL Licence . Based on Pymorphic.py by Jens Moenig [ jens@moenig.org ] \n ", max_width = 390 , fontsize = 16)

#normal procedur#give it a name
#give it a startposition
#set its visbility
#add it (a must yet) to the world see later!
#PKHG.TODO.??? make this a def?
about.name = "About"
about.set_position(Point(200,200))
about.is_visible = False

#######to be compatible with 0905 state of git START ???!!!
#test Blinker 16092012
blinker = Blinker()
blinker.set_position(Point(450,300))
blinker.is_visible = False
world.add(blinker)

##StringInput test

#stringinput = StringInput(kbd_listener = hand.kbd_listener, default="test StringInput  pkhg")
stringinput = StringInput(hand, blinker, default="mouse here! if GREEN light type!")

world.stringinput_ID = id(stringinput)
stringinput.set_position(Point(400,200))
stringinput.name = "I am IP"
stringinput.is_visible = False
stringinput.with_name = True
#stringinput.keyboard_listener = world.keyboard_listener
world.add_child(stringinput)


#add als default morphs to the world!
#we know by the following world.add lines which child in
#world.children is what (but better do not rely on this)
world.add(world_menu)
world.add(about)

#add a texture morph
textured_morph = Morph()
textured_morph.set_texture( "swatch.png" )
textured_morph.set_position(Point(600,100))
world.add(textured_morph)
tex2_morph = Morph(bounds = Rectangle(Point(0,0),Point(200,200)))
tex2_morph.set_texture("weetniet.png")
tex2_morph.set_position(Point(600,200))
world.add(tex2_morph)
print("textured_morph x position: ",textured_morph.get_position().x)
print("textured_morph y position: ",textured_morph.get_position().y)
print("textured_morph height : ",textured_morph.get_height())
print("textured_morph width : ",textured_morph.get_width())
#PKHG to see what world contains:check_contains(world,"world")


repl = Repl(world)
world.add(repl)

print("start of test_PKHG")
#PKHG is now ok, maybe cleaned now:for el in world.children:print(el,"its id = ",id(el))
#for el in world.children: print(id(el))

##########end of default settings ########################

########## do not change the following code ##############
class ephestos:
    running = False


def draw_ephestos(self,context):
    global show_world
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 0.5)
    bgl.glLineWidth(1.5)


#    if show_world:
    world.draw()

    # restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)

class open_ephestos(bpy.types.Operator):
    bl_idname = "ephestos_button.modal"
    bl_label = "enable Ephestos"
    _timer = None
    def modal(self, context, event):
        result =  {'PASS_THROUGH'}
        context.area.tag_redraw()

        if context.area:
            context.area.tag_redraw()

        if event.type == 'TIMER':
            return {'PASS_THROUGH'}

        if context.area.type == 'VIEW_3D' and ephestos.running and event.type in {'ESC',}:
            context.region.callback_remove(self._handle)
            ephestos.running = False
            print("CANCELLED")
            result = {'CANCELLED'}
        elif context.area.type == 'VIEW_3D' and ephestos.running \
                 and event.mouse_region_x > 0 \
                 and event.mouse_region_x < bpy.context.area.regions[4].width\
                 and event.mouse_region_y > 0 \
                 and event.mouse_region_y < bpy.context.area.regions[4].height :
            if debug_show_acttions_of_handle:
                print("=======> start hand actions: test_3 L127 event type :", \
                  event.type," event value : ",event.value,\
                  " next hand is called!")
            hand.bounds.origin = Point(event.mouse_region_x, event.mouse_region_y)
            res = hand.process_all_events(event) #{'RUNNING_MODAL'}
            if debug_show_acttions_of_handle:
                print("=======> end hand actions result of process_all_events =",res, "\n")
#fort test of events only            print("\n=======>>>> event info: type=", event.type,"\n value=", event.value)
            return(res)
        else:
#            print("event type :" ,event.type)
#            print("event value : ",event.value)
#            print("PASS THROUGH")
            pass
        return result

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D' and ephestos.running == False :

            self.cursor_on_handle = 'None'
            context.window_manager.modal_handler_add(self)

            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle = context.region.callback_add(draw_ephestos, (self, context), 'POST_PIXEL')
#PKHG.notneeded            self._handle_world = context.region.callback_add(draw_World, (self, context), 'POST_PIXEL')
            self._timer = context.window_manager.event_timer_add(0.01,
                    context.window)
            ephestos.running = True
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Ephestos is already opened and running")
            return {'CANCELLED'}

# this the main panel
bpy.types.Scene.text_for_text = StringProperty(name="change text",\
           default= "Change me",description ="Test for changing morph text")
bpy.types.Scene.text_for_input = StringProperty(name="input",default="for input",\
             description="used for StringFields")
bpy.types.Scene.world_is_running = BoolProperty(name="next action", default = False,\
           description="toggle showing the  world")

old_text = "Change me"

class the_world(bpy.types.Operator):
    bl_idname = "world.toggle"
    bl_label = "start or stop showing the world"

    def execute(self, context):
        global world
        result = {"PASS_THROUGH"}
        sce = context.scene
        runing_value = sce.world_is_running
        if runing_value:
            world.running = True
            sce.world_is_running = False
        else:
            world.running = False
            result = {'FINISHED'}
            sce.world_is_running = True
        return result

#stringfield_input = "for input"
class change_text(bpy.types.Operator):
    bl_idname = "textmorph.text"
    bl_label = "TestchangeText"

    def execute(self,context):
        global text, old_text
        sce = context.scene
        if old_text != sce.text_for_text:
            old_text = sce.text_for_text
            multiline_text.adjust_text(old_text)
        return {'FINISHED'}
'''
class for_stringfield_text(bpy.types.Operator):
    bl_idname = "forinput.text"
    bl_label = "change global stringfield"

    def execute(self,context):
        global stringfield_input
        sce = context.scene
        if  stringfield_input!= sce.text_for_input:
            stringfield_input = sce.text_for_input
        return {'FINISHED'}
'''

# button for toggling visibility of green morph, to test morp.hide() and morph.show() together with world.draw()
class morph_visibility(bpy.types.Operator):
    bl_idname = "morph.visibility"
    bl_label = "toggle visibility of green morph"

    def execute(self,context):

        global mymorph1

        if  mymorph1.is_visible:
            mymorph1.hide()
        else:
            mymorph1.show()
        return {'FINISHED'}

class ephestos_panel(bpy.types.Panel):
    bl_label = "Ephestos"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    def draw(self, context):
        sce = context.scene
        layout = self.layout
        box = layout.box()
        box.label(text="Ephestos WIP not finished yet")
        box.operator("ephestos_button.modal")
#        col = layout.column()
#        col.prop(sce,'world_is_running')
#        col.operator('world.toggle')
#        col.prop(sce,'text_for_text')
#        col.operator('textmorph.text')
#        col.prop(sce,'text_for_input')
#        col.operator('forinput.text')
#        col.operator('morph.visibility')


def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
