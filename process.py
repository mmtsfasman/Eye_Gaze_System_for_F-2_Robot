'''
"text" started at 16:06:43.487. Stroke delay 600.
Text complete.
Gaze complete.
Turn completed.
'''


class process:
    def __init__(self, prev_gaze='', phrase=False, stroke=0, start=0, end=0, agree=False, disagree=False, question=False, citation=False, reasoning=False, illustr=False):
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
        
        
    '''def new_values(self, queue):
        #convert socket input into values to process
        
        for message in queue:
            if message.starts_with 
        text = .lower
        
        self.prev_gaze = 
        self.phrase = 
        self.stroke = 
        self.start =
        self.end = 
        self.last_played = 
        
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
        if re.search('\"', text.lower):
            self.disagree = True '''


    