from .menu import *

class Button(Trigger, RoundedBox):
    def __init__(self, target=None,
                 action= None, 
                 label=None,
                 fontname="verdana.ttf",
                 fontsize=10,
                 bold=False,
                 italic=False):
        super(Button, self).__init__()
