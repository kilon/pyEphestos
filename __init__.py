#-------------------------------------------------
#    morphic.py
#
#    a tree-based GUI for Python
#    inspired by Squeak
#
#    written by Jens Moenig
#    jens@moenig.org
#
#    version 2009-Nov-06
#
#    Copyright (C) 2009 by Jens Moenig
#---------------------------------------
#-------------------------------------------------
#    morpheas.py
#
#    Morpheas is the GUI side of Ephestos based on morphic.py
#
#
#    written by Kilon Alios
#    thekilons@yahoo.co.uk
#
#    version April-2012
#
#    Copyright (C) 2012 by Kilon Alios
#---------------------------------------
#    Permission is hereby granted, free of charge, to any person
#    obtaining a copy of this software and associated documentation
#    files (the "Software"), to deal in the Software without
#    restriction, including without limitation the rights to use, copy,
#    modify, merge, publish, distribute, sublicense, and/or sell copies
#    of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be
#    included in all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
#    yet to implement:
#    - make World customizable before opening it
#    - scroll bars
#    - tool tips
#    - skinnables
#    - turtle trails
#    - better string editing
#    - multi-line edits



bl_info = {
    "name": "Ephestos : The Golden Age",
    "description": "Ephestos is a visual programming language , a GUI and inerface for supercollider",
    "author": "Kilon",
    "version": (0, 0, 1),
    "blender": (2, 6, 3),
    "location": "View3D > Left panel ",
    "warning": 'warn',  # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "https://github.com/kilon/Ephestos",
    "category": "Development"}



if "bpy" in locals():
    import imp
    if "morpheas" in locals():
        imp.reload(morpheas)

import bpy
import bgl
import blf

from bpy.props import *

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



world_initialised = False
world = None
def initialise():
    ##########start of default settings (today example for test_StringInput.py) ##


    #This file uses a World-morph on the 3DView screen of Blender
    #and all events are handled via the hand (an unvisible morph) but
    #can be made visible by a CrossHair-morph
    global world
    global world_initialised
    world_initialised = True
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

    #PKHG to see what world contains:check_contains(world,"world")


    repl = Repl(world)
    world.add(repl)


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
        #context.area.header_text_set("Welcome to Ephestos")
        if context.area:
            context.area.tag_redraw()

        if event.type == 'TIMER':
            return {'PASS_THROUGH'}

        if context.area.type == 'VIEW_3D' and ephestos.running and event.type in {'ESC',}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            ephestos.running = False
            result = {'CANCELLED'}
        elif context.area.type == 'VIEW_3D' and ephestos.running \
                 and event.mouse_region_x > 0 \
                 and event.mouse_region_x < bpy.context.area.regions[4].width\
                 and event.mouse_region_y > 0 \
                 and event.mouse_region_y < bpy.context.area.regions[4].height :
            hand = world.hand
            hand.bounds.origin = Point(event.mouse_region_x, event.mouse_region_y)
            result = hand.process_all_events(event)


        return result

    def invoke(self, context, event):
        global world_initialised
        if context.area.type == 'VIEW_3D' and ephestos.running == False :
            if world_initialised == False: initialise()
            self.cursor_on_handle = 'None'


            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle =bpy.types.SpaceView3D.draw_handler_add(draw_ephestos,(self,context), 'WINDOW', 'POST_PIXEL')
#PKHG.notneeded            self._handle_world = context.region.callback_add(draw_World, (self, context), 'POST_PIXEL')
            self._timer = context.window_manager.event_timer_add(0.01,
                    context.window)
            ephestos.running = True
            context.window_manager.modal_handler_add(self)
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
