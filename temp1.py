#!/usr/bin/python3
"""
Names: <Tapiwa Matar>
Student Number: <MTRTAP003>
Prac: <Prac 1>
Date: <31/07/2019>
"""

# import Relevant Librares
import RPi.GPIO as GPIO
import itertools
import time

#definition
count =0 #count value to keep count of iterations
binn = list(itertools.product([0,1], repeat=3)) # list of binary numbers 0-7

#GPIO SETUP
GPIO.setmode(GPIO.BOARD) # sets GPIO to board
GPIO.setup(11, GPIO.OUT) # configures GPIO 11 to output
GPIO.setup(13, GPIO.OUT) # configures GPIO 13 to output
GPIO.setup(15, GPIO.OUT) # configures GPIO 15 to output 
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP) # configures GPIO 16 to input, with pull up resistor
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) # configures GPIO 18 to input, with pull up resistor
GPIO.output(11, 0) #initialize the gpio with output low
GPIO.output(13, 0)
GPIO.output(15, 0)

#mycallback for interuption
def my_callback(channel):
    global count #call to  global count 
    if channel == 16:
        count = count + 1 # change direction of iteration to sum
        print('This is a edge event callback function!')
        print('Edge detected on channel 16')
    elif channel ==  18:
        count = count -1 # change direction of iteration to subtraction
        print('This is a edge event callback function!')
        print('Edge detected on channel 18')

# Logic
def main():
    global count  # call to global count value
    while True:
        time.sleep(0.01) # sleep time to allow cpu to do other things
        if GPIO.event_detected(16) or GPIO.event_detected(18): #if either buttons are pressed
            if count ==8: #if iteration overflows to 8 return to 0
                count = 0
                GPIO.output(11, binn[count][0]) # displays binary 0 after 8 overflow 
                GPIO.output(13, binn[count][1])
                GPIO.output(15, binn[count][2])
            elif count ==-1: # if iteration overflows to -1 return to 7 
                count = 7
                GPIO.output(11, binn[count][0]) #displays binary 7 after -1 overflow 
                GPIO.output(13, binn[count][1])
                GPIO.output(15, binn[count][2])
            elif count>=0 and count <=7: # check if number is in range [0, 7]
                GPIO.output(11, binn[count][0]) #sets the output at gpio with reference to binary represantation of count 
                GPIO.output(13, binn[count][1])
                GPIO.output(15, binn[count][2])

# add rising edge detection on a channel, ignoring further edges for 200ms for switch bounce handling
GPIO.add_event_detect(16, GPIO.FALLING, callback=my_callback, bouncetime=300)
# add rising edge detection on a channel, ignoring further edges for 200ms for switch bounce handling
GPIO.add_event_detect(18, GPIO.FALLING, callback=my_callback, bouncetime=300)

# Only run the functions if 
if __name__ == "__main__":
    # Make sure the GPIO is stopped correctly
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("Exiting gracefully")
        # Turn off your GPIOs here
        GPIO.cleanup()
    except Exception as e:
        GPIO.cleanup()
        print("Some other error occurred")
        print(e.message)
