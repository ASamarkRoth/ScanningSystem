
""" Evaluating the steps necessary to invoke to move to the new position. 

STEPPER_Y: KK5002 has a lead of 2 mm.
STEPPER_X: KK6005 has a lead of 5 mm.

Both stepper motors 17H261-02S/D has a stepping angle: 1.8 deg (rotarystepper catalogue)
Step-accuracy: +- 0.05 deg (rotarystepper catalogue)

"""
import sys
import numpy as np
import os

settings_file = '.scanning.xy'

step_length_y = (1.8/360)*2
step_length_x = (1.8/360)*5

def pos_eval(new_x, new_y):
    x, y = get_coords()
    limits = list(map(float, read_value("limits")))
    print("Current position is:", x, y)
    new_steps_y = round((new_y-y)/step_length_y)
    new_steps_x = round((new_x-x)/step_length_x)
    new_y = new_steps_y*step_length_y + y
    new_x = new_steps_x*step_length_x + x
    new_y = "{0:.3f}".format(round(new_y,3))
    new_x = "{0:.3f}".format(round(new_x,3))
    if float(new_x) < limits[0] or float(new_x) > limits[1] or float(new_y) < limits[2] or float(new_y) > limits[3]:
        print("ERROR: Tried to move out of set boundary. No stepping is executed and exiting ...")
        sys.exit(2);
    print("New planned position is:", new_x, new_y)
    print("Invoking step:", new_steps_x, new_steps_y)
    return new_steps_x, new_steps_y

def set_new_position(went_x, went_y):
    if went_x == 0 and went_y == 0:
        return
    x_old, y_old = get_coords()
    new_y = went_y*step_length_y + y_old
    new_x = went_x*step_length_x + x_old
    new_y = "{0:.3f}".format(round(new_y,3))
    new_x = "{0:.3f}".format(round(new_x,3))
    print("New position is to be:", new_x, new_y)

def set_real_position(went_x, went_y):
    x_old, y_old = get_coords()
    new_y = went_y*step_length_y + y_old
    new_x = went_x*step_length_x + x_old
    if new_x != 0 and new_y != 0:
        print("OBS: missed steps!")
    new_y = "{0:.3f}".format(round(new_y,3))
    new_x = "{0:.3f}".format(round(new_x,3))
    print("New real position is: ", new_x, new_y )
    set_coords(new_x, new_y)


def read_coords():
    content = 0
    with open("temp."+read_value("read_file")[0]+".scan", 'r') as f:
        content = f.readlines()
        if not content: 
            return None, None
        x, y = map(float, content[0].split())
    with open("temp."+read_value("read_file")[0]+".scan", 'w') as f:
        f.seek(0, 0)
        f.writelines(content[1:])
        return x, y

def get_coords(): 
    with open(settings_file, 'r') as f:
        s, x, y = f.readline().split()
    return float(x), float(y)

def set_coords(x, y): 
    with open(settings_file, 'r+') as f:
        line = "pos "+str(x)+" "+str(y)+"\n"
        content = f.readlines()
        content[0] = line
        f.seek(0, 0)
        f.writelines(content)

def set_power(s):
    print("Executing: ", "./power_setup.sh cmd "+s)
    os.system("./power_set.sh cmd "+s)
    os.system(s +" >> power.log")


def read_value(s):
    with open(settings_file, 'r') as f:
        for line in f.readlines():
            l = line.split()
            if not l:
                break
            if l[0] == s:
                return l[1:]
        print("Could not read value: ", s)

def set_value(s, value):
    rep = -1
    with open(settings_file, 'r') as f:
        for j, line in enumerate(f.readlines()):
            l = line.split()
            if not l: 
                break
            #print("l", l)
            if l[0] == s:
                rep = j
    with open(settings_file, 'r+') as f:
        content = f.readlines()
        #print("Content = ", content)
        content[rep] = s +' '+ ' '.join(value)+'\n'
        f.seek(0, 0)
        f.writelines(content)
    if rep < 0:
        print("Could not read value: ", s)

def generate_swipe_file(s):
    x = np.arange(float(s[1]), float(s[2]) + float(s[3]), float(s[3]))
    y = np.arange(float(s[4]), float(s[5]) + float(s[6]), float(s[6]))
    with open(s[0]+'.scan', 'w') as f:
        for i in range(len(x)):
            for j in range(len(y)):
                if i%2 == 1: 
                    f.write(str(x[-j-1])+' '+str(y[i])+'\n')
                else:
                    f.write(str(x[j])+' '+str(y[i])+'\n')



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

