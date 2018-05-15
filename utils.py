import datetime
from process import *
from states import *
from socket import *
import random 
import math
import matplotlib.pyplot as plt

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
        #print(queue)
        mess.new_values(queue, time, all_states)    
        
    for st in all_states:
        #print(st.__class__.__name__ + ' | ' + str(st.value))
        st.time = time
        st.update_st(mess)
        
        
def visualize(all_states):
    '''
    visualizes states' curves on a plot (x - time, y - activation of the state)
    '''
    
    plt.xlabel('time (ms)')
    plt.ylabel('activation')
      
    for st in all_states:
        name = st.__class__.__name__
        if st.points:
            xs = [p[0] for p in st.points]
            ys = [p[1] for p in st.points]            
            plt.plot(xs, ys, label=name)
    
    plt.legend()
    plt.show()

        
            
def winner_changed(prev_winner_state, all_states):
    ''' 
    take previous winner object, and all states set,
    return True - if winner state is different from the previous one,
            False - if winner state is the same
    '''
    
    maxValue = (sorted([v.value for v in all_states]))[-1]
    new_leaders = [st.__class__.__name__ for st in all_states if st.value >= maxValue]
    if prev_winner_state.__class__.__name__ in new_leaders:
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


def bml_changed(prev_bml_winner, new_bml):
    '''
    take new bml and the preveious one, compare them
    if changed - True, if the same one - False
    '''
    
    pers = re.compile('(?:person1)|$')
    aside = re.compile('(?:lexeme.\".+?\")|$')
    if re.search(pers, new_bml).group() != '' and re.search(pers, prev_bml_winner).group() != '':
        return False
    elif re.search(aside, new_bml).group() != re.search(aside, prev_bml_winner).group():
        return True


def bml(index, direction=''):
    ''' 
    input:
    -id of output bml
    -side of the gaze (left, right, up, down, person) = True
    output:
    bml str with full bml for gaze to the corresponding side
    (return randomized from corresponding packages)

    example:

    >>>bml(23, direction='left')
    output: '<bml id="23" syncmode="single"><head id="2" lexeme="eyes_down_left3"/>
        <pupils id="3" lexeme="eyes_down_left3"/></bml>'
    '''
    
    
    left_bmls = ['eyes_down_left3', 'eyes_up_left3']
    right_bmls = ['eyes_down_right3', 'eyes_up_right3']
    down_bmls = ['avtoman2']
    up_bmls = ['think9', 'think8']
    closed_bmls = ['CLOSED']

    if direction == 'person':
        out_bml = '<gaze id=\"2\" target=\"person1' 

    else:
        if  direction == 'aside':
            out_bmls = left_bmls + right_bmls + down_bmls + up_bmls
            

        elif direction == 'left':
            out_bmls = left_bmls

        elif direction == 'right':
            out_bmls = right_bmls

        elif direction == 'down':
            out_bmls = up_bmls

        elif direction == 'up':
            out_bmls = down_bmls
            
        elif direction == 'closed':
            out_bmls = closed_bmls

        s = random.choice(out_bmls)    
        out_bml = '<head id=\"2\" lexeme=\"' + s + '\"/><pupils id=\"3\" lexeme=\"' + s

    start = '<bml id=\"'+ str(index) + '\" syncmode=\"join\">'
    end = '\"/></bml>'
    return start + out_bml + end
  
    
