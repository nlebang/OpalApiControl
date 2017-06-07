"""
VarIDX and VARVGS for LTB PSAT Formatted Data Streaming from ePhasorsim Running Models

"""

import OpalApiPy
from dime import dime
import acquisitioncontrol
from OpalApiControl.system import acquire
from OpalApiControl.OpalAPIFormatting import psse32
import varreqs
import logging
import time
from time import sleep


Bus_Data = acquisitioncontrol.DataList(1)
BusIDX = {}
busvolt = []
busang = []
Syn_Data = acquisitioncontrol.DataList(2)
SynIDX = {}
synang = []
synspeed = []
syne1d = []
syne1q = []
syne2d = []
syne2q = []
synpsid = []
synpsiq = []
synact = []
synreact = []
ExcIDX = {}
excVref = []
excVmag = []

Load_Data = acquisitioncontrol.DataList(3)
VarStore = {}
Varvgs = {}
global dimec
global start_time
global bus_set

def stream_data(groups):
    """Creates Bus,Generator, and Load Data Structure as well as the acquisition threads for dynamic streaming. Threads run
     until the model is paused, then must be run again if further acquisition is required.  Data Lists will be appended to
     granted the Bus_Data, etc, if this module is imported

     groups = (group# tuple, in ascending order)"""
    if 1 in groups:
        bus_set = acquisitioncontrol.StartAcquisitionThread('ephasorFormat1', 'phasor01_IEEE39', Bus_Data, groups[0],
                                                       "Bus Data Thread Set", 0.33)
    if 2 in groups:
        syn_set = acquisitioncontrol.StartAcquisitionThread('ephasorFormat1', 'phasor01_IEEE39', Syn_Data, groups[1],
                                                       "Generator Data Thread Set", 0.33)
    if 3 in groups:
        load_set = acquisitioncontrol.StartAcquisitionThread('ephasorFormat1', 'phasor01_IEEE39', Load_Data, groups[2],
                                                       "Load Data Thread Set", 0.33)
    if 4 in groups:
        line_set = acquisitioncontrol.StartAcquisitionThread('ephasorFormat1', 'phasor01_IEEE39', Load_Data, groups[3],
                                                         "Load Data Thread Set", 0.33)
    if 1 in groups:
        bus_set.start()
    if 2 in groups:
        syn_set.start()
    if 3 in groups:
        load_set.start()
    #if 4 in groups:
    #    line_set.start()
    acquire.connectToModel('ephasorFormat1','phasor01_IEEE39')
    OpalApiPy.SetAcqBlockLastVal(0, 1)
    start_time = bus_set.simulationTime


def set_dime_connect(dev, port):
    """Enter module name to connect, along with the port established by dime connection."""

    #try:
    dimec = dime.Dime(dev, port)
    #dimec.cleanup()
    dimec.start()
    sleep(0.1)
    #except:
    #    logging.warning('<dime connection not established>')
    #else:
    #    logging.log('<dime connection established>')


def acq_data():
    """Constructs acquisition list for data server. Slight re-ordering is done for Bus P and Q(Must append Syn,Load P and Q)"""
    All_Acq_Data = []
    All_Acq_Data.extend(Bus_Data.returnLastAcq())
    All_Acq_Data.append(psse32.freq)
    All_Acq_Data.extend(Load_Data.returnLastAcq())
    All_Acq_Data.extend(Syn_Data.returnLastAcq())


    return All_Acq_Data

def ltb_stream():
    """Sends requested data indices for devices to the LTB server using dime"""

    if len(varreqs.Vgsinfo['dev_list']) == 0:
        logging.warning('<No Devices Requesting>')
        return

    else:
        acq_time = time.time()
        for dev in varreqs.Vgsinfo['dev_list']:
            idx = varreqs.Vgsinfo[dev]['var_idx']
            var_data = acq_data()
            Varvgs['vars'] = var_data[idx[0]:len(idx)-1]            #Need to add modified data
            Varvgs['accurate'] = var_data[idx[0]:len(idx)-1]        #Accurate streaming data
            Varvgs['t'] = bus_set.simulationTime-start_time
            print('Time', Varvgs['t'])
            Varvgs['k'] = bus_set.simulationTime/30
            print('Steps', Varvgs['k'])
            dimec.send_var(dev, 'Varvgs')
