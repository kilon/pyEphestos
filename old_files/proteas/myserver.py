
import bpy 
from xmlrpc.server import * 

class myserver:
    running = True
    
class main_handler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2', )
    
server = SimpleXMLRPCServer(("localhost", 8999), 
requestHandler=main_handler, allow_none = True) 
print("registering") 

def call_bpy(cmd): 
    exec(cmd) 
    
server.register_function(call_bpy) 

def stop_server(): 
    myserver.running = False
    print("server stoped")
    
server.register_function(stop_server)

def start_server(): 
    myserver.running = True
    print("server start") 
    
server.register_function(start_server)
 
server.register_instance(bpy) 
print("registering complete, serving") 
# server.serve_forever() 

while myserver.running :
    server.handle_request()

del(server)