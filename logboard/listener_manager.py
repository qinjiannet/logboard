#-*- coding: UTF-8 -*-
from sae import kvdb,channel
from datetime import datetime,timedelta
import random
import string
LOG_LISTENER = 'log_listener'
EXPIRE_MINUTES = 120 #listener expires after 120 minutes
MAX_RETRY = 20

def reset_listeners():
	kv = kvdb.KVClient()
	return kv.delete(LOG_LISTENER)

def get_listeners():
	kv = kvdb.KVClient()
	return kv.get(LOG_LISTENER)

def create_listener():
	listeners = get_listeners()
	for x in range(MAX_RETRY):
		listeners = get_listeners()
		name = ''.join(random.choice(string.letters + string.digits) for x in range(32))
		if listeners and listeners.get(name):
			continue
		return name
	raise Exception('Error on creating listener, Max retry exceeded!')

def add_listener(name,ctime = datetime.now()):
	listeners = get_listeners()
	if listeners is None:
		listeners = dict()
	listeners[name] = {'ctime':ctime}
	kv = kvdb.KVClient()
	kv.set(LOG_LISTENER,listeners)

def remove_listener(name,listeners = None):
	if listeners is None:
		listeners = get_listeners()
	if listeners and listeners.get(name):
		del listeners[name]
	kv = kvdb.KVClient()
	kv.set(LOG_LISTENER,listeners)

def is_expired(listener):
	return listener['ctime'] + timedelta(minutes = EXPIRE_MINUTES) < datetime.now()

def broadcast(msg,listeners = None):
	if listeners is None:
		listeners = get_listeners()
	if listeners is None:
		return
	removes = []
	for key in listeners:
		print key
		listener = listeners[key]
		if is_expired(listener):
			removes.append(key)
		else:
			send_msg(key,msg)
	for item in removes:
		remove_listener(item,listeners)
def send_msg(target,msg):
	print 'send_msg',target,msg
	channel.send_message(target, str(msg))