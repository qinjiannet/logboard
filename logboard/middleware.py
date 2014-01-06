#-*- coding: UTF-8 -*-
from datetime import datetime
import sys,traceback
from logboard import listener_manager,msg_box
import json
exclusion_list = ['/logboard/reset/','/logboard/broadcast/']
class DebugMiddleware(object):
	def __init__(self):
		self.listeners = listener_manager.get_listeners()
	def process_response(self, request, response):
		msg = '[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']' + ' ' + "\"" + request.method + " " + request.path + " " + request.META['SERVER_PROTOCOL'] + " " + str(response.status_code) + " " + str(len(response.content))+"\""
		if request.path not in exclusion_list:
			self.broadcast(msg,'info')
		return response
	def process_exception(self, request, exception):
		msg = exception.__class__.__name__ + ": " + str(exception) + "\n" + '\n'.join(traceback.format_exc().splitlines())
		if request.path not in exclusion_list:
			self.broadcast(msg,'warning')
	def broadcast(self,msg,type):
		print msg,type
		#listener_manager.broadcast(json.dumps({'msg':msg,'type':type}),self.listeners)
		from sae.taskqueue import add_task
		rkey = msg_box.gen_key()
		msg_box.set_msg(rkey,json.dumps({'type':type,'msg':msg}))
		add_task('msg_queue', '/logboard/broadcast/', rkey)