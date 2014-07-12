
#PKHG.error from .world import * #PKHG test 0505012
from .menu import *
from .rectangle import *

class yesnoMenu(Morph):
    def __init__(self,x,y,parent):
        super(yesnoMenu, self).__init__()
        self.parent = parent
        parent.children.append(self)
        self.x = x
        self.y = y
#OK  300 300         print(x,y)
        self.position = Point(x,y)
        self.bounds = Rectangle(self.position, Point(x + 60, y + 120))
        print("----yesno L16 x,y,position and bounds = ", x,y,self.position,self.bounds)
        print("==== yesnomenu L16 yesnobounds  = ", self.bounds)
        print("yesno built")
        self.name = "YesNo"
        self.with_name = True
        self.my_context_menu()
        self.color = (0, 1, 0, 0.5)
#        self.rounded = True
        self.my_draw()
        
    def my_context_menu(self):
        position = self.position
        tmp =  Rectangle(position, position + 30)
        quit = Morph(bounds = tmp)
        quit.name = 'quit'
        quit.with_name = True
        quit.is_visible = True
        quit.color = (0,0,.5,.6)
        quit.set_position(position)
        self.parent.children.append(quit)
        self.add(quit)
        
        tmp =  Rectangle(position, position + 30)
        no = Morph(bounds = tmp)
        no.name = 'no'
        no.with_name = True
        no.is_visible = True
        no.color = (0,0,.5,.6)
        no.set_position(Point(position.x, position.y + 30))
        self.parent.children.append(no)
        self.add(no)
        
        tmp =  Rectangle(position, position + 30)
        yes = Morph(bounds = tmp)
        yes.name = 'yes'
        yes.with_name = True
        yes.is_visible = True
        yes.color = (0,0,.5,.6)
        yes.set_position(Point(position.x,position.y + 60))
        self.parent.children.append(yes)
        self.add(yes)        
#        menu.add_item("Yes","yes_option")
#        menu.add_item("No","no_option")

    def my_draw(self):
        world = self
        print("world = ???",world, self.parent)
        print(self.children[:])
#???        ch0 = self.children[0]
#        self.children[0].draw()
#        print("L39 yesnomenu bounds of ", ch0,ch0.bounds)
#        ch0.position = self.position
        self.draw()
    '''
    def draw(self):
        #PKHG delete needed because of ...
        for m in self.children:
            m.delete()
        for pair in self.items:
            item = MenuItem(self.target, pair[1], pair[0])            
            item.with_name = True
    '''        
        
    def mouse_down_left(self, pos):
        print("\nyesno mouse_down_left callde\n=====")
        result = True
        '''
        if self.action == "yes_option":
            result = "Yes"
        elif self.action == "no_option":
            result = "No"        else:
            self.delete()
        '''
        return result
