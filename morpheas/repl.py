#PKHG trying to build a Read Eval Print Loop REPL ;-)

from .morph import *
from .rectangle import *
from .text import *


class Repl(Morph):
    """a morph to Read Eval Print Loop python lines """

    def __init__(self, world = None, name = "REPL"):
        super(Repl, self).__init__(with_name = True)
        self.world = world
        self.set_position(Point(200,200))
        self.name = name
        self.info_test = Text("I will try to\nRead\nEval\nPrint\nLoop\nan Python commandline", fontname = "verdana.ttf", fontsize= 12, max_width = 400 )
        
        self.info_test.bounds = Rectangle(Point(0,0), Point(200,200))
        self.info_test.set_position(Point(200, 300))
        world.add(self)
        self.add(self.info_test)
        tmp = world.stringinput_ID
        self.string_input = None
        for el in world.children:
            if id(el) == tmp:
                self.string_input = el
        self.string_input.set_position(Point(400, 400))
        self.string_input.is_visible = True
                                    
    def draw(self):
        super(Repl,self).draw()
        self.info_test.draw()

    def get_handles_mouse_click(self):
        """a click wil activate evaluation"""
        return True
    
    def mouse_down_left(self, pos):
        print("\n>>++ repl L39 got a mouse down")
        tmp = self.string_input.onelinetext.text
        print(">>++ seeing" ,tmp)
        if tmp.endswith("=?"):
            tmp = tmp[:-2]
            try:
                res = eval(tmp)
                print("***RESULT = ", res)
                
                self.info_test.text =   str(res) 
                print(self.info_test.text)
                self.info_test.parse()
                self.info_test.draw()
            except Exception as excep:
                print("***ERROR evaluation tmp", tmp, excep)
