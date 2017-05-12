#!/usr/bin/python3

#################################################################
#  stepper.py - Stepper motor control using Gertbot and Python  #
#  Based on Gertbot example code at http://www.gertbot.com/     #
#################################################################

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("steps", type=int, help="number of steps (neg/pos)")
args = parser.parse_args()

import time

# Use the Gertbot drivers
import gertbot as gb

# This is for the development environment:
BOARD = 0           # which board we talk to
STEPPER_A = 0       # channel for first stepper motor
MODE  = 24          # stepper control, gray code
# mode    0=odd
#         1=brushed
#         2=DCC
#         8=step gray off
#         9=step pulse off 
#        24=step gray powered
#        25=step pulse powered
FREQ = 400.0        # frequency

# Main program

# Open serial port to talk to Gertbot
gb.open_uart(0)

# Setup the channels for stepper motors
gb.set_mode(BOARD,STEPPER_A,MODE)
gb.freq_stepper(BOARD,STEPPER_A,FREQ)

# do the actual move
gb.move_stepper(BOARD,STEPPER_A,args.steps)

status = gb.read_error_status(BOARD)
if status != 0:
  print("Gertbot reports error(s):")    
  print(gb.error_string(status))
else:
  print("all good!")  

# on exit stop everything
#gb.emergency_stop()


