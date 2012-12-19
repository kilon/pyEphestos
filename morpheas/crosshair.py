#from .morph import *
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
            self.draw_line(self.hand.mouse_x - 10, self.hand.mouse_y,\
                           self.hand.mouse_x + 10, self.hand.mouse_y)
            self.draw_line(self.hand.mouse_x, self.hand.mouse_y - 10,\
                           self.hand.mouse_x, self.hand.mouse_y + 10)
        else:
            if debug_print_cross:
                print(" visibility of CrossHair is False")
                
    def set_visibility(self, value):
        self.is_visible = value
        
