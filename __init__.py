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
#    version March-2012
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
    "warning": '',  # used for warning icon and text in addons panel
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.5/Py/Scripts/System/Gyes",
    "tracker_url": "https://github.com/kilon/Ephestos",
    "category": "Development"}


if "bpy" in locals():
    import imp
    imp.reload(Ephestos.morpheas)
    
else:
    from Ephestos import morpheas
   

import bpy
import bgl
import blf
from bpy.props import *

text = morpheas.Text("PKHG = Peter\nline 2\nand this too and more and more")
text.set_position(morpheas.Point(70,70))
p1 = morpheas.Point(40,50)
p2 = morpheas.Point(80,120) 
mymorph= morpheas.Morph( top_right = p2,rounded = True, with_name = True)
morph2= morpheas.Morph(bot_left = p1, top_right = p2)
morph3= morpheas.Morph()
world= morpheas.World()

world.add(mymorph)
world.add(morph2)
world.add(morph3)
world.add(text)

morph2.set_position(morpheas.Point(150,150))
morph3.set_position(morpheas.Point(350,350))
hand = morpheas.Hand()

hand.attach_to_world(world)
mymorph.color= (1.0,0.0,0.0)
mymorph.name = "red"
morph2.color= (0.0,1.0,0.0)
morph2.name = "green"
morph3.color= (0.0,0.0,1.0)
morph3.name = "blue"

class World:
    running = False
    mouse_region_x = 0
    mouse_region_y = 0

def draw_World(self,context):
    global world
    mW = world #morpheas.World() #was Morph
    bgl.glEnable(bgl.GL_BLEND)
#for world    morpheas.draw_rounded_morph(mW)
    mW.draw_new()    
    return

show_world = True 


class ephestos:
    running = False
    

def draw_ephestos(self,context):
    global show_world
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 0.5)
    bgl.glLineWidth(1.5)

    """
    #set colour to use
    bgl.glColor4f(0.5,0.0,0.5,0.3)

    x_region = round((bpy.context.area.regions[4].width-5)/2)
    y_region = round((bpy.context.area.regions[4].height-5)/2)
    print("x_region : ",x_region)
    print("y_region : ",y_region)
    bgl.glRecti(5,5,x_region, y_region)
    """
#    if show_world:
    world.draw_new()
#        show_world = False
    mymorph.draw_new(ephestos)
    morph2.draw_new(ephestos)
    morph3.draw_new(ephestos)
    text.draw_new(ephestos)
    # restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)
    
class open_ephestos(bpy.types.Operator):
    bl_idname = "ephestos_button.modal"
    bl_label = "Ephestos"

    def modal(self, context, event):
        context.area.tag_redraw()
        
        
        if context.area.type == 'VIEW_3D' and ephestos.running and event.type in ('ESC'):
            context.region.callback_remove(self._handle)
            ephestos.running = False
            print("CANCELLED")
            return {'CANCELLED'}
        elif context.area.type == 'VIEW_3D' and ephestos.running and event.type in ('MOUSEMOVE','LEFTMOUSE','RIGHTMOUSE') and event.mouse_region_x > 0 and event.mouse_region_x < bpy.context.area.regions[4].width and event.mouse_region_y > 0  and event.mouse_region_y < bpy.context.area.regions[4].height :
            print("RUNNING_MODAL")
            print("event type :" ,event.type)
            print("event value : ",event.value)
            hand.bounds.origin = morpheas.Point(event.mouse_region_x, event.mouse_region_y)
            return hand.process_mouse_event(event) #{'RUNNING_MODAL'}   
        else:
            print("event type :" ,event.type)
            print("event value : ",event.value)
            print("PASS THROUGH")
            return {'PASS_THROUGH'}
         

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D' and ephestos.running == False :
            
            self.cursor_on_handle = 'None'
            context.window_manager.modal_handler_add(self)

            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle = context.region.callback_add(draw_ephestos, (self, context), 'POST_PIXEL')
#PKHG.notneeded            self._handle_world = context.region.callback_add(draw_World, (self, context), 'POST_PIXEL')            
            ephestos.running = True
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Ephestos is already opened and running")
            return {'CANCELLED'}

# this the main panel
class ephestos_panel(bpy.types.Panel):
    bl_label = "Ephestos"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
   
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Ephestos WIP not finished yet")
        box.operator("ephestos_button.modal")
        



        
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

 
if __name__ == "__main__":
    register()
    
