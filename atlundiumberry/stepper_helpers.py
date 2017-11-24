
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

class Scanner:

    def __init__(self, config_file):
        self.config_file = config_file
        self.step_length_y = (1.8/360)*2
        self.step_length_x = (1.8/360)*5


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
        #print("yaml=", doc)
        return doc[setting]

    def ReadCoordsFile(self):
        with open("temp."+self.ReadSetting("read_file")+".scan", 'r') as f:
            content = f.readlines()
            if len(content) > 0:
                return map(float, (content[0].rsplit()))
            else:
                return None, None
            

    def PosEval(self, new_x, new_y):
        x, y = self.ReadSetting("pos")
        print("Current position is:", x, y)
        new_steps_y = round((new_y-float(y))/self.step_length_y)
        new_steps_x = round((new_x-float(x))/self.step_length_x)
        new_y = new_steps_y*self.step_length_y + float(y)
        new_x = new_steps_x*self.step_length_x + float(x)
        new_y = "{0:.3f}".format(round(new_y,3))
        new_x = "{0:.3f}".format(round(new_x,3))
        print("New planned position is:", new_x, new_y)
        print("Invoking step:", new_steps_x, new_steps_y)
        return new_steps_x, new_steps_y

    def SetNewPosition(self, went_x, went_y):
        if went_x == 0 and went_y == 0:
            return
        x_old, y_old = self.ReadSetting("pos")
        new_y = went_y*self.step_length_y + float(y_old)
        new_x = went_x*self.step_length_x + float(x_old)
        new_y = "{0:.3f}".format(round(new_y,3))
        new_x = "{0:.3f}".format(round(new_x,3))
        print("New position is to be:", new_x, new_y)

    def SetRealPosition(self, went_x, went_y):
        x_old, y_old = self.ReadSetting("pos")
        new_y = went_y*self.step_length_y + float(y_old)
        new_x = went_x*self.step_length_x + float(x_old)
        new_y = "{0:.3f}".format(round(new_y,3))
        new_x = "{0:.3f}".format(round(new_x,3))
        print("New real position is: ", new_x, new_y )
        self.ChangeSetting("pos", [new_x, new_y])
        with open("coords.log", 'a') as f_temp:
            f_temp.write(new_x + " " + new_y+"\n")

    def PerformedMove(self):
        print(self.ReadSetting("read_file"))
        with open("temp."+self.ReadSetting("read_file")+".scan", 'r') as f_in:
            content = f_in.readlines()
        with open("temp."+self.ReadSetting("read_file")+".scan", 'w') as f_out:
            f_out.seek(0, 0)
            f_out.writelines(content[1:])

    def SetPower(self, s):
        print("Executing: ", "./power_set cmd "+s)
        os.system("./power_set cmd "+s)
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

