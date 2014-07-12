# for client
import xmlrpc.client
s = xmlrpc.client.ServerProxy('http://localhost:8999')
s.call_bpy("bpy.data.objects[0].name=\"Jim\"")
s.stop_server()
