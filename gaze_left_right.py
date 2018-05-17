
# coding: utf-8

# In[ ]:




def gaze_leftright(prev_bml):
 time = time_to_millisec()
 
 bml_right = '<bml id=\"'+ str(time) + '\" syncmode=\"join\"><head id=\"2\" lexeme=\"eyes_down_right3\"/><pupils id=\"3\" lexeme=\"eyes_down_right3\"/></bml>'

 bml_left = '<bml id=\"'+ str(time) + '\" syncmode=\"join\"><head id=\"2\" lexeme=\"eyes_down_left3\"/><pupils id=\"3\" lexeme=\"eyes_down_left3\"/></bml>'

 if bml_changed(bml, bml_right):
     return bml_right
 
 elif bml_changed(prev_bml, bml_left):
     return bml_left
 
 


def work():
 
 global prev_bml    
 new_bml = gaze_leftright(prev_bml)    
 prev_bml = new_bml
 send(new_bml)

