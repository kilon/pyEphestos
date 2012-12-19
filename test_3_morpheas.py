from bpy.props import  StringProperty, BoolProperty

import bpy
import bgl
import blf
from .morpheas import *


pwBot = Point(30,30)
pwTop = Point(200,400)


world= World()
hand = Hand()
world.add(hand)

test_Menu = Menu(title="Menu I am ")
test_Menu.name = "I am a Menu"
test_Menu.is_draggable = False #should be fixed?!
test_Menu.with_name = True
#PKHG.no effect: test_Menu.bounds = Point(0,200).corner(Point(10,220))
#test test_Menu.set_position(Point(50,200))
test_Menu.set_position(Point(0,0))
#test_Menu.color = (1,0,0,0)

#PKHG test 5-5-2012 8:24
test_Menu.add_line() #debug050512_1659 shows a blue line
test_Menu.add_item(label = '1') #no params ==> label="close", action='nop'
test_Menu.add_line() #debug050512_1659 shows a blue line
test_Menu.add_item(label = '2') #no params ==> label="close", action='nop'

test_Menu.add_line() #debug050512_1659 shows a blue line
test_Menu.add_item(label = 'add abracadabra') #no params ==> label="close", action='nop'
test_Menu.add_line() #debug050512_1659 shows a blue line
    
test_Menu.add_item(action='close_my_Menu') #no params ==> label="close", action='nop'
test_Menu.add_line() #debug050512_1659 shows a blue line
test_Menu.add_input_StringField(default = 'change me',width = 300)

#PKHG.0505: not at good place:  test_Menu.add_input_StringField(default='I am Text field and may be changed')

test_MenuItem = MenuItem(label = "test_menu_item")
test_MenuItem.set_position(Point(100,150))
test_MenuItem.create_label()
test_MenuItem.name = "I am a MenuItem"
#test_MenuItem.with_name = True
#???test_MenuItem.set_position(Point(20,300))
#PKHG.reason see below in comment: test_Menu.add(test_MenuItem)

print("test L51 items of test_Menu", test_Menu.items[:])
print("childrens of test_Menu = ",test_Menu.children[:])

#060512 add a Trigger to show the Menu!
trigger_show_Menu = Trigger(action='show_Menu')
trigger_show_Menu.set_position(Point(100,100))
trigger_show_Menu.set_color(color='blue')
trigger_show_Menu.with_name = True
world.add(trigger_show_Menu)


button1 = Button(label="button" )
button1.border = 10
button1.bounds = Rectangle(Point(0,0), Point(40,40))
button1.set_position(Point(200,200))
col = (1,0,0,1)
button1.set_color(color = 'green') 
print("default button bounds ", button1.bounds, " extent = ", button1.get_extent())
world.add(button1)

#at this moment a Menu should be added latest to world!
world.add(test_Menu)


'''
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
'''

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
            print("=======> start hand actions: test_3 L127 event type :", \
                  event.type," event value : ",event.value,\
                  " next hand is called!")
            hand.bounds.origin = Point(event.mouse_region_x, event.mouse_region_y)
            res = hand.process_all_events(event) #{'RUNNING_MODAL'}
            print("=======> end hand actions result of process_all_events =",res, "\n")
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
    
        
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

 
if __name__ == "__main__":
    register()
    
