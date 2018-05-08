import math
from process import *


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
    down_bmls = ['DOWN']
    up_bmls = ['UP']
    closed_bmls = ['CLOSED']

    if direction == 'person':
        out_bml = ['target=\"person1\"/>'] 

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

        s = choice(out_bmls)    
        out_bml = 'lexeme=\"' + s + '\"/><pupils id=\"3\" lexeme=\"' + s

    start = '<bml id=\"'+ str(index) + '\" syncmode=\"single\"><head id=\"2\" '
    end = '\"/></bml>'
    return start + out_bml + end



#parent class of state
class state:
    
    def __init__(self, points=None):
        self.direct = ''
        self.points = points or []
        self.time = 0     
        self.value = 0
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __ne__(self, other):
        return self.value != other.value
    
    def __gt__(self, other):
        return self.value > other.value  
        
    def update_st(self, m):
        
        x = self.time
        y = 0
        self.value = y
        self.points.append((x, y))
        
        
    def return_bml(self):        
        return bml(self.time, direction=self.direct)
    
    def execute_behavior(self, filename, prev_bml_winner):
        
        new_bml = self.return_bml()
        if new_bml != self.prev_bml_winner:
            with open (filename, 'w', encoding='utf-8') as io:
                inp = io.read()
                if inp == '':
                    inp += 'time,state,bml/r/n'
                io.write(inp + self.time + ',' + self.__class__.__name__ + ',' + self.return_bml() + '/r/n')
            return new_bml


#daughter classes of states
class think(state):
    
    def __init__(self):
        state.__init__(self)
        self.direct = 'aside'
        
    def update_st(self, m):
        
        x = self.time
        y = math.log(x^2, math.e)
        self.value = y
        self.points.append((x, y)) 
    
    
class attention_to_person(state):
    
    def __init__(self):
        state.__init__(self)
        self.direct = 'person'
        self.const = None
        
    def update_st(self, m):
        
        x = self.time
        if m.prev_gaze == 'person' or self.const == None:
            self.const = x
        if self.const:
            y = (x + self.const)/5
            self.value = y
            self.points.append((x, y))

        
class speak(state):
    
    def __init__(self):
        state.__init__(self)
        self.direct = 'person'
        
    def update_st(self, m):
        
        if m.phrase == True:
            x = self.time
            y = -(x - m.stroke)^2 + 100
            self.value = y
            self.points.append((x, y))
                        
            #0 = a*((start - stroke)^2) + b*start + 200
            #0 = a*((end - stroke)^2) + b*end + 200        
        
        
class agree(state):
    
    def __init__(self):
        state.__init__(self)
        self.direct = 'closed'
        
    def update_st(self, m):
        
        if m.agree == True:
            x = self.time
            y = x^2
            self.value = y
            self.points.append((x, y))
            
            
class anti_social(state):
    
    def __init__(self):
        state.__init__(self)
        self.direct = 'aside'
        
        
class quote(state):
    
    def update_st(self, m):
        
        if m.citation == True:            
            if m.prev_gaze == 'aside':
                self.direct = 'person'
            else:
                self.direct = 'aside'
                
            x = self.time
            y = x^2
            self.value = y
            self.points.append((x, y))
    
    
class remember(state):
    
    def __init__(self):
        state.__init__(self)
        self.direct = 'aside'
        
    def update_st(self, m):
        
        if m.reasononing == True or m.illustr == True:
            x = self.time
            y = x^2
            self.value = y
            self.points.append((x, y))
        
