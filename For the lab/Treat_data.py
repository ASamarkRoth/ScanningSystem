import csv                               ## for reading in our data files
import logging                           ## for orderly print output
import numpy as np                       ## for handling of data
import matplotlib.pyplot as plt          ## for plotting
import sys                               ## useful system calls (used to exit cleanly)


n = 8192  #number of channels used by the MCA
m = 30000  #limit on y (number of counts)
dataFile = 'yourfile.Spe'  #the file we want to read (.Spe if saved with Maestro in ASCII SPE format, .txt works also)
title = "Cobalt 60 Spectrum"  #the title we want to give our plot


#we create a class composed of the data that is in the file and some functions that can be used on this new class "Spectrum" 
class Spectrum:
    """A class to hold our spectrum measurement data and meta data (such as duration)"""
    def __init__(self, filename):
        self.filename = filename
        self.x = np.array(np.zeros(1))    
        self.y = np.array(np.zeros(1))
        self.name = filename   
        self.duration = 0
    def subtract_from_data(self, m):
        self.y = self.y - m.y
        self.y[self.y < 0] = 0;
    def scale_data(self, scale):
        self.y *= scale

        
#This is the core of the program to read the data from a file.
def read_mca_data_file(filename):
    log = logging.getLogger('gammalab_analysis') ## set up logging
    m = Spectrum(filename) ## create a new Spectrum measurement object; this is what we return in the end
    log.info("Reading data from file '" + filename + "'")
    try:
        with open(filename) as f:
            reader = csv.reader(f)
            interval = []        
            for row in reader:
                if row[0] == '$MEAS_TIM:':
                    log.debug("Parsing MEAS_TIM header info")
                    row = next(reader)
                    duration = [int(s) for s in row[0].split(' ')]
                    m.duration = duration[1] ## two parts: CPU/realtime; take the second
                if row[0] == '$DATA:':
                    log.debug("Parsing DATA header info")
                    row = next(reader)
                    interval = [int(s) for s in row[0].split(' ')]
                    break
            log.debug("Done with header parsing")
            nbins = int(interval[1]-interval[0])+1
            m.y = np.array(np.zeros(nbins))
            for idx, row in enumerate(reader):
                if idx >= nbins:
                    break
                m.y[idx] = int(row[0])
            m.x = np.arange(interval[0], interval[1]+1,1)
            log.debug("Loaded all data from file")
    except IOError:
        log.error("Could not find the file '"+str(filename)+"'")
        sys.exit(-1)
    return m

if __name__ == '__main__':
    FORMAT = '%(asctime)s %(name)s:line %(lineno)-4d %(levelname)-8s %(message)s'
    logging.basicConfig(format=FORMAT)
    log = logging.getLogger('gammalab_analysis') ## set up logging
    log.setLevel("INFO")


    ## read in the data file
    spectrum = read_mca_data_file(dataFile)
    if not spectrum:
        sys.exit()
        
    #Plot the data
    plt.figure()
    #add axis titles and general title
    plt.xlabel('Channel')
    plt.ylabel('Counts')
    plt.title(title)
    plt.xlim([0, n])                                       ##add a limit on x (number of channels)
    #plt.ylim([0, m])                                      ##add a limit on y
    #plt.yscale('log')                                     ## set y axis to log scale
    plt.grid(True)                                         ## enable a grid to guide the eye
    plt.plot(spectrum.x, spectrum.y, 'b', label=title)