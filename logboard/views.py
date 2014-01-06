#-*- coding: UTF-8 -*-
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response,redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.http import Http404
import random
import re
import json
from sae import channel
from logboard import listener_manager,msg_box

def reset(request):
	return HttpResponse(listener_manager.reset_listeners(), mimetype="text/plain")
	
#@login_required
def index(request):
	#if request.user.is_staff:
	name = listener_manager.create_listener()
	duration = listener_manager.EXPIRE_MINUTES
	url = channel.create_channel(name, duration)
	listener_manager.add_listener(name)
	print 'create',name,url
	return render_to_response('logboard/index.html', {'url':url}, context_instance=RequestContext(request))

@csrf_exempt
def connected(request):
	res = request.POST
	print res
	return HttpResponse(json.dumps(res), mimetype="text/plain")

@csrf_exempt
def disconnected(request):
	res = request.POST
	name = res['from']
	listener_manager.remove_listener(name)
	print 'remove_listener',name
	return HttpResponse(json.dumps(res), mimetype="text/plain")

@csrf_exempt
def message(request):
	return HttpResponse('', mimetype="text/plain")

def test(request):
	print None + None

@csrf_exempt
def broadcast(request):
	rkey = request.POST.keys()[0]
	#json.dumps({'msg':msg,'type':type}
	listener_manager.broadcast(msg_box.get_msg(rkey))
	msg_box.del_msg(rkey)
	return HttpResponse('ok', mimetype="text/plain")