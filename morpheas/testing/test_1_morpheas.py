
import bpy
import bgl
import blf
#from bpy.props import *
#from Ephestos import morpheas
from . basics_morpheas import Point, Rectangle, Node
from . class_Morph import Morph
from . class_Text import Text
from . class_RoundedBox import RoundedBox
from . class_World import World
from . class_Hand import Hand


pwBot = Point(30,30)
pwTop = Point(200,400)
good_rounded_box = RoundedBox( )
#good_rounded_box.bounds = Point(30,30).corner(Point(200,400))
good_rounded_box.set_position(Point(40,40))
good_rounded_box.name = "roundedBox"
good_rounded_box.color = (1, 0, 0, 1)
good_rounded_box.alpha = 0.8

text = Text("PKHG = Peter\nline 2\nand this too and more and more")
text.set_position(Point(70,70))
p1 = Point(40,50)
p2 = Point(80,120)
bounds_red = p1.corner(p2)

red_morph= Morph( bounds = bounds_red, rounded = True, with_name = True)
green_morph= Morph()
blue_morph= Morph()
world= World()

rounded_box = RoundedBox(border = 30)#does not work yet why???b bottom_left= p1, top_right = p2)
rounded_box.bounds = Point(0,0).corner(Point(200,400))
rounded_box.color = (1, 1, 1, .5)
rounded_box.bordercolor = (0, 0, 0, 1)

rounded_box.set_position(Point(200,200))

world.add(red_morph)
world.add(green_morph)
world.add(blue_morph)
world.add(text)
world.add(rounded_box)
world.add(good_rounded_box)

green_morph.set_position(Point(150,150))
blue_morph.set_position(Point(350,350))
hand = Hand()
hand.attach_to_world(world)
red_morph.color= (1.0,0.0,0.0, 1.0)
red_morph.name = "RED"
green_morph.color= (0.0,1.0,0.0, 0.5)
green_morph.name = "GREEN"
blue_morph.color= (0.0,0.0,1.0, 0.3)
blue_morph.name = "BLUE"

class World:
    running = False
    mouse_region_x = 0
    mouse_region_y = 0

def draw_World(self,context):
    global world
    mW = world #World() #was Morph
    bgl.glEnable(bgl.GL_BLEND)
#for world    draw_rounded_morph(mW)
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
    good_rounded_box.draw_new(ephestos)
    world.draw_new(ephestos)
#        show_world = False
    red_morph.draw_new(ephestos)
    green_morph.draw_new(ephestos)
    blue_morph.draw_new(ephestos)
    text.draw_new(ephestos)
    rounded_box.draw_new(ephestos)
    # restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)
    
class open_ephestos(bpy.types.Operator):
    bl_idname = "ephestos_button.modal"
    bl_label = "Ephestos"

    def modal(self, context, event):
        result =  {'PASS_THROUGH'}
        context.area.tag_redraw()                
        if context.area.type == 'VIEW_3D' and ephestos.running and event.type in ('ESC'):
            context.region.callback_remove(self._handle)
            ephestos.running = False
            print("CANCELLED")
            result = {'CANCELLED'}
        elif context.area.type == 'VIEW_3D' and ephestos.running \
                 and event.type in ('MOUSEMOVE','LEFTMOUSE','RIGHTMOUSE')\
                 and event.mouse_region_x > 0 \
                 and event.mouse_region_x < bpy.context.area.regions[4].width\
                 and event.mouse_region_y > 0 \
                 and event.mouse_region_y < bpy.context.area.regions[4].height :
#            print("RUNNING_MODAL")
#            print("event type :" ,event.type)
#            print("event value : ",event.value)
            hand.bounds.origin = Point(event.mouse_region_x, event.mouse_region_y)
            hand.process_mouse_event(event) #{'RUNNING_MODAL'}            
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
    
