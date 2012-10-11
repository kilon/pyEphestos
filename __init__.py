#-------------------------------------------------
#    morphic.py
#
#    a tree-based GUI for Python
#    inspired by Squeak
#
#    written by Jens Moenig
#    jens@moenig.org
#
#    version 2009-Nov-06
#
#    Copyright (C) 2009 by Jens Moenig
#---------------------------------------
#-------------------------------------------------
#    morpheas.py
#
#    Morpheas is the GUI side of Ephestos based on morphic.py
#
#
#    written by Kilon Alios
#    thekilons@yahoo.co.uk
#
#    version April-2012
#
#    Copyright (C) 2012 by Kilon Alios
#---------------------------------------
#    Permission is hereby granted, free of charge, to any person
#    obtaining a copy of this software and associated documentation
#    files (the "Software"), to deal in the Software without
#    restriction, including without limitation the rights to use, copy,
#    modify, merge, publish, distribute, sublicense, and/or sell copies
#    of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be
#    included in all copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
#    yet to implement:
#    - make World customizable before opening it
#    - scroll bars
#    - tool tips
#    - skinnables
#    - turtle trails
#    - better string editing
#    - multi-line edits

""" here we go """



bl_info = {
    "name": "Ephestos : The Golden Age",
    "description": "Ephestos is a visual programming language , a GUI and inerface for supercollider",
    "author": "Kilon",
    "version": (0, 0, 1),
    "blender": (2, 6, 3),
    "location": "View3D > Left panel ",
    "warning": 'warn',  # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "https://github.com/kilon/Ephestos",
    "category": "Development"}

#select you default startup file!
PKHG_test = True
KILON_test = False
ZEFFIE_test = False #add your analog lines ;-)

if "bpy" in locals():
    import imp
    if "morpheas" in locals():
        imp.reload(morpheas)
    if "test_1_morpheas" in locals():
        if PKHG_test:
            imp.reload(test_PKHG_stringinput_100612)
        else:
            imp.reload(test_1_morpheas)
else:
    import Ephestos
    if PKHG_test:
        from Ephestos import  test_PKHG_stringinput_100612
    else:
        from Ephestos import  test_1_morpheas

import bpy

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
