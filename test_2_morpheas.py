from bpy.props import  StringProperty, BoolProperty

import bpy
import bgl
import blf
from .morpheas import *


pwBot = Point(30,30)
pwTop = Point(200,400)

#PKHG>not yet ok
one_String = String("Hallo everybody")
one_String.set_position(Point(60,60))

good_rounded_box = RoundedBox( )
#PKHG.works ;-)good_rounded_box.bounds = Point(30,30).corner(Point(200,400))
good_rounded_box.set_position(Point(140,50))
good_rounded_box.name = "roundedBox"
good_rounded_box.color = (1, 0, 0, 1)
#good_rounded_box.alpha = 0.8

#PKHG.check size of brackets!
multiline_text = Text("[] {}()\n[] {}()\nPKHG = Peter\nline >=4\n[] {}()\nand this too and more and more [] {}()", max_width = 200)
#multiline_text = Text("PKHG  was here", max_width = 200) 
multiline_text.set_position(Point(70,70))

p1 = Point(240,50)
p2 = Point(280,120)
bounds_red = Rectangle(p1,p2)

red_morph= Morph( bounds = bounds_red, rounded = True, with_name = True)
green_morph= Morph()
blue_morph= Morph()
world= World()

rounded_box = RoundedBox(border = 30, outer_per =.1, inner_per = 0.5)#does not work yet why???b bottom_left= p1, top_right = p2)
rounded_box.bounds = Rectangle(Point(0,200),Point(400,400))
rounded_box.color = (1, 1, 1, .5)
rounded_box.bordercolor = (0, 0, 0, 1)
rounded_box.set_position(Point(200,200))

test_Menu = Menu(title="I am a Menu kjshjfhskjfhkashfkashf ")
test_Menu.name = "I am a Menu"
test_Menu.with_name = True
test_Menu.bounds = Rectangle(Point(0,200),Point(300,400))
test_Menu.set_position(Point(50,220))
#PKHG test 5-5-2012 8:24
test_Menu.add_line()
test_Menu.add_item()
#???? test_Menu.add_entry(default='may be changed')
print("test L51 items of test_Menu", test_Menu.items[:])
print("childrens of test_Menu = ",test_Menu.children[:])
world.add(test_Menu)

test_Bouncer = Bouncer()
test_Bouncer.set_position(Point(30,250))
test_Bouncer.color = (0,1,0,.4)
world.add(test_Bouncer)

#PKHG test 5-5-2012 8:24
test_ListMenu = ListMenu()
test_ListMenu.build_menus()
test_ListMenu.set_position(Point(25,240))
world.add(test_ListMenu)


test_Trigger = Trigger()
test_Trigger.name = "I am a Trigger"
test_Trigger.with_name = True
test_Trigger.set_position(Point(20,300))
world.add(test_Trigger)

world.add(red_morph)
world.add(green_morph)
world.add(blue_morph)
world.add(multiline_text)
world.add(rounded_box)
world.add(good_rounded_box)
#PKHG.not yet ok
world.add(one_String)
#????world.add(info_String)
#PKHG.stringfieldTest.???
#????world.start_all_bouncers()
info_String = String("Mouse over FieldString ")
info_String.is_visible = False
info_String.name = "Info_input"
#info_String.set_position(Point(5,5))

test_stringfield = StringField(default="input test")
test_stringfield.name ="input..."
test_stringfield.with_name = True

test_stringfield.add(info_String)
info_String.set_position(test_stringfield.bounds.corner)

world.add(test_stringfield)
#via test_stringfield: world.add(info_String)

green_morph.set_position(Point(150,150))
blue_morph.set_position(Point(350,350))
hand = Hand()
# hand.attach_to_world(world)
world.add(hand)
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
    mW.draw()    
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
            print("test L147 event type :" ,event.type," event value : ",event.value)
            hand.bounds.origin = Point(event.mouse_region_x, event.mouse_region_y)
            res = hand.process_all_events(event) #{'RUNNING_MODAL'}
            print("test L150  result of process_all_events =",res, "\n")
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
    
