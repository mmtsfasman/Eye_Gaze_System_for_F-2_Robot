import math
from process import *
import random
import datetime
from utils import bml, bml_changed
import numpy as np
from scipy.optimize import fsolve

#parent class of state
class state:
    
    def __init__(self):
        self.direct = ''
        self.points = []
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
    
    def execute_behavior(self, filename, new_bml):
        with open (filename, 'a', encoding='utf-8') as io:
             io.write(str(self.time) + ',' + datetime.datetime.now().strftime('%H:%M:%S.%f') + ',' + self.__class__.__name__ + ',' + self.return_bml() + '\r\n')



#daughter classes of states
class think(state):
    
    def __init__(self):
        state.__init__(self)
        self.direct = 'aside'
        
    def update_st(self, m):
        x = self.time
        #y = math.log(x^2, math.e)
        y = 1000*math.cos(x/5000)+1000
               
        if y < 0:
            y = 0
        self.value = y 
        self.points.append((x, y))
            
    

class attention_to_person(state):
    
    def __init__(self):
        state.__init__(self)
        self.direct = 'person'
        self.const = None
        
    def update_st(self, m):
        #print('константа аттеншн: ' + str(self.const))
        x = self.time
        if m.prev_gaze == 'person' or self.const == None or self.value >= 2500:
            self.const = x
        if m.question == True:
            y = 2500
        else:
            y = (x - self.const)/7
        if y < 0:
            y = 0
        self.value = y 
        self.points.append((x, y))

        
class speak(state):
    
    def __init__(self):
        state.__init__(self)
        self.direct = 'person'
        self.abc = [] 
        

    def update_st(self, m):
        
        if m.phrase == True:
            x = self.time            
                        
            const = 2500
            
            #to compute the parabola equation with start at the phrase start point, and peak at the stroke point
            def equations(p):
                    a, b, c = p
                    return (2*a*m.stroke+b, a*(m.stroke**2)+b*m.stroke-const+c, a*(m.start**2)+b*m.start+c)
                
            if self.abc == [] or m.start < self.time:          
                a,b,c =  fsolve(equations, (1, 1, 1))
                self.abc = [a, b, c]
            
            y = self.abc[0]*(x**2) + self.abc[1]*x + self.abc[2]
            #print(str(self.abc[0])+'*(x**2) + ' +str(self.abc[1]) + '*x + ' + str(self.abc[2]))
            
            if y < 0:
                y = 0
                
            self.value = y 
            self.points.append((x, y))

        
class agree(state):
    
    def __init__(self):
        state.__init__(self)
        self.direct = 'closed'
        
    def update_st(self, m):
        
        if m.agree == True:
            x = self.time
            y = x^2
            if y < 0:
                y = 0
            self.value = y 
            self.points.append((x, y))
            
            
class anti_social(state):
    
    def __init__(self):
        state.__init__(self)
        self.direct = 'aside'
        
    def update_st(self, m):
        if m.disagree == True:
            x = self.time
            y = x
            if y < 0:
                y = 0
            self.value = y 
            self.points.append((x, y))
    
        
        
class quote(state):
    
    def update_st(self, m):
        
        if m.citation == True:            
            if m.prev_gaze == 'aside':
                self.direct = 'person'
            else:
                self.direct = 'aside'
                
            x = self.time
            y = x^2
            if y < 0:
                y = 0
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
            if y < 0:
                y = 0
            self.value = y 
            self.points.append((x, y))
        
