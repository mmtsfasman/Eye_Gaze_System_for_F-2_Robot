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
            
            #question parameter to default when speech is completed and the previous phrase doesn't affect the robot anymore
            if self.end < time:
                self.question = False
                
            #process message about previous gaze("Gaze completed." message means that it was towards a person, "Turn completed" - aside)
            if message.endswith('Gaze completed.'):
                self.prev_gaze = 'person'                
            elif message.endswith('Turn completed.'):
                self.prev_gaze = 'aside'
            

            #if speech completed - all attributes connected to speech and its parameters -> to default
            elif message.endswith('Speech completed.'):
                self.end = time
                self.phrase = False                
                self.agree = False
                self.disagree = False
                self.citation = False
                self.reasononing = False
                self.illustr = False

                #if phrase was question - question parameter to True (cause robot will be expecting an answer after the phrase is completed)
                if re.search('\?', self.text):
                    self.question = True

            #if robot speaking - update speech parameters and statement characteristics depending on text and time limits  
            elif re.search('Stroke', message):

                #robot is speaking
                self.phrase = True
                
                text = re.findall('\"(.*)\"', message)[0].lower()
                self.text = text

                #speech start time
                start_time = re.findall('at (.+?\.[0-9]+)\.', message)[0]
                self.start = time_to_millisec(start_time)

                #speech stroke time
                stroke_time = re.findall('delay ([0-9]*)\.', message)[0]
                self.stroke = self.start + int(stroke_time)                

                #speech characteristics depending on text
                if re.search('\bда\b', text):
                    self.agree = True
                if re.search('(\bнет\b|\bне\b)', text):
                    self.disagree = True
                if re.search('(потому\b|потому что\b)', text):
                    self.reasoning = True
                if re.search('(\bнапример|\bк примеру\b)', text):
                    self.illustr = True




    
