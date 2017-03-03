# This sets data into a data list, and retrieves the data after every entry depending on the model sampling rate.
from config import *
print("in File threadTest1")
if __name__ == '__main__':
    print("running file ThreadTest1")

    #Creates a list for storing the data acquired by the dirset thread
    #it is a list of tuples, each index being the division of the samples/sec for when the
    #dat was acquired.
    dataStruc1 = acquisitioncontrol.DataList(1);    #Create Data List for Group 1

    #Creates a thread object for starting acquisiton on Group 1 of the selected project and model at an interval which is
    # 1 times sample/sec of model( same as model sample/sec). Interval cannot be lower than the model sample/sec
    dirset = acquisitioncontrol.StartAcquisitionThread('ephasorex2','phasor01_IEEE39',dataStruc1,1,"AcqThread Set",1)

    #creates a thread object for returning the last value that was acquired.  Again, the interval must be greater than or equal
    # to the model samples/sec. 1 means it is the same as the sample/sec of the model.
    dirret = acquisitioncontrol.acquisitionThreadReturn('ephasorex2','phasor01_IEEE39',dataStruc1,1,"AcqThread Return",1)

    #This allows for setting the interval for acquisition. In this case, the thread checks every 5 seconds for the last data
    #added to the list.
    dirsetTime = acquisitioncontrol.acquisitionThreadReturnWithTime('ephasorex2','phasor01_IEEE39',dataStruc1,1,"AcqThread Return",5)

    #Starts both threads
    dirset.start()
    dirret.start()

    #No need to join it seems. After testing all cases, the joining halts a thread until the main thread is killed, so it doesn't end.
    #They can be set to setDaemon(True) to kill the thread automatically when main ends, but I've read that
    # this isn't always the case.

    #if you want to make other API calls, you must acquire.connectToModel(project,model) from the main thread as well
    #Then You can print out things like the control signals,    signalcontrol.showControlSignals()   and other
    #functions in the signals and parameters modules.