import datetime
from process import *
from states import *
from socket import *
from random import choice
import math


def time_to_millisec(when=datetime.datetime.now()):
    ''' 
    take time return time in milliseconds
    without an argument: return local time in milliseconds
    '''
    
    if type(when) == str:
        when = datetime.datetime.strptime(when, '%H:%M:%S.%f')
    
    return when.hour*360000 + when.minute*60000 + when.second*1000 + when.microsecond//1000 


def global_update(all_states, queue=None):
    '''
    take a set of states instances, update all of them
    '''
    
    mess = process()
    #if queue:
    #    m.new_values(queue)
    time = time_to_millisec()
    
    for st in all_states:
        st.time = time
        st.update_st(mess)
    
def winner_changed(prev_winner_state, all_states):
    ''' 
    take previous winner object, and all states set,
    return True - if winner state is different from the previous one,
            False - if winner state is the same
    '''
    
    maxValue = (sorted(all_states))[0].value
    new_leaders = [st.__class__.__name__ for st in all_states if st.value == maxValue]
    if prev_winner.value == maxValue or prev_winner.__class__.__name__ in new_leaders:
        return False
    else:
        return True
        
        
                
def the_winner(all_states):
    '''
    take all states
    return the winner state
    '''
    
    maxValue = (sorted(self.all_states))[0].value
    new_leaders = [st for st in all_states if st.value == maxValue]
    
    winner_state = random.choice(self.leaders)
    