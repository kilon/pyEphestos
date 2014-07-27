#-*- coding: utf-8 -*-

#------------------------------------------
#   pyEphestos
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
#
#    Under GPL license for more info see the Blender license
#
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

""" Pharo code:
stream := SocketStream openConnectionToHostNamed: ' 127.0.0.1'  port: 4000 .
stream sendCommand: 'Hello Pharo AGAIN!!!!'.
stream close."""

bl_info = {
    "name": "Ephestos : communication tool for Pharo",
    "description": "Ephestos is a communication tool to allow Pharo to control Blender. This allows Pharo to control blender via Blender Python API. Pharo is a simple programming language , very powerful IDE and a fun live coding enviroment.",
    "author": "Kilon",
    "version": (0, 0, 1),
    "blender": (2, 7, 1),
    "location": "View3D > Left panel ",
    "warning": 'Warning !!! It may crash Blender ! Always save your work !',  # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "https://github.com/kilon/pyEphestos",
    "category": "Development"}


import time
import bpy
import threading
import socket
from bpy.props import *
from time import sleep

ephestos_running = False
thread_created = False
threadSocket = 0
socketServer = 0
receivedSocket = "none"
listening = False
socketMessages = []
receivedData = ''
pherror = [""]

def create_thread():

    global threadSocket,listening
    threadSocket = threading.Thread(name='threadSocket', target= socket_listen)
    listening = True
    create_socket_connection()
    threadSocket.start()
    #threadSocket.join()

def socket_listen():
    global receivedSocket,listening, receivedData,socketServer, socketMessages, pherror
    socketServer.listen(5)

    while listening:
        (receivedSocket , adreess) = socketServer.accept()
        receivedData = (receivedSocket.recv(1024)).decode("utf-8")[:-2]

        #exec(receivedData)
        socketMessages.append(receivedData)
        sleep(0.03)

        print("pherror : " ,pherror)


        while not (pherror[-1]==""):

            receivedSocket.sendall((pherror[-1]+'\n').encode())
            print("I have sent err : --->"+ pherror[-1] + ' <---- and removed it from the list of errors')
            if len(pherror) > 1:pherror.remove(pherror[-1])


            receivedSocket.sendall("end of error\n".encode())
        receivedSocket.close()




def create_socket_connection():
    global socketServer
    socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketServer.bind(('127.0.0.1',4000))


class open_ephestos(bpy.types.Operator):
    bl_idname = "ephestos_button.modal"
    bl_label = "enable Ephestos"
    _timer = None

    def modal(self, context, event):
        global ephestos_running, thread_created, listening, socketServer, socketMessages, pherror
        result =  {'PASS_THROUGH'}
        #context.area.tag_redraw()
        #context.area.header_text_set("Welcome to Ephestos")
        #if context.area:
           # context.area.tag_redraw()


        if context.area.type == 'VIEW_3D' and ephestos_running and event.type in {'ESC',}:

            ephestos_running = False
            listening = False
            #time.sleep(1)
            socketServer.close()
            context.window_manager.event_timer_remove(self._timer)
            #time.sleep(1)
            thread_created = False
            result = {'CANCELLED'}
            self.report({'WARNING'}, "Ephestos has been closed")

        if context.area.type == 'VIEW_3D' and ephestos_running and event.type == 'TIMER' :
          for msg in socketMessages:
              try:

                  exec(msg,globals())
                  #socketMessages.remove(msg)
                  pherror.append("no error\n")
              except Exception as e:
                  newerror = "Error:" +str(e)+" with :" + msg
                  pherror.append( newerror )
                  print( "inserted an error now pherror : ",pherror)
                  #self.report({'WARNING'}, pherror)
                  #socketMessages.remove(msg)
              socketMessages.remove(msg)
          # create_thread()
          # thread_created = True

        return result

    def invoke(self, context, event):
        global ephestos_running,thread_created
        if context.area.type == 'VIEW_3D' and ephestos_running == False :
            self.cursor_on_handle = 'None'

            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            #self._handle =bpy.types.SpaceView3D.draw_handler_add(draw_ephestos,(self,context), 'WINDOW', 'POST_PIXEL')

            self._timer = context.window_manager.event_timer_add(0.01,context.window)
            ephestos_running = True
            context.window_manager.modal_handler_add(self)
            create_thread()
            thread_created = True
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Ephestos is already opened and running")
            return {'CANCELLED'}


class ephestos_panel(bpy.types.Panel):
    bl_label = "Ephestos"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    def draw(self, context):
        global receivedSocket,listening,pherror

        sce = context.scene
        layout = self.layout
        box = layout.box()
        box.label(text="Ephestos WIP not finished yet")
        box.label(text="-----------------------------")

        if listening:
            box.label(text="Listening")
        else:
            box.label(text="Not Listening")

        box.label(text="ReceivedData:")
        box.label(text=receivedData)
        if len(pherror) == 0:
            box.label(text="Error: no error ")
        else:
            box.label(text=pherror[-1])
        box.operator("ephestos_button.modal")


def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
