#################################################################
#  stepper.py - Stepper motor control using Gertbot and Python  #
#  Based on Gertbot example code at http://www.gertbot.com/     #
#################################################################

import stepper_helpers as sh

import sys
import argparse

parser = argparse.ArgumentParser("Specify how many steps that should be taken in as: 'steps_x steps_y'")
parser.add_argument("-step", dest='steps', type=int, help="steps_x steps_y", nargs=2)
parser.add_argument("-N", dest='new_xy', nargs=2, help="Start a new run from scratch with new origin.")
parser.add_argument("-new", dest='restart', action="store_true", help="Start a new run from scratch with origin the same last saved.")
parser.add_argument("-xy", dest='xy', nargs=2, help="Provide the new coordinates as: 'x y' (mm)")
parser.add_argument("-set_limits", dest='limits', nargs=4, help="Set boundary limits of the current coordinate system: 'x_low x_high y_low y_high' (mm)")
parser.add_argument("-file_xy", dest='file_xy', nargs=1, help="Provide the file name from which the position data is to be read from.")
args = parser.parse_args()

if len(sys.argv)==1:
	parser.print_help()
	sys.exit(1)

print("args = ", args)

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
	print("Invoking step:", steps_x, steps_y)

elif args.file_xy:
	print("Reading coordinates from file ... (SHOULD BE IMPLEMENTED?)")
	sys.exit()


if not steps_x or not steps_y: 
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
FREQ = 50.0        # frequency

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

# on exit stop everything
#gb.emergency_stop()


