# Shellhacksfall20
Shellhack Fall 2020 challenge
We decided to work towards the Best Hack for Social Good by JPMorgan Chase challenge.
Welcome to our Shellhacks project.
This project is aimed to improve mental health during covid by helping you build memory skills.
During these hard times, people have more stress, anxiety, and depression because of economic ression, covid, and long quarantine times.
These games are aimed to distract you from todays issues while helping you improve your memory skills and learning something new.
The games were made in python.

Color memorization and number memorization are made to work with buttons and leds connected to a raspberry pi, but can work with any device that uses GPIOS and pi.
If you haven't worked with pi or GPIOS before, it can be really fun experience and can become a hobby fast!
On the file theres a picture provided on how the setup looks. Inside the files you can change which GPIO pins you used if needed.

Color memorization is like the Simon game, where you have to follow the random flashing color sequences and press the correspndong buttons, getting a new color every round, and you have 3 lives/chances to get the sequences correct. Number memorization is similar but with numbers and only works with sound. Each time you get a new random number 1-6, and you have to press the corresponding button. There is also four different modes: normal, triples, sixes, and insane. Normal mode gives you 1 number at a time, increasing over time. Triples mode gives you three digit numbers at a time to remember. Sixes mode you get six digit numbers at a time. Insane mode is the same as normal but you only get 1 life. You get a life every 3 rounds you get correct except in insane mode. Each correct round you get 5 points. Score multiplier goes up every 5 rounds in normal and insane, 3 in triples and sixes.
