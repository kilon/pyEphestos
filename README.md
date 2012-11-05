# SUMMARY

Ephestos is going to be a visual programming language and environment that will import and export python code and be fully compliant with python. It will be an environment to make programming more visual and easier for the user, especially the creation of Blender addons. 


There are going to be 3 tools:

1) Morpheas - A port of Morphic Gui for python. Morphic is the standard GUI for Squeak, Pharo and Self programming languages and is unique in the sense that besides user interaction it allows the user to even modify it while a programm is running make it possible to create ease custom modifications. Also any piece of code can have a visual representation called morph, thus making it suitable for visual programming.
 
2) Proteas - Visual Programming Environement leveraging Morpheas and Real Time Context Sensitive Documentation. Proteas' goal is to be fully complaint with python allowing any python program to be a proteas programm and vice versa. Any piece of code will display documentation so the user never feels lost. 

3) Orpheas - DAW front end for Supercollider music and audio synthesis server via OSC messages.

Currently only Morpheas is implemented, based on pymorphic by Jens Monig. The goal for the time being is to offer blender developers a second GUI that will run on top of bgl and be more flexible, more powerful and more customisable than the standard Blender GUI. This flexibility will make it possible to design any kind of graphical element that will allow or not allow user interaction. 

It is my intention to also create a standalone version that will not be dependant on or related to blender, this version  will focus on general python developement.
