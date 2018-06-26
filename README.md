# Eye Gaze System for F-2 Robot
The project is completed in the frame of my Bachelor's Thesis, its full text can be found [**here**](Full_description(Thesis_text).pdf) 
The project is supervised by Artemy Kotov and supported by Kerchatov Institute lab developing F-2 Emotional Robot.

## Eye gaze system

[**core.py**](core.py):
Core of the system - receive messages from server, update all the states, calculate the winning state, send a string with corresponding bml back to the robot.   

[**process.py**](process.py):
Functions rocessing messages and generating corresponding values in the right format to be received by states.

[**states.py**](states.py):
Classes of states - parent class state and daughter classes with particular states (think, speak, attention_to_person, etc.)

[**utils.py**](utils.py):
Secondary functions.

[**random_gaze.py**](random_gaze.py):
A script moderating random eye gaze as a control experimental condition.




### Modelling eye gaze in the robot (*extracted from Thesis*)

After determining a set of oculomotor movements and their distribution, and verifying their significance for humans, my aim was to design them in the robot. The technologies I used to model robot&#39;s eye gaze behavior included Python, Behavior Markup Language (BML), and an external face tracker Kinect Xbox 360, recognising user&#39;s eyes and face location.

#### 1. Theoretical foundation: assumptions

As a result of corpus data processing, I made certain assumptions my programis based on. My hypothesis was that there are certain states evolving in human brain when communicating. Activation of those states depends on internal and external stimuli. Every state has its way of activation change.

This assumption is partially based on K. Lonrenz&#39;s hydraulic behavioral model (Lorenz 1963). Although his theory is primarily about instinctive animals&#39; behavior, it perfectly suits humans at the same time. In Lorenz&#39;s words, behavior resembles hydraulic system shown in Figure 5.

Figure 5. _K. Lorenz&#39;s hydraulic model (Lorenz, 1963)_


Internal motivation produce water from the tap, which fills up a reservoir.  The water from reservoir pushes a spring out in a certain extent. At the same time there are external stimuli symbolically represented by weights on a scale, which pull the spring as well. The spring releases water to a tray with holes - the more water is released at the same time, the more &#39;spouts&#39; it fills. The number of spouts represents the strength ofreaction expressed. It can be illustrated by a goose hunger: the growing hunger is an internal factor filling up a reservoir. When a goose notices a piece of bread it adds another external factor on the scale. When spring is pushed away, the water will be released and the goose will eat the bread in an extent of passion depending on how hungry it was or how attractive the bread is.

Similarly, in my program, different external and internal factors push the spring out and release the water from reservoir increasing state&#39;s activation. At each period of time states compete in their level of activation. The winner state sends a certain eye gaze to the robot&#39;s interface. The more &#39;water flows out&#39; the higher is the probability of a state to send its gaze to the machine.

The states competing in my system are based on the functions described above, in Section 3.2.2. Everystate has its own mathematical function which changes its activation value when receiving certain messages from the robot&#39;s system. Those messages, representing those internal and external factors, affect states according to the algorithms assigned.

#### 2. Program structure

My model is built in Python and is currently availible in this github repository.

The program itself is started through core.py script and works by an algorithm symbolically represented on the chart 6 below.

Figure 6. _Program functioning algorithm (simplified)_

 
The program listens to certain messages received from the robot&#39;s system through a network socket connection. My script processes those messages and changes state&#39;s activation correspondingly, if no messages are received my program still updates the states, but without any new changes in states&#39; mathematical functions. The state with the greatest activation &#39;wins&#39; and if it is not the same state as the previous winner and it is not the same eye gaze direction, it sends a bml package with its gaze to the robot. It all happens in 40 milliseconds loop similar to 25 frames per second in cinema or cartoon animation.

Bml packages are what robot&#39;s behavior is built on, they are strings with a certain syntax, and are structured as in the following example of eye gaze in up-left direction:

&lt;bml id=&quot;22&quot; syncmode=&quot;single&quot;&gt;
                &lt;head id=&quot;2&quot; lexeme=&quot;eyes\_up\_left3&quot;/&gt;
                &lt;pupils id=&quot;3&quot; lexeme=&quot;eyes\_up\_left3&quot;/&gt;
        &lt;/bml&gt;.

Script utils.py stores secondary functions used in the core and states scripts.

  **2.1 Message receiving and processing**

So far the incoming messages from the robot&#39;s system include the following:

- ➔&#39;Turn completed.&#39; - when robot has completed bml package to look aside.
- ➔&#39;Gaze completed.&#39; - when robot has completed bml package to look towards a person (creating eye contact)
- ➔&#39;&quot;_text_&quot; started at _time_. Stroke delay _time_.&#39; - when a bml package with speech has started playing on the robot. _Text_ is a string with robot&#39;s speech, start _time_ is the time robot starts pronouncing the speech,  delay _time_ is the time period after which phrasal stress is expected in milliseconds.
- ➔&#39;Speech completed.&#39; - when speech bml package is finished.

