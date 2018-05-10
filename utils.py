import datetime
from process import *
from states import *
from socket import *
import random 
import math


def time_to_millisec(when=None):
    ''' 
    take time return time in milliseconds
    without an argument: return local time in milliseconds
    '''
    
    if when == None:
        when = datetime.datetime.now()
    if type(when) == str:
        when = datetime.datetime.strptime(when, '%H:%M:%S.%f')
    
    return (when.hour*360000 + when.minute*60000 + when.second*1000 + when.microsecond//1000) 


def global_update(all_states, mess, queue=None):
    '''
    take a set of states instances, queue, and message object
    update all of state instances in the set
    '''
    time = time_to_millisec()
    
    if queue:
        m.new_values(queue, time)    
        
    for st in all_states:
        st.time = time
        st.update_st(mess)
        
            
def winner_changed(prev_winner_state, all_states):
    ''' 
    take previous winner object, and all states set,
    return True - if winner state is different from the previous one,
            False - if winner state is the same
    '''
    
    maxValue = (sorted(all_states))[-1].value
    new_leaders = [st.__class__.__name__ for st in all_states if st.value == maxValue]
    if prev_winner_state.value == maxValue or prev_winner_state.__class__.__name__ in new_leaders:
        return False
    else:
        return True
        
        
                
def the_winner(all_states):
    '''
    take all states
    return the winner state
    '''
    
    maxValue = (sorted(all_states))[-1].value
    new_leaders = [st for st in all_states if st.value == maxValue]
    
    winner_state = random.choice(new_leaders)
    return winner_state
    
  
    