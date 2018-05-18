from socket import *
from time import sleep
from threading import Event, Thread, Timer
import time
from states import *
from utils import *
from process import *


count = 0
interval = 8

def random_gaze(prev_bml):
    
    side = ['person', 'aside', 'aside', 'aside', 'aside']
    si = random.choice(side)
    gaze = bml(time_to_millisec(), si)
    if bml_changed(prev_bml, gaze):
        return gaze
    else:
        return None




def gaze_leftright(prev_bml):
    time = time_to_millisec()
     
    bml_right = '<bml id=\"'+ str(time) + '\" syncmode=\"join\"><head id=\"2\" lexeme=\"eyes_down_right3\"/><pupils id=\"3\" lexeme=\"eyes_down_right3\"/></bml>'

    bml_left = '<bml id=\"'+ str(time) + '\" syncmode=\"join\"><head id=\"2\" lexeme=\"eyes_down_left3\"/><pupils id=\"3\" lexeme=\"eyes_down_left3\"/></bml>'

    if bml_changed(prev_bml, bml_right):
        return bml_right
     
    elif bml_changed(prev_bml, bml_left):
        return bml_left
 
 



def timer_call(f_stop, target):
    if not f_stop.is_set():
        Timer(target - time.clock(), timer_call, [f_stop, target+interval]).start()
        work()
        



def work():
 
    global prev_bml    
    new_bml = gaze_leftright(prev_bml)    
    prev_bml = new_bml
    send(new_bml)

def send(bml): 
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('127.0.0.1', 6061))
    bytebml = bml.encode('utf-8')
    sock.send(len(bytebml).to_bytes(4,byteorder='little')+bytebml)
    sock.close()

    
    
host = '127.0.0.1'
port = 6060

try:
    
    f_stop = Event()
    target = time.clock() + interval
    
    try:
        prev_bml
    except NameError:
        prev_bml = ''
        
    timer_call(f_stop, target)
    while not f_stop.is_set():
        sleep(1)
except KeyboardInterrupt:
    print("Interrupted.")
    f_stop.set()


