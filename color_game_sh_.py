from gpiozero import LED, Button
from time import sleep
import random
from subprocess import call

#attempt to import speak module
voice = True
zero = True
try:
    from espeak import espeak                     
except ImportError:
    print("Failed to import espeak module for speech!")
    print("sudo apt-get install espeak python-espeak")
    voice = False

#attempt to import gpiozero module
try:
    from gpiozero import LED, Button                     
except ImportError:
    print("Failed to import gpiozero module! Please install this module tobe able to play the games.")
    print("sudo apt install python-gpiozero")
    gpio = False

class Color_Game():

    def __init__(self, v):      
        # game variables
        self.start = False
        self.round = 1
        self.lives = 3
        self.colors = [] # contain pattern of lights
        self.index = 0
        #self.second = [3, 1, 0.7, 0.3] #seconds between numbers
        #self.diff = 1 # default normal; easy, normal, hard, insane
        #self.diff_s = ['easy', 'normal', 'hard', 'insane']

        # leds
        self.red = LED(18)
        self.green = LED(6)
        self.yellow = LED(17)
        self.blue = LED(27)
        self.green2 = LED(3)
        self.white = LED(5)

        # buttons
        self.b1 = Button(4)
        self.b2 = Button(26)
        self.b3 = Button(2)
        self.b4 = Button(19)
        self.b5 = Button(15)
        self.b6 = Button(14)
        self.be = Button(13)  # exit button
        #self.buttons = [self.b1, self.b2, self.b3, self.b4]

        #linking color to button number
        self.choices = [(self.red, 0 ), (self.green, 1), (self.yellow, 2), (self.blue, 3), (self.green2, 4), (self.white, 5)]
       
        #voice                
        self.voice = v                              

    # check if button pressed matches the color sequence
    def check_color(self, i):
        sleep(0.3)
        # if wrong lose 1 life and reset index
        if self.colors[self.index] != i:
            self.lives -= 1
            self.index = 0

            # exit if no lives left
            if self.lives == 0:
                return 2

            # show pattern again
            self.speak("wrong! Here it is again.")
            for x in self.colors:
                l = self.choices[x][0]
                l.on()
                sleep(1)
                l.off()
                sleep(0.3)
            return 0

        # else increase index
        else:
            self.index += 1

            # if index reaches amount of colors in round then next round
            if self.index == self.round:
                self.speak("good job! round: " + str(self.round + 1))
                self.index = 0
                self.round += 1
                return 1
            else:
                return 0

    # print and say messages
    def speak(self, message):
        print(message)
        if self.voice:
            call(["espeak","-s140 -ven+f3 -z", message])

    #play game
    def play(self):
        
        #intro
        self.speak("Welcome to Color Memorization!")
        self.speak("Press first button to start.")
        self.speak("second button to toggle sound.")
        self.speak("third button for instructions.")
        self.speak("7th button to exit at any time.")

        lost = False
        while True:
            #exit pressed
            if self.be.is_pressed:
                self.speak("Goodbye!")
                break
            
            #play pressed
            if self.b1.is_pressed:
                self.turn_off()
                self.speak("Good Luck!")
                self.start = True               
                break

            # voice toggle pressed
            if self.b2.is_pressed:
                if self.voice:
                    self.voice = False
                    self.speak("Voice has been turned off")                 
                else:
                    self.voice = True
                    self.speak("Voice has been turned on")                  
                sleep(1)

            #insutrctions
            if self.b3.is_pressed:
                self.speak("This is a game where the colors flash and you have to press the coresponding buttons.")
                self.speak("Example: if blue flashes, you press the fourth button since blue is in the 4th position.")
                self.speak("The patttern will repeat and each time a new light will be added.")
                self.speak("You have 3 lives, and lose 1 when you get a number wrong.")
                self.speak("This was made in python to use in a pie or any device supporting GPIOS with python. ")
                sleep(1)

        if self.start:

            #pick difficulty first
            #self.speak("Pick a difficulty with buttons: easy, normal, hard, insane")
            # while True:

            #     # check for pressed buttons
            #     if self.b1.is_pressed:
            #         self.diff = 0                       
            #         break

            #     if self.b2.is_pressed:
            #         self.diff = 1                       
            #         break

            #     if self.b3.is_pressed:
            #         self.diff = 2                       
            #         break

            #     if self.b4.is_pressed:
            #         self.diff = 3                       
            #         break

            while True:
                # if lost exit
                if lost: break

                # flash random color sequence
                self.gen_flash()

                # your turn!
                while True:
                    # if exit is pressed
                    if self.be.is_pressed:
                        self.speak("Goodbye!")
                        lost = True
                        break

                    # game over if 0 lives reached
                    if self.lives == 0:
                        self.speak("you lost in round: " + str(self.round))
                        lost = True
                        break

                    # check for pressed buttons
                    if self.b1.is_pressed:
                        check = self.check_color(0)
                        if check == 1:
                            break

                    if self.b2.is_pressed:
                        check = self.check_color(1)
                        if check == 1:
                            break

                    if self.b3.is_pressed:
                        check = self.check_color(2)
                        if check == 1:
                            break

                    if self.b4.is_pressed:
                        check = self.check_color(3)
                        if check == 1:
                            break
                    if self.b5.is_pressed:
                        check = self.check_color(4)
                        if check == 1:
                            break

                    if self.b6.is_pressed:
                        check = self.check_color(5)
                        if check == 1:
                            break
        sleep(1)

    #game where it creates random patterns of flashing lights
    def gen_flash(self):

        #show current pattern of flash if theres more than 1
        if len(self.colors) != 0:
            for x in self.colors:
                l = self.choices[x][0]
                l.on()
                sleep(1)
                l.off()
                sleep(0.3)
       
       #create new led flash 
        l = self.choices[random.randint(0, 5)]
        l[0].on()
        sleep(1)
        l[0].off()
        self.colors.append(l[1])

    #test if leds are all working, you should see all leds on
    def test(self):
        print("testing if all leds work")
        sleep(0.3)
        for l in self.choices:
            led = l[0]
            led.on()
            sleep(0.5)

    #turning off leds before game
    def turn_off(self):   
        for l in self.choices:
            led = l[0]
            led.off()
        sleep(1)

#if correct module was imported then play game
if zero:
    my_game = Color_Game(voice)
    my_game.test()
    my_game.play()
else:
    print("cannot start game without gpiozero.")