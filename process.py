import re
from utils import time_to_millisec


class process:
    '''
    Object with current info from the message queue. If no queue given - creates an instance with default values.
    
    Types of messages:
    '"text" started at 16:06:43.487. Stroke delay 600.'
    'Speech completed.'
    'Gaze completed.'
    'Turn completed.'
  
    new_values() processes incoming queue and updates instance's attributes corrispondingly    
    '''

    def __init__(self, prev_gaze='', phrase=False, stroke=0, start=0, end=0, agree=False,
                 disagree=False, question=False, citation=False, reasoning=False, illustr=False):
        self.prev_gaze = prev_gaze
        self.phrase = phrase
        self.stroke = stroke #in ms
        self.start = start #in ms
        self.end = end #in ms
        self.agree = agree 
        self.disagree = disagree
        self.question = question
        self.citation = citation
        self.reasononing = reasoning
        self.illustr = illustr
        
    def new_values(self, queue, time):
        #convert socket input into values for stetes instances
        
        for message in queue:
            if message == 'Text completed.':
                self.end = time
                self.phrase = False
                
            elif message == 'Gaze completed.':
                self.prev_gaze = 'person'
                
            elif message == 'Turn completed.':
                self.prev_gaze = 'aside'
                
            elif message.startswith('\"'):
                self.phrase = True
                
                text = re.search('\"{.*?}\"', message).lower()
                
                start_time = re.search('at {.*?}\.', message)
                self.start = time_to_millisec(start_time)
                
                stroke_time = re.search('delay {[1-9]*?}\.', message)
                self.stroke = self.start + int(stroke_time)
                
                if re.search('\?', text):
                    self.question = True
                if re.search('\bда\b', text):
                    self.agree = True
                if re.search('(\bнет\b|\bне\b)', text):
                    self.disagree = True
                if re.search('(потому\b|потому\bчто\b)', text):
                    self.reasoning = True
                if re.search('(\например|\bк\bпримеру\b)', text):
                    self.illustr = True
                if re.search('\"', text):
                    self.disagree = True


    