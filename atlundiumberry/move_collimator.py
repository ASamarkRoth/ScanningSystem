#!/usr/bin/python3

import stepper_helpers as sh

import os
import sys
import argparse
import shutil

parser = argparse.ArgumentParser("Specify how many steps that should be taken in as: 'steps_x steps_y'")
parser.add_argument("-step", dest='steps', type=int, help="steps_x steps_y", nargs=2)
parser.add_argument("-N", dest='new_xy', nargs=2, help="Start a new run from scratch with new origin.")
parser.add_argument("-new", dest='restart', action="store_true", help="Start a new run from scratch with origin the same last saved.")
parser.add_argument("-xy", dest='xy', nargs=2, help="Provide the new coordinates as: 'x y' (mm)")
parser.add_argument("-set_limits", dest='limits', nargs=4, help="Set boundary limits of the current coordinate system: 'x_low x_high y_low y_high' (mm)")
parser.add_argument("-swipe_file", dest='swipe', nargs=7, help="Generate a file with coordinates to perform an (x0-x1, y0-y1) with step lengths (dx, dy) swipe scan. As: 'file_name x0 x1 dx y0 y1 dy'. Neglect file ending.")
parser.add_argument("-file_xy", dest='file_xy', nargs=1, help="Provide the file name from which the position data is to be read from. If file is set then every time the program is executed the collimator will move to the positions indicated in the file. A temporary file temp.'file name'.scan is deleted if the scan is completed.")
parser.add_argument("-set_freq", dest='freq', nargs=1, help="Set freq as: 'new_freq' (Hz)")
parser.add_argument("-set_defaults", dest='defs', action="store_true", help="Reset default settings.")
parser.add_argument("-set_power_com", dest='tdk', action="store_true", help="Set up the power supply communication (tdk-lambda Gen 50-30). OBS: this activates automatic power ON/OFF over the operation.")
parser.add_argument("-no_power_com", dest='no_tdk', action="store_true", help="Inactivate automatic power supply communication and power ON/OFF during operation.")
parser.add_argument("-v", dest='view', action="store_true", help="View current settings.")
args = parser.parse_args()

steps_x = 0
steps_y = 0

if len(sys.argv)==1:
    if int(sh.read_value("is_file")[0]):
        x, y = sh.read_coords()
        if x == None and y == None:
            sh.set_value("is_file", '0')
            os.remove("temp."+sh.read_value("read_file")[0]+".scan")
            sys.exit()
        steps_x, steps_y = sh.pos_eval(x, y)
    else:
        parser.print_help()
        sh.set_value("is_file", '0')
        sys.exit(1)

print("args = ", args)

if args.tdk:
    print("Setting up power supply communication ")
    os.system("echo 'Setting up tdk-lambda'")
    os.system("./power_set.sh setup")
    sh.set_value("is_power_com", '1')

if args.no_tdk:
    print("Inactivating power supply communication ")
    sh.set_value("is_power_com", '0')

if args.view:
    print("\nCurrent settings are:")
    os.system("cat .scanning.xy")
    print("")

if args.limits:
    print("Setting limits to: ", args.limits)
    sh.set_value("limits", args.limits)

if args.freq:
    print("Setting frequency to: ", args.freq)
    sh.set_value("freq", args.freq)

if args.defs:
    print("Setting defaults")
    sh.set_value("freq", ['50'])
    sh.set_value("limits", ['-10','60','-10','60'])
    sh.set_value("is_file", ['0'])
    sh.set_value("is_power_com", ['0'])

if args.swipe:
    print("Generating swipe file:", args.swipe[0]+".scan")
    sh.generate_swipe_file(args.swipe)

if args.file_xy:
    print("Setting file to read from:", args.file_xy)
    sh.set_value("is_file", ['1'])
    sh.set_value("read_file", args.file_xy)
    shutil.copyfile(args.file_xy[0]+".scan", "temp."+args.file_xy[0]+".scan")

if args.restart: 
    print("Restarting the analysis with start coordinates as the last ones in \".positions.xy\"")	
    x, y = sh.get_coords()
    sh.deleteContent('move_data/.positions.xy')
    sh.set_coords(x,y)
    sys.exit()

