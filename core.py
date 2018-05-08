import asyncio
import time
import queue
from states import *
from utils import *
from process import *


async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    
    print("Received %r from %r" % (message, addr))
    global q
    q.put(message)


    
async def timer_work(loop):
    
    global q
    while True:
        
        try:
            all_states
        except NameError:
            #all_states = []
            thi = think()
            sp = speak()
            att = attention_to_person
            rem = remember()
            quo = quote()
            ant = anti_social()
            agr = agree()
            all_states = [thi, sp, att, rem, quo, ant, agr]
        
        try:
            prev_bml_winner
        except NameError:
            prev_bml_winner = ''
            
        try:
            prev_winner_state
        except NameError:
            prev_winner_state = state()
        
        if q.empty():
            global_update(all_states)           
        else:
            global_update(all_states, q.get)
            
            
        if winner_changed(prev_winner_state, all_states) == True:
            new_state_winner = the_winner(all_states, prev_winner_state) 
            new_bml_winner = new_state_winner.execute_behavior('results.txt', prev_bml_winner)
            prev_bml_winner = new_bml_winner
            prev_winner_state = new_winner_state
            #send(global_update(q.get)) 
            #print(q.get())
        await asyncio.sleep(0.04, loop=loop)
    return True

q = queue.Queue()
loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 6060, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    timer_task = asyncio.ensure_future(timer_work(loop))
    loop.run_until_complete(asyncio.wait([timer_task]))
except KeyboardInterrupt:
    timer_task.cancel()

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
print("Server closed")
loop.close()