#PKHG trying to build a Read Eval Print Loop REPL ;-)
#import code  #PKHG does not work as expected ...
#from code import InteractiveConsole #Interpreter
#import inspect #for test
from .morph import *
from .rectangle import *
from .text import *
from . import repl_loc


class Repl(Morph):
    """a morph to Read Eval Print Loop python lines """

    def __init__(self, world = None, name = "REPL"):
        super(Repl, self).__init__(with_name = True)
        self.world = world
        self.set_position(Point(200,200))
        self.name = name
        self.info_test = Text("I will try to\nRead\nEval\nPrint\nLoop\nan Python commandline", fontname = "verdana.ttf", fontsize= 12, max_width = 400 )
        self.info_test.bounds = Rectangle(Point(0,0), Point(200,200))
        self.info_test.set_position(Point(200, 330))
        world.add(self)
        self.add(self.info_test)
        tmp = world.stringinput_ID
        self.string_input = None
        for el in world.children:
            if id(el) == tmp:
                self.string_input = el
        self.string_input.set_position(Point(200, 225 + self.bounds.get_height()))
        self.string_input.is_visible = True
 #does not work for me yet?! no evaluation of eg sin(1)       self.II = InteractiveConsole()

    def draw(self):
        super(Repl,self).draw()
        self.info_test.draw()

    def get_handles_mouse_click(self):
        """a click wil activate evaluation"""
        return True

    def mouse_down_left(self, pos):
        tmp = self.string_input.text
        if True: #tmp.endswith("?"):
            #because of True tmp = tmp[:-1]
            res = ""
            try:
#                res = eval("Ephestos.tmp.repl_loc." + tmp)
                #'''
                tmp2 = tmp.split(" = ")
                print("tmp2 = ", tmp2)
                if len(tmp2) == 1:
                    res = eval(tmp)
                else:
                    res = tmp2[0] # "Ephestos.tmp.repl_loc." + tmp2[0]
                    print("res vor exec=", res)
                    exec(tmp,globals())
                    tmp3 = eval(tmp2[-1])
                    print("tmp3 = ", tmp3)
                    res += " = " + str(eval(tmp2[-1]))
                #'''
                if not res:
                    res = "test PKHG L49 in repl.py"
                print("***REPL RESULT = ", res)
                tmp2 = self.info_test.text
                #PKHG remove first line (no scrolling yet)
                firstnl = tmp2.index("\n") + 1
                tmp2 = tmp2[firstnl:] + "\n"
#                print("\n\ntest",type(tmp2),tmp2)
#                self.info_test.text += "\n" + str(res)
                self.info_test.text = tmp2 + str(res)
                self.info_test.parse()
                self.info_test.draw()
            except Exception as excep:
                print("***ERROR evaluation tmp", tmp, excep)
        else:
            print(">>REPL++ seeing," ,tmp, "\nto eval, assignment = must be surrounde by at least onespace ;-)")

        def mouse_down_right(self,pos):
            print("\n\n mouse_down_right of repl called")
            self.is_visible = False
