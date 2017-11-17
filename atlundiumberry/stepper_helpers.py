
""" Evaluating the steps necessary to invoke to move to the new position. 

STEPPER_Y: KK5002 has a lead of 2 mm.
STEPPER_X: KK6005 has a lead of 5 mm.

Both stepper motors 17H261-02S/D has a stepping angle: 1.8 deg (rotarystepper catalogue)
Step-accuracy: +- 0.05 deg (rotarystepper catalogue)

"""
import sys
import numpy as np
import os

import yaml

settings_file = '.test.yaml'

step_length_y = (1.8/360)*2
step_length_x = (1.8/360)*5


class Scanner:

    def __init__(self, config_file):
        self.config_file = config_file

    def ChangeSetting(self, setting, value):
        stream = open(self.config_file, 'r+')
        doc = yaml.load(stream)
        if setting in doc:
            doc[setting] = value
        else:
            print("Setting", setting, "does not exist in the configure file")
            return False
        stream.seek(0)
        stream.truncate()
        yaml.dump(doc, stream)
        stream.close()
        return True

    def ReadSetting(self, setting):
        stream = open(self.config_file, 'r+')
        doc = yaml.load(stream)
        if setting not in doc:
            print("Setting", setting, "does not exist in the configure file")
            return None
        stream.close()
        print("yaml=", doc)
        return doc[setting]

    def PosEval(self, new_x, new_y):
        x, y = self.ReadSetting("pos")
        limits = self.ReadSetting("limits")
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

    def SetNewPosition(self, went_x, went_y):
        if went_x == 0 and went_y == 0:
            return
        x_old, y_old = self.ReadSetting("pos")
        new_y = went_y*step_length_y + y_old
        new_x = went_x*step_length_x + x_old
        new_y = "{0:.3f}".format(round(new_y,3))
        new_x = "{0:.3f}".format(round(new_x,3))
        print("New position is to be:", new_x, new_y)

    def SetRealPosition(self, went_x, went_y):
        x_old, y_old = ReadSetting("pos")
        new_y = went_y*step_length_y + y_old
        new_x = went_x*step_length_x + x_old
        new_y = "{0:.3f}".format(round(new_y,3))
        new_x = "{0:.3f}".format(round(new_x,3))
        print("New real position is: ", new_x, new_y )
        ChangeSetting("pos", [new_x, new_y])
        with open("coords.log", 'a') as f_temp:
            f_temp.write(new_x + " " + new_y+"\n")

    def PerformedMove(self):
        with open("temp."+read_value("read_file")[0]+".scan", 'r') as f_in:
            content = f_in.readlines()
        with open("temp."+read_value("read_file")[0]+".scan", 'w') as f_out:
            f_out.seek(0, 0)
            f_out.writelines(content[1:])

    def SetPower(self, s):
        print("Executing: ", "./power_setup.sh cmd "+s)
        os.system("./power_set.sh cmd "+s)
        os.system(s +" >> power.log")

    def GenerateSwipeFile(self, s):
        x = np.arange(float(s[1]), float(s[2]) + float(s[3]), float(s[3]))
        y = np.arange(float(s[4]), float(s[5]) + float(s[6]), float(s[6]))
        with open(s[0]+'.scan', 'w') as f:
            for i in range(len(x)):
                for j in range(len(y)):
                    if i%2 == 1: 
                        f.write(str(x[-j-1])+' '+str(y[i])+'\n')
                    else:
                        f.write(str(x[j])+' '+str(y[i])+'\n')

if __name__ == '__main__':
    pos = [1, 1]
    scan = Scanner(settings_file)
    scan.ChangeSetting("read_file222", "surface")
    readf = scan.ReadSetting("stop")
    print("Readf=",readf)
    stream = open(settings_file, 'r+')
    stream.seek(0)
    print("File content:\n",stream.read())
    stream.close()
    #print(yaml.dump(doc))

