#-------------------------------------------------
#    morphic.py
#
#    a tree-based GUI for Python
#    inspired by Squeak
#
#    written by Jens Mönig
#    jens@moenig.org
#
#    version 2009-Nov-06
#
#    Copyright (C) 2009 by Jens Mönig
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

"""
if "bpy" in locals():
    import imp
    imp.reload(morpheas)
    
else:
    from Ephestos import morpheas
"""    

import bpy
import bgl
import blf
from bpy.props import *


def draw_ephestos():
    '''accepts 2 coordinates and a colour then draws
    the line and the handle'''

    

    #set colour to use
    bgl.glColor4f(0.5,0.0,0.5,0.7)

    #draw main line and handles
    #bgl.glBegin(bgl.GL_LINES)
    bgl.glRecti(5,5,bpy.context.area.regions[4].width-5, bpy.context.area.regions[4].height-5)
    #bgl.glEnd()
    x1 = 50
    y1 = 50
    x2 = bpy.context.area.regions[4].width-50
    y2 = bpy.context.area.regions[4].height-50
    color=[0.5,0.5,0.5,1]
    if len(bpy.data.images)>0:
        img = bpy.data.images[0]
        img.gl_load(bgl.GL_NEAREST, bgl.GL_NEAREST)
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, img.bindcode)
        bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MIN_FILTER, bgl.GL_NEAREST)

        bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MAG_FILTER, bgl.GL_NEAREST)
        bgl.glEnable(bgl.GL_TEXTURE_2D)
        bgl.glEnable(bgl.GL_BLEND)
        #bgl.glBlendFunc(bgl.GL_SRC_ALPHA, bgl.GL_ONE_MINUS_SRC_ALPHA)
        bgl.glColor4f(color[0], color[1], color[2], color[3])
        bgl.glBegin(bgl.GL_QUADS)
        bgl.glTexCoord2f(0,0)
        bgl.glVertex2f(x1,y1)
        bgl.glTexCoord2f(0,1)
        bgl.glVertex2f(x1,y2)
        bgl.glTexCoord2f(1,1)
        bgl.glVertex2f(x2,y2)
        bgl.glTexCoord2f(1,0)
        bgl.glVertex2f(x2,y1)
        bgl.glEnd()
        bgl.glDisable(bgl.GL_BLEND)
        bgl.glDisable(bgl.GL_TEXTURE_2D)




def DrawStringToViewport(text, x, y, size, color):
    ''' my_string : the text we want to print
        pos_x, pos_y : coordinates in integer values
        size : font height.
        colour_type : used for definining the colour'''
    my_dpi, font_id = 72, 0 # dirty fast assignment
    bgl.glColor4f(*color)
    blf.position(font_id, x, y, 0)
    blf.size(font_id, size, my_dpi)
    blf.draw(font_id, text)


def InitViewportText(self, context):
    '''used to deligate opengl text printing to the viewport'''
    this_h = context.region.height
    this_w = context.region.width
    dimension_string = "Gyes - RMG (Random Material Generator)"
    explanation_string = "Press ESC to exit"
    DrawStringToViewport(dimension_string, 100, bpy.context.area.height-50, 20, dimension_colour)
    DrawStringToViewport("Material Templates Librarian version 0.01", 100, bpy.context.area.height-70, 20, dimension_colour)
    
    DrawStringToViewport(explanation_string, 10, 7, 40, explanation_colour)
    DrawStringToViewport("Region : "+ bpy.context.area.regions[4].type, 10, 100, 20, explanation_colour)

def InitGLOverlay(self, context):
    

    # 50% alpha, 2 pixel width line
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 0.5)
    bgl.glLineWidth(1.5)

    # start visible drawing
    draw_ephestos()
    InitViewportText(self, context)

    # restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)


class open_ephestos(bpy.types.Operator):
    bl_idname = "ephestos.open"
    bl_label = "Ephestos"

    def modal(self, context, event):
        context.area.tag_redraw()

        
        if event.type in ('ESC'):
            context.region.callback_remove(self._handle)
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            self.cursor_on_handle = 'None'
            context.window_manager.modal_handler_add(self)

            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle = context.region.callback_add(InitGLOverlay, (self, context), 'POST_PIXEL')
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Image View not found, cannot run operator")
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
        box.operator("ephestos.open")
        



        
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

 
if __name__ == "__main__":
    register()
    