from socket import *
from time import sleep
from threading import Event, Thread, Timer
from queue import Queue
import time
from states import *
from utils import *
from process import *

count = 0
interval = 0.04

def listen(host, port):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((host,port))
    s.listen(1)
    global q
    while True:
        c, addr = s.accept()
        size = c.recv(4)
        data = c.recv(int.from_bytes(size, byteorder='little'))
        c.close
        q.put(data.decode())
        print('Received')

def timer_call(f_stop, target):
    if not f_stop.is_set():
        Timer(target - time.clock(), timer_call, [f_stop, target+interval]).start()
        work()
        

def work():
    qu = []
    while not q.empty():
        qu.append(q.get())

    global mess
    global prev_bml_winner
    global prev_winner_state
        
    global_update(all_states, mess, qu)
        
    if winner_changed(prev_winner_state, all_states) == True:
        new_winner_state = the_winner(all_states)
        new_bml_winner = new_winner_state.execute_behavior('results.csv', prev_bml_winner)
        prev_bml_winner = new_bml_winner        
        prev_winner_state = new_winner_state


    
#initialize all_states
try:
    all_states
except NameError:
    #print("New states created")        
    thi = think()
    sp = speak()
    att = attention_to_person()
    rem = remember()
    quo = quote()
    ant = anti_social()
    agr = agree()
    all_states = [thi, sp, att, rem, quo, ant, agr]
    
try:
    mess
except NameError:
    mess = process()
    
try:
    prev_bml_winner
except NameError:
    prev_bml_winner = ''    

    
host = '127.0.0.1'
port = 6069
q = Queue()

try:
    thread = Thread(target=listen, args=(host, port))
    thread.daemon = True
    thread.start()
    f_stop = Event()
    target = time.clock() + interval
    
    try:
        prev_winner_state
    except NameError:
        prev_winner_state = state()
        
    timer_call(f_stop, target)
    while not f_stop.is_set():
        sleep(1)
except KeyboardInterrupt:
    print("Interrupted.")
    f_stop.set()
    visualize(all_states)

