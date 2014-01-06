#-*- coding: UTF-8 -*-
from sae import kvdb,channel
from datetime import datetime,timedelta
import random
import string
import os
LOG_MSGBOX = 'log_msg_box'
MAX_RETRY = 20

def gen_key():
	return os.urandom(32).encode('hex')

def reset_msgbox():
	kv = kvdb.KVClient()
	return kv.delete(LOG_MSGBOX)

def get_msgbox():
	kv = kvdb.KVClient()
	msgbox = kv.get(LOG_MSGBOX)
	if msgbox is None:
		msgbox = {}
	return msgbox

def set_msgbox(msgbox):
	kv = kvdb.KVClient()
	kv.set(LOG_MSGBOX,msgbox)

def get_msg(key):
	msgbox = get_msgbox()
	return msgbox.get(key)

def set_msg(key,msg):
	msgbox = get_msgbox()
	msgbox[key] = msg
	set_msgbox(msgbox)

def del_msg(key):
	msgbox = get_msgbox()
	if msgbox.get(key):
		del msgbox[key]
	set_msgbox(msgbox)