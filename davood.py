#!/usr/bin/python3
import RPi.GPIO as gpio
import random
import time
import os
from getch import Getch

# CONSTANT VALUES
LEDS = [17, 27, 22, 11]
BUZZER = 9

# COLOR SEQUENCE ARRAY
colors = []

# INIT GETCH
getc = Getch()

def setup():
    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)
    gpio.setup(LEDS, gpio.OUT, initial=gpio.LOW)
    gpio.setup(BUZZER, gpio.OUT, initial=gpio.LOW)

def controllerInput(key):
    if key == 'w':
        return LEDS[0]
    elif key == 'a':
        return LEDS[1]
    elif key == 's':
        return LEDS[2]
    elif key == 'd':
        return LEDS[3]

def generateColor():
    rand = random.randint(1,4)
    if rand == 1:
        return LEDS[0]
    elif rand == 2:
        return LEDS[1]
    elif rand == 3:
        return LEDS[2]
    elif rand == 4:
        return LEDS[3]

def flashLed(pin, delay):
    gpio.output(pin, gpio.HIGH)
    gpio.output(BUZZER, gpio.HIGH)
    time.sleep(delay)
    gpio.output(pin, gpio.LOW)
    gpio.output(BUZZER, gpio.LOW)

def play_setColors(level):
    new_color = generateColor()
    colors.append(new_color)
    for i in colors:
        flashLed(i, 1.5-(level*.05))

def userIndicatorNote(delay=0.13):
    gpio.output(BUZZER, gpio.HIGH)
    time.sleep(delay)
    gpio.output(BUZZER, gpio.LOW)
    time.sleep(delay)
    gpio.output(BUZZER, gpio.HIGH)
    time.sleep(delay)
    gpio.output(BUZZER, gpio.LOW)

def isCorrectColors():
    for i in colors:
        key = controllerInput(getc.impl())
        if key == i:
            flashLed(key, 0.2)
        else:
            return True
    return False

def gameOverIndicator(delay=0.2):
    gpio.output(BUZZER, gpio.HIGH)
    for i in range(20):
        gpio.output(LEDS, gpio.HIGH)
        time.sleep(delay)
        gpio.output(LEDS, gpio.LOW)
        time.sleep(delay)
    gpio.output(BUZZER, gpio.LOW)

def introduction():
    is_play = False
    print("#####################################################")
    print("###  Davood's Says Game (Raspberry Pi Edition)   ####")
    print("###\t\t By Dominic Antigua \t\t####")
    print("###################################################")
    print("Control Keys: \nW = RED LED\nA = GREEN LED\nS = BLUE LED\nD = YELLOW LED\n")
    print("---------------------------------------------------")
    while not is_play:
        upress = input("Type 'y'/ 'yes' to start play the game(y/yes): ")
        if upress.lower() == 'y' or upress.lower() == 'yes':
            is_play = True
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        
def main():
    # GAME INDICATOR
    level = 1
    gameOver = False
    # Setting Up GPIO and Gameplay
    os.system('cls' if os.name == 'nt' else 'clear')
    setup()
    introduction()
    try:
        while not gameOver and (level < 30):
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Current Level: ", level)
            play_setColors(level)
            userIndicatorNote()
            print("Press the key now!!!")
            gameOver = isCorrectColors()
            time.sleep(1)
            level = level+1 if not gameOver else level
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Highest Level: ", level)
        print("Davood Says, Game Over!!!\n")
        gameOverIndicator()
    finally:
        gpio.cleanup()

main()