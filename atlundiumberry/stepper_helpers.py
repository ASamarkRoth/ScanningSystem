
""" Evaluating the steps necessary to invoke to move to the new position. 

STEPPER_Y: KK5002 has a lead of 2 mm.
STEPPER_X: KK6005 has a lead of 5 mm.

Both stepper motors 17H261-02S/D has a stepping angle: 1.8 deg (rotarystepper catalogue)
Step-accuracy: +- 0.05 deg (rotarystepper catalogue)

"""

settings_file = '.scanning.xy'

def pos_eval(new_x, new_y):
	x, y = get_coords()
	print("Current position is:", x, y)
	step_length_y = (1.8/360)*2
	step_length_x = (1.8/360)*5
	new_steps_y = round((new_y-y)/step_length_y)
	new_steps_x = round((new_x-x)/step_length_x)
	new_y = new_steps_y*step_length_y + y
	new_x = new_steps_x*step_length_x + x
	new_y = "{0:.3f}".format(round(new_y,3))
	new_x = "{0:.3f}".format(round(new_x,3))
	print("New position is:", new_x, new_y)
	set_coords(new_x, new_y)
	return new_steps_x, new_steps_y

def get_coords(): 
	with open(settings_file, 'r') as f:
		s, x, y = map(float, f.readline().split())
	return x, y

def set_coords(x, y): 
	with open(settings_file, 'r+') as f:
		line = "pos"+str(x)+" "+str(y)+"\n";
		content = f.readlines()
                content[0] = line
		#f.seek(0, 0)
		f.writelines(content)

def line_prepender(filename, line):
	with open(filename, 'r+') as f:
		content = f.read()
		f.seek(0, 0)
		f.write(line.rstrip('\r\n') + '\n' + content)

def deleteContent(fName):
	with open(fName, "w"):
		pass

def insertContent(fName, line):
	with open(fName, "w") as f:
		f.write(line)

