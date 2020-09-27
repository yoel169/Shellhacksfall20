from gpiozero import LED, Button
from time import sleep
import random
from subprocess import call

#attempt to import speak module
voice = True
try:
    from espeak import espeak                     
except ImportError:
    print("Failed to import espeak module for speech!")
    print("sudo apt-get install espeak python-espeak")
    voice = False

#attempt to import gpiozero module
zero = True
try:
    from gpiozero import LED, Button                     
except ImportError:
    print("Failed to import gpiozero module! Please install this module tobe able to play the games.")
    print("sudo apt install python-gpiozero")
    gpio = False

class Number_Game():
    def __init__(self):
        # game variables
        self.start = False
        self.round = 1
        self.lives = 3
        self.index = 0
        self.numbers = []
        self.diff = 1 # default normal; normal, triples, sixes, insane
        self.diff_s = ['normal', 'triples', 'sixes', 'insane']
        self.correct = 0
        self.score = 0
        self.multiplier = 1 # score multiplier
        self.digit = 0 #position of digit in list of numbers
        self.diff_tie = [1,3,6] #tying difficulty with number of digits

        #the following use the pi's GPIO numbers, feel free to change them if needed
        # buttons
        self.b1 = Button(4)
        self.b2 = Button(26)
        self.b3 = Button(2)
        self.b4 = Button(19)
        self.b5 = Button(15)
        self.b6 = Button(14)
        self.be = Button(13)  # exit button

        #LEDS for turning off before game
        self.red = LED(18)
        self.green = LED(6)
        self.yellow = LED(17)
        self.blue = LED(27)
        self.green2 = LED(3)
        self.white = LED(5)
        self.choices = [(self.red, 0 ), (self.green, 1), (self.yellow, 2), (self.blue, 3), (self.green2, 4), (self.white, 5)]


     # print and say messages
    def speak(self, message, p):
        # to prevent from printing numbers!
        if p == 1:
            print(message)

        call(["espeak","-s140 -ven+f3 -z", message])         


    # play game
    def play(self):

        lost = False

         #intro
        self.speak("Welcome to Number Memorization! This game only works with sound.", 1)
        self.speak("Press first button to start.", 1)
        self.speak("second button for instructions.", 1)
        self.speak("7th button to exit at any time.", 1)

        while True:
            #exit pressed
            if self.be.is_pressed:
                self.speak("Goodbye!", 1)
                break
            
            #play pressed
            if self.b1.is_pressed:
                self.speak("Good Luck!", 1)
                self.start = True               
                break

            #insutrctions
            if self.b2.is_pressed:
                self.speak("This is a game where you're given random numbers and you have to keep up.", 1)
                self.speak("Example: if you're given 5, you press the 5th button.", 1)
                self.speak("The patttern will repeat and each time a new number will be added.", 1)
                self.speak("You have 3 lives, and lose 1 when you get a number wrong.", 1)
                self.speak("Normal mode gives you 1 number at a time, increasing over time", 1)
                self.speak("Triples mode gives you three numbers at a time to remember.", 1)
                self.speak("Sixes mode you get six numbers at a time.", 1)
                self.speak("Insane mode is the same as normal but you only get 1 life.", 1)
                self.speak("You get a life every 3 rounds you get correct except in insane mode.", 1)
                self.speak("Each correct round you get 5 points.", 1)
                self.speak("Score multiplier goes up every 5 rounds in normal and insane, 3 in triples and sixes.", 1)
                self.speak("This was made in python to use in a pie or any device supporting GPIOS with python. ", 1)
                sleep(1)

        #play!
        if self.start:

            #pick difficulty first
            self.speak("Pick a difficulty with buttons: normal, triples, sixes, insane", 1)
            while True:

                # check for pressed buttons
                if self.b1.is_pressed:
                    self.diff = 0 
                    break

                if self.b2.is_pressed:
                    self.diff = 1                       
                    break

                if self.b3.is_pressed:
                    self.diff = 2                       
                    break

                if self.b4.is_pressed:
                    self.diff = 3                       
                    break
            
            self.speak("you picked: " + self.diff_s[self.diff], 1)

            #play loop
            while True:
                # if lost exit
                if lost: break

                # flash random number sequence
                self.gen_number()

                # your turn!
                while True:
                    # if exit is pressed
                    if self.be.is_pressed:
                        self.speak("Goodbye!", 1)
                        self.speak("your score was: " + str(self.score), 1)
                        lost = True
                        break

                    # game over if 0 lives reached
                    if self.lives == 0:
                        self.speak("you lost in round: " + str(self.round), 1)
                        self.speak("with a score of: " + str(self.score), 1)
                        lost = True
                        break

                    # check for pressed buttons
                    if self.b1.is_pressed:
                        if self.diff == 0 or self.diff == 3:
                            check = self.check(1)
                        else:
                            check = self.check2(1)    
                        if check == 1:
                            break

                    if self.b2.is_pressed:
                        if self.diff == 0 or self.diff == 3:
                            check = self.check(2)
                        else:
                            check = self.check2(2) 
                        if check == 1:
                            break

                    if self.b3.is_pressed:
                        if self.diff == 0 or self.diff == 3:   
                            check = self.check(3)
                        else:
                            check = self.check2(3) 
                        if check == 1:
                            break

                    if self.b4.is_pressed:
                        if self.diff == 0 or self.diff == 3:   
                            check = self.check(4)
                        else:
                            check = self.check2(4) 
                        if check == 1:
                            break
                    if self.b5.is_pressed:
                        if self.diff == 0 or self.diff == 3:  
                            check = self.check(5)
                        else:
                            check = self.check2(5) 
                        if check == 1:
                            break

                    if self.b6.is_pressed:
                        if self.diff == 0 or self.diff == 3:
                            check = self.check(6)
                        else:
                            check = self.check2(6) 
                        if check == 1:
                            break     

    #generate new number patterns
    def gen_number(self):

        # game mode normal or insane
        if self.diff == 0 or self.diff == 3:
            #show current number pattern
            if len(self.numbers) != 0:
                for x in self.numbers:
                    self.speak(str(x), 0)

            #create new number pattern
            l = random.randint(1, 6)
            self.speak(str(l), 0)
            self.numbers.append(l)

        # triples and sixes
        else:
            x = [] # making numbers
            s = 0  # number of digits per number

            # show current number pattern
            if len(self.numbers) != 0:
                for current_list in self.numbers:
                    self.speak(str(self.convert(current_list)), 0)
                    
            #generate numbers
            if self.diff == 1:
                s = 3
            elif self.diff == 2:
                s = 6 

            for t in range(s):
                x.append(random.randint(1,6))
            self.numbers.append(x)
            self.speak(str(self.convert(x)), 0)
            

    # of integers into a single integer 
    def convert(self, l): 
      
        # Converting integer list to string list 
        # and joining the list using join() 
        res = int("".join(map(str, l)))    
        return res 


    # check if user entered correct number
    def check(self, n):
        sleep(0.3)
        if self.numbers[self.index] != n:
            if self.diff == 3:
                self.lives = 0
                return 2
            else:
                self.lives -= 1
                self.index = 0
                self.correct = 0

            # exit if no lives left
            if self.lives == 0:
                return 2

            # show pattern again
            self.speak("wrong! Here it is again.", 1)
            self.speak("you have " + str(self.lives) + " lives left.", 1)
            for x in self.numbers:
                self.speak(str(x), 0)
            return 0

        # else correct
        else:
            self.index += 1

            # if index reaches amount of numbers in round then next round
            if self.index == self.round:
                self.correct += 1
                self.speak("good job! round: " + str(self.round + 1), 1)
                self.index = 0
                self.round += 1
                self.score += 5 * self.multiplier

                #increase multiplier every 5 waves
                if self.round % 5 == 0:
                    self.multiplier +=1
                    self.speak("score multiplier increased to " + str(self.multiplier), 1)

                # 5 streak increase lives by 1
                if self.correct == 3:
                    self.lives += 1
                    self.correct = 0
                    self.speak("lives increased by 1", 1)   
                return 1
            else:
                return 0


    # check for more than 1 digit per number
    def check2(self, n):
        sleep(0.3)   
        #incorrect   
        if self.numbers[self.index][self.digit] != n:
            if self.diff == 3:
                self.lives = 0
                return 2
                     
            self.index = 0
            self.digit = 0
            self.lives -= 1
            self.correct = 0

            # exit if no lives left
            if self.lives == 0:
                return 2

            # show pattern again
            self.speak("wrong! Here it is again.", 1)
            self.speak("you have " + str(self.lives) + " lives left.", 1)
            for numbers in self.numbers:
                self.speak(str(self.convert(numbers)), 0)
            return 0

        else:
            self.digit += 1

            # go to next number
            if self.digit == self.diff_tie[self.diff]:
                self.index += 1
                self.digit = 0

                # if index reaches amount of numbers in round then next round
                if self.index == self.round:
                    self.speak("good job! round: " + str(self.round + 1), 1)
                    self.index = 0
                    self.round += 1
                    self.correct += 1
                    self.score += 5 * self.multiplier

                    #increase multiplier
                    if self.round % 3 == 0:
                        self.multiplier +=1
                        self.speak("score multiplier increased to " + str(self.multiplier), 1)

                    # 3 streak increase lives by 1
                    if self.correct == 3:
                        self.correct = 0
                        self.lives += 1
                        self.speak("lives increased by 1", 1)

                    return 1
                else:
                    return 0


    #turning off leds before game
    def turn_off(self):   
        for l in self.choices:
            led = l[0]
            led.off()
        sleep(1)

if voice and zero:
    print("Make sure you turn up your speakers to hear game.")

    my_game = Number_Game()
    my_game.turn_off()
    my_game.play()