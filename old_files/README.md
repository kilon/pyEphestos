# SUMMARY

Ephestos is an effort to offer an alternative to Python for Blender. The
alternative is Pharo.

http://pharo.org/

Pharo offers several things

1)  A language that is simple and more english like than python. Pharo is a
modern non backward compatible Smalltalk implementation. Everything is messages
to objects.

For example the typical hello world code in Pharo is :

Transcript show: 'Hello World

2) Live coding , meaning that you can code the application while it runs.

3) A powerful IDE implemented in Pharo itself. Tons of tools to make life easy.

4) A very powerful debugger, in case of an error the debugger alows you to
change the code and resume your application where the error happened as if the
error never happened.

5) A full blown GUI API , simple, powerful and flexible and entirely written in
Pharo. Far more sophisticated than what the Blender GUI API offers.

PyEphestos is the Blender Side of the Ephestos project , its a typical python
addon that exchanges communication with the Pharo side via sockets. It allows
Pharo to control Blender.

Pharo also can be used as a GUI alternative for Blender.
