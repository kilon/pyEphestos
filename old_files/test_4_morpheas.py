debug_show_acttions_of_handle = False

from bpy.props import  StringProperty, BoolProperty

import bpy
import bgl
import blf
from .morpheas import *


world = World()
#shows indeed only About and developers choice world.is_dev_mode = False
hand = Hand()
world.add(hand)
crosshair = CrossHair(hand)
world.add(crosshair)
#menu = Menu()
#menu.context_menu()
#world.add(menu)
world_menu = world.context_menu()
about = Text("About\nbased on pymorpheas\nmorph adjusted for Blender\nby Dimitris and Peter", max_width = 350)
about.name = "About"
#multiline_text = Text("PKHG  was here", max_width = 200) 
about.set_position(Point(200,200))
about.is_visible = False
world.add(about)

### test InputStringMorph
stringMorph = InputStringMorph(text="hallo by PKHG")
stringMorph.is_visiable = False
stringMorph_id = id(stringMorph)
print("\n\n stringMorph_id", stringMorph_id)
world_menu.stringField_ID = stringMorph_id

stringMorph.set_position(Point(250,200))
world.add(stringMorph)


yesno = yesnoMenu(300,300, world)
#world.add(yesno)

yesno.is_visible = True
yesno.width_name = True
mymorph1= Morph()
mymorph1.name="MMM 1111  ttttttttttttttttttt"
mymorph1.with_name = True
print(mymorph1.bounds)
#mymorph1.set_color(1.0,0.0,0.0,1)
mymorph1.set_color("green")
mymorph1.set_position(Point(300,200))
#print("test 4\n",dir(world_menu), "\n------end test_4")
world.add(world_menu)
world.add(mymorph1)

#for el in world.children: print(id(el))
#world.add(yesno)
mymorph1.set_position(Point(300,300))

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
    world.draw()
    '''
    good_rounded_box.draw_new(ephestos)
    world.draw_new(ephestos)
#        show_world = False
    red_morph.draw_new(ephestos)
    green_morph.draw_new(ephestos)
    blue_morph.draw_new(ephestos)
    multiline_text.draw_new(ephestos)
    rounded_box.draw_new(ephestos)
    one_String.draw_new(ephestos)
#PKHG.stringfieldTest.???
    test_stringfield.draw_new( ephestos)
    '''
    # restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)
    
class open_ephestos(bpy.types.Operator):
    bl_idname = "ephestos_button.modal"
    bl_label = "enable Ephestos"

    def modal(self, context, event):
        result =  {'PASS_THROUGH'}
        context.area.tag_redraw()                
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

stringfield_input = "for input"    
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

class for_stringfield_text(bpy.types.Operator):
    bl_idname = "forinput.text"
    bl_label = "change global stringfield"

    def execute(self,context):
        global stringfield_input
        sce = context.scene
        if  stringfield_input!= sce.text_for_input:
            stringfield_input = sce.text_for_input
        return {'FINISHED'}  

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
        col = layout.column()
        col.prop(sce,'world_is_running')
        col.operator('world.toggle')
        col.prop(sce,'text_for_text')
        col.operator('textmorph.text')
        col.prop(sce,'text_for_input')
#        col.operator('forinput.text')
        col.operator('morph.visibility')
    
        
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

 
if __name__ == "__main__":
    register()
    
