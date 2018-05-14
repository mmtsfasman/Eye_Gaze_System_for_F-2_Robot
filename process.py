import re
from utils import time_to_millisec, visualize
'''
try:
    ""Потому что да, например?" started at 16:06:43.487. Stroke delay 600."
    "Speech completed."
    "Gaze completed."
    "Turn completed."
    ""Потому что?" started at 16:06:43.487. Stroke delay 600."
    
'''

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

    def __init__(self, prev_gaze='', phrase=False, stroke=0, start=0, end=0, agree=False, disagree=False, question=False, citation=False, reasoning=False, illustr=False, text=''):
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
        self.text = text
        
    #convert socket input into values for stetes instances        
    def new_values(self, queue, time, all_states):

        for message in queue:
            if self.end < time:
                self.question = False
            
            if message.endswith('Speech completed.'):
                self.end = time
                self.phrase = False                
                self.agree = False
                self.disagree = False
                self.citation = False
                self.reasononing = False
                self.illustr = False
                if re.search('\?', self.text):
                    self.question = True
                
            elif message.endswith('Gaze completed.'):
                self.prev_gaze = 'person'
                
            elif message.endswith('Turn completed.'):
                self.prev_gaze = 'aside'
               
            if message.endswith('vis'):
                visualize(all_states)
                
            if re.search('Stroke', message):
                self.phrase = True
                
                text = re.findall('\"(.*)\"', message)[0].lower()
                
                start_time = re.findall('at (.+?\.[0-9]+)\.', message)[0]
                self.start = time_to_millisec(start_time)
                
                stroke_time = re.findall('delay ([0-9]*)\.', message)[0]
                self.stroke = self.start + int(stroke_time)                
                
                print(str(self.start) + ', stroke = ' + str(self.stroke))
                
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
                
                self.text = text


    