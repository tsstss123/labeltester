# -*- coding:utf-8 -*-
import logging
import zmq

import random
import PIL

IP = '112.74.87.27'
PORT = 6677
zmq_ctx = zmq.Context()
s = zmq_ctx.socket(zmq.REQ)
s.connect('tcp://{0}:{1}'.format(IP, PORT))

print('please input your username')
name = input()
login_msg = dict(TYPE='LOGIN', USERNAME=name)

s.send_pyobj(login_msg)
msg = s.recv_pyobj()

print(msg)

if msg['TYPE'] != 'LOGIN_SUCC':
    print('Login Failure')
    exit()

token = msg['TOKEN']

while True:
    msg = dict(TYPE='GET',TOKEN=token)
    s.send_pyobj(msg)

    msg = s.recv_pyobj()
    msg['PICDATA'].show()
    for id in range(len(msg['PICOPT'])):
        print(str(id + 1) + ')', msg['PICOPT'][id][1])
    ipt = input()
    try:
        chid = int(ipt) - 1
    except:
        print('input error')
        chid = -1
    if chid < 0:
        print('choose error')
    else:
        opt = [msg['PICOPT'][chid][0]]

    msg = dict(TYPE='PICRESULT', TOKEN=token, PICID=msg['PICID'], OPT=opt)

    s.send_pyobj(msg)
    msg = s.recv_pyobj()

    print(msg['TYPE'])