#------------------------------------------
#   pyEphestos
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
#
#    Under GPL license for more info see the Blender license
#
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



bl_info = {
    "name": "Ephestos : The Golden Age",
    "description": "Ephestos is a communication tool to allow Pharo to control Blender",
    "author": "Kilon",
    "version": (0, 0, 1),
    "blender": (2, 6, 3),
    "location": "View3D > Left panel ",
    "warning": 'warn',  # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "https://github.com/kilon/pyEphestos",
    "category": "Development"}



import bpy
from bpy.props import *
ephestos_running = False

class open_ephestos(bpy.types.Operator):
    bl_idname = "ephestos_button.modal"
    bl_label = "enable Ephestos"
    _timer = None

    def modal(self, context, event):
        global ephestos_running
        result =  {'PASS_THROUGH'}
        context.area.tag_redraw()
        #context.area.header_text_set("Welcome to Ephestos")
        if context.area:
            context.area.tag_redraw()

        if event.type == 'TIMER':
            return {'PASS_THROUGH'}

        if context.area.type == 'VIEW_3D' and ephestos_running and event.type in {'ESC',}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            ephestos_running = False
            result = {'CANCELLED'}



        return result

    def invoke(self, context, event):
        global ephestos_running
        if context.area.type == 'VIEW_3D' and ephestos_running == False :
            self.cursor_on_handle = 'None'

            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            #self._handle =bpy.types.SpaceView3D.draw_handler_add(draw_ephestos,(self,context), 'WINDOW', 'POST_PIXEL')

            self._timer = context.window_manager.event_timer_add(0.01,
                    context.window)
            ephestos_running = True
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Ephestos is already opened and running")
            return {'CANCELLED'}


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


def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
