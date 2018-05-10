import math
from process import *
import random
import datetime
from utils import bml


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
        
        if new_bml != prev_bml_winner:
            print(self.__class__.__name__ + str(self.value))
            with open (filename, 'a', encoding='utf-8') as io:
                #inp = io.read()
                #if inp == '':
                #    inp += 'time,state,bml/r/n'
                io.write(str(self.time) + ',' + datetime.datetime.now().strftime('%H:%M:%S.%f') + ',' + self.__class__.__name__ + ',' + self.return_bml() + '\r\n')
            return new_bml


#daughter classes of states
class think(state):
    
    def __init__(self):
        state.__init__(self)
        self.direct = 'aside'
        
    def update_st(self, m):
        
        x = self.time
        #y = math.log(x^2, math.e)
        y = 1000*math.cos(x/1000)+1000
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
            y = (x + self.const)/1000
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
        
