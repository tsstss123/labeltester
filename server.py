# -*- coding:utf-8 -*-
import logging
import zmq

zmq_ctx = zmq.Context()
s = zmq_ctx.socket(zmq.REP)
s.bind('tcp://0.0.0.0:6677')

def get_image(token):
    from PIL import Image
    img = Image.open('test.png')
    return img

def user_login(username):
    return True
def user_token(username):
    return username
def deal_msg(msg_recv):
    print('deal msg', msg_recv)
    if 'TYPE' not in msg_recv:
        logging.warning('message not have TYPE')
        return False
    type = msg_recv['TYPE']
    msg_send = dict(TYPE='NOPE')
    if type == 'LOGIN':
        username = msg_recv['USERNAME']
        if user_login(username):
            msg_send = dict(TYPE='LOGIN_SUCC', TOKEN=user_token(username))
        else:
            msg_send = dict(TYPE='LOGIN_FAIL')
    elif type == 'GET':
        token = msg_recv['TOKEN']
        msg_send['TYPE'] = 'PICSAMPLE'
        msg_send['PICDATA'] = get_image(token)
        msg_send['PICID'] = '0101010'
        msg_send['PICOPT'] = [(1, '植物'), (2, '动物')]
    elif type == 'PICRESULT':
        token = msg_recv['TOKEN']
        pid = msg_recv['PICID']
        print('pic id = ', pid, 'choose', msg_recv['OPT'][0])
        msg_send['TYPE'] = 'ACK'
    s.send_pyobj(msg_send)

if __name__ == '__main__':

    while True:
        msg = s.recv_pyobj()
        print('receive a msg')
        if not isinstance(msg, dict):
            print('msg not a dict')
            continue
        deal_msg(msg)