Messages are processed into a set of stimuli in the right format for the states to use through process class stored in proccess.py script in the repository.



**2.2 States classes hierarchy**

States based on the function system described in Section 3.2.2 are realised as a system of Python classes1. The parent class is called stateand includes all the functions and attributes all states have. Individual states are state&#39;s daughter classes. Eye gaze function classification from 3.2.2 Section is slightly reorganized so that it could be implemented most effectively. Function - implementation correspondence is shown in Table 6. Some of the functions are not implemented due to the limits of robot&#39;s recognition, and speech processing abilities. They can be implemented later, when certain information about the interlocutor position and behavior, speech characteristics, robot emotions is automatically extracted.

The functions implemented, partially implemented and not yet implemented are shown in Table 6:

Table 6. _Eye gaze function&#39;s implementation_

| **Function** | **Implemented?** | **How implemented? (Or why not implemented?)** | **What class?** | **Subtypes inside that class** |
| --- | --- | --- | --- | --- |
| thinking | yes, fully |  Independent from any internal/external factors or incoming messages function. Created so due to the fact that no human processes can be represented as a constant line - it usually can be approximated to a pulsing curve. | **thinking** | _no extra factors_ |
| speaking | yes,fully |  Where _a, b, c_ are predicted every time a speech startpoint and phrasal stress point are determined. Parabola, with the peak in the phrasal stress, and abscissa intersection points in the starting and ending point of robot&#39;s phrase. | **speaking** | ✔phrasal stress: determines the peak of the parabola |
| attention to person&#39;s reaction | yes,fully |  Where _a_ is time in a moment when robot looked towards the user, so that it grows from zero every time robot looked user in the eye. | **attention_to_person** | ✔question: after robot asks a question the activation jumps on x |
| softening anti-social situation | partially | Still requires automatic speech processing. | **antisocial** | ✔disagreeing✘ too long eye contact✘ softening &#39;strong&#39; words |
| remembering | partially | Still requires automatic speech processing do that factors are determined. | **remembering** | ✔argumentation✘ remembering a word/a situation✘ mental arithmetic✘ thinking on the answer |
| agreeing  | partially | Requires eyelids in robot&#39;s interface (to close eyes). However, if the bml package with closed eyes is added - my class would function. It will be function. | **agreeing** | _no extra factors_ |
| joking | _no_ | Requires automatic joke recognition. | |  _no extra factors_ |
| listening | _no_ | Requires automatic sound source recognition (to determine who is speaking). | | _no extra factors_ |
| mimicking interlocutor&#39;s eye gaze | _no_ | Requires eye gaze direction recognition (where is interlocutor looking?). | | _no extra factors_ |
| eye gaze patterns (iconic eye gaze) | _no_ | Requires special speech processing and determination of triggering words.| | ✘quote class ✘ verbs of movement &amp; thinking✘ words of looking✘ eye gaze metaphors✘ imaginary object usually mapped with hands✘ emotions &amp; words of emotions |

#### 3. Examples of system functioning on the robot

When the system is interrupted, it plots the activation functions for every state that has been activated during the system functioning period.

The first example, Figure 7, shows how the system is functioning by itself, without any extra robot&#39;s actions.  In other words, if the system is on and robot is in the state of inaction, robot&#39;s eye gaze behavior changes by the functions shown on the picture. Think state is a cosine function (blue curve)  independent from any stimuli. Attention to person is a linear function (orange lines) function that changes when the eye contact is achieved: it falls to zero and begins its new linear function from that point. The points where a new state beats all the other ones are the points of that state&#39;s victory - the points of sending eye gaze bml package to the robot.

Figure 7. _Example of states activation in robot&#39;s inaction_

As opposed to the state of inaction (Figure 7 above), the second example (Figure 8 below) represents robot&#39;s eye gaze behavior when speaking.

Figure 8. _Example of states activation when robot is speaking_

Attention to person state&#39;s sudden jump in the end of the phrase indicates that the phrase was a question and the robot came back to eye contact in order to listen to the answer or to check out interlocutor&#39;s reaction triggered by that question. Parabolas (orange curves) evolve when robot is speaking.

Figure 9. _Example from figure 8 with phrase limiting points illustration_

 Figure 9 illustrates that phrases starting and ending points can be spotted by the points parabolas intersect horizontal axis (see start point and end point in Figure 9). Parabola&#39;s peaks, on the other hand, are phrasal stress moments (see phrasal stress point in Figure 9).

**3 Generalizations**

The suggested model is constructed on three principles. First, it appeals to the observations of human eye gaze behavior based on the Russian Emotional Corpus. Second, on the hypothesis that internal states compete between each other, and the winner state gets expressed. Third, on K. Lorenz&#39;s hydraulic model. In order to verify whether this model reached the aim to increase robot&#39;s likeability and believability, we tested it in human-robot interaction experiment (Section 6).