elif args.new_xy != None: 
    sh.deleteContent('move_data/.positions.xy')
    sh.set_coords(float(args.new_xy[0]), float(args.new_xy[1]))
    print("The data has been reset and the new origin has been successfully added to \".positions.xy\"")
    sys.exit()

elif args.steps:
    steps_x = args.steps[0]
    steps_y = args.steps[1]

elif args.xy:
    steps_x, steps_y = sh.pos_eval(float(args.xy[0]), float(args.xy[1]))
    print("Stepping [x, y]: [", steps_x,", ",steps_y,"]")

if steps_x == 0 and steps_y == 0: 
    print("Exiting since no steps set")
    sys.exit()

print("Stepping [x, y]: [", steps_x,", ",steps_y,"]")

#pos_eval(0,0)

import time

# Use the Gertbot drivers
import gertbot as gb

# Initial settings:
BOARD = 3           # which board we talk to
# View the linear units from the where the wagons are as close as possible to the motors: Y is bottom motor (i.e. running the KK50) and X is top motor (i.e. running the KK60)
STEPPER_Y = 0       # channel for first stepper motor
STEPPER_X = 2       # channel for second stepper motor
MODE = gb.MODE_STEPG_OFF          # stepper control, gray code
# mode    0=odd
#         1=brushed
#         2=DCC
#         8=step gray off
#         9=step pulse off 
#        24=step gray powered
#        25=step pulse powered
FREQ = float(sh.read_value("freq")[0])        # frequency

print("Set frequency is:", FREQ)

# Main program

# Open serial port to talk to Gertbot
print("Opening serial port ...")
gb.open_uart(0)

# Setup the channels for stepper motors
print("Setting up channels for stepper motors ...")
gb.set_mode(BOARD,STEPPER_Y,MODE)
gb.freq_stepper(BOARD,STEPPER_Y,FREQ)
gb.set_mode(BOARD,STEPPER_X,MODE)
gb.freq_stepper(BOARD,STEPPER_X,FREQ)

# END-STOP NEEDS TO BE IMPLEMENTED CAREFULLY. (note motor polarisation and j3-pin!)
# ENDSTOP_OFF = 0
# ENDSTOP_LOW = 1
# ENDSTOP_HIGH = 2

# Setting active-low endstop for direction B, OFF for dir A. 
#gb.set_endstop(BOARD, STEPPER_Y, gb.ENDSTOP_OFF, gb.ENDSTOP_LOW)

if int(sh.read_value("is_power_com")[0]):
    print("Activating power")
    sh.set_power("OUT 1")
    time.sleep(2) #this is to ensure power is on

# DO THE ACTUAL MOVE
print("Invoking move ...")
gb.move_stepper(BOARD,STEPPER_Y,steps_y)
gb.move_stepper(BOARD,STEPPER_X,steps_x)

time.sleep(5)

#Checking status after move for both motors and aborts if anything is wrong.
motor_status = gb.get_motor_status(BOARD, STEPPER_Y)
print("Motor status Y: ", motor_status) 
if steps_y != 0 and any(motor_status) != 0:
    print("There was a motor error/end stop reached for motor Y. - The run is aborted.")

motor_status = gb.get_motor_status(BOARD, STEPPER_X)
print("Motor status X: ", motor_status)
if steps_x != 0 and any(motor_status) != 0:
    print("There was a motor error/end stop reached for motor X. - The run is aborted.")

status = gb.get_io_setup(BOARD)
print("Status: ", status)

missed = gb.get_motor_missed(BOARD, STEPPER_Y)
print("Missed Y: ", missed)
missed = gb.get_motor_missed(BOARD, STEPPER_X)
print("Missed X: ", missed)

print("Reading error status ...")
status = gb.read_error_status(BOARD)
print("Status received ...")
if status != 0:
    print("Gertbot reports error(s):")    
    print(gb.error_string(status))
else:
    print("all good!")  

# Added this to avoid motor going into pwr state after end-stop activation.
gb.set_mode(BOARD,STEPPER_X,MODE)

if int(sh.read_value("is_power_com")[0]):
    print("Deactivating power")
    sh.set_power("OUT 0")

# on exit stop everything
#gb.emergency_stop()


