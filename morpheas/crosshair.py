#from .morph import *
debug_print_cross = True
from .hand import *
class CrossHair(Morph):
    """ a slave to (a/THE) hand, but painting a Cross, dependent on is_visible"""
    def __init__(self, hand):
        super(Morph,self).__init__()
        self.bounds = Rectangle(Point(0,0),Point(0,0))
        self.color = (1.0, 0, 0, 1)
        self.hand = hand
        self.is_visible = True
        
    def draw(self):
        if self.is_visible:            
            mp_x = self.hand.mouse_x
            mp_y = self.hand.mouse_y
            top_x = mp_x 
            bot_y = mp_x - 10
            top_y = mp_y + 10
            left_x = mp_y - 10
            right_x = mp_y + 10
            if debug_print_cross:
                print("  a cross must be painted at", (mp_x, mp_y))
            self.draw_line(mp_x, top_y, mp_x, bot_y)
            self.draw_line(left_x, mp_x, right_x, mp_x)
        else:
            if debug_print_cross:
                print(" visibility of CrossHair is False")
                
    def set_visibility(self, value):
        self.is_visible = value
        
