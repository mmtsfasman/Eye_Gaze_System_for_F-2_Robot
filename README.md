# Eye Gaze System for F-2 Robot

## Eye gaze system

[**core.py**](core.py):
Core of the system - receive messages from server, update all the states, calculate the winning state, send a string with corresponding bml back to the robot.   

[**process.py**](process.py):
Functions rocessing messages and generating corresponding values in the right format to be received by states.

[**states.py**](states.py):
Classes of states - parent class state and daughter classes with particular states (think, speak, attention_to_person, etc.)

[**utils.py**](utils.py):
Secondary functions.

## Сообщения между роботом и глазодвигательной моделью

### От модели к роботу
* Подготовленным и валидный bml пакет в в формате строке.
    
    Например: 
    ```"<bml id="22" syncmode="single"><head id="2" lexeme="eyes_up_left3"/><pupils id="3" lexeme="eyes_up_left3"/></bml>"```

### От робота к модели 
* Сообщение о начале высказывания

    ```"text" started at 16:06:43.487. Stroke delay 600.```
  

    *Время указывается в формате %H:%M:%S.%f. Параметр %f выдаёт микросекунды, поэтому строка с временем обрезается на 3 символа слева для пролучения миллисекунд. Для получение времени из строки в python*
    
    ```python
    >>> datetime.strptime('16:06:43.487', '%H:%M:%S.%f')
    datetime.datetime(1900, 1, 1, 16, 6, 43, 487000)
    ```
    
* Сообщение об окончании высказывания

    ```Speech completed.```

    *Высказывание в данном случае не указывается. Так как робот может воспроизводить только одно высказывание. Поэтому на данном этапе для экономии трафика будет указываться просто Text. Для сложной системы с прерваниями выполнение bml пакетов необходимо указывать текст, а так же добавить сообщения об остановке, средства отмены пакетов и тд.*

* Сообщение о выполнении поворота головы и глаз на собеседника

    ```Gaze completed.```

    *Сообщение будет приходить каждый раз, когда выполнился тег gaze, даже если он был поставлен в очередь не моделью*

* Сообщение о выполнении повота глаз/головы в сторону отличную от собеседника

    ```Turn completed.```

    *Сообщение будет приходить каждый раз, когда выполнились теги, которые связаны с шеей и глазами,() даже если он был поставлен в очередь не моделью*
