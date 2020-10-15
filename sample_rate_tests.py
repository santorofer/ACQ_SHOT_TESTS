"""
D-Tacq ACQ2106 with ACQ435 Digitizers (up to 6)  real time streaming support.

This code does some kind of QA test of the different sample rates that the ACQ can run.
For each SR, starting at 4KHz to 16KHz, a consecutive series of shots at each freq. is done.
The trigger is hardware, done by connecting to the Func. Generator using it's REST API.

"""

import MDSplus
import time
import sys
import requests

#Func. Generator:
target   = 'http://172.20.240.19/Include/WebControlMethod.asp'
#Pressing the trigger button is done using the following load:
pay_load = 'queryID=1&queryMode=SetKey&queryInput=Trigger'

timesleep = 60 #secs
tree = MDSplus.Tree('daqtest', -1)
node = tree.ACQ2106_4353.NODE.data()

print("Open daqtest tree {}".format(tree))
print("TRIG_MODE {}".format(str(tree.ACQ2106_4353.TRIG_MODE.data())))

f_4000  = [4000 for i in range(10)]
f_5000  = [5000 for i in range(10)]
f_6000  = [6000 for i in range(10)]
f_8000  = [8000 for i in range(10)]
f_10000 = [10000 for i in range(10)]
f_12000 = [12000 for i in range(10)]
f_16000 = [16000 for i in range(10)]

# freq_list = [4000, 5000, 6000, 7000, 8000, 9000, 10000, 16000]
# freq_lists = [f_5000, f_6000, f_8000, f_10000, f_12000, f_16000]
freq_lists = [f_8000]
shotcount = 0

import acq400_hapi
uut = acq400_hapi.Acq400(node, monitor=False)
print("ACQ set abort...")
uut.s0.set_abort = 1
time.sleep(5)

for idenx, frequencies in enumerate(freq_lists):
    for iterate, item in enumerate(frequencies):
        tree    = MDSplus.Tree('daqtest', -1)

        tree.ACQ2106_4353.FREQ.record = int(item)
        tree.ACQ2106_4353.SEG_LENGTH.record = int(item * 5)
        print("SR = {}".format(int(tree.ACQ2106_4353.FREQ.data())))
        time.sleep(1)

        shotcount += 1
        shot = int(tree.ACQ2106_4353.FREQ.data()) + shotcount

        print("Shot Number {}".format(shot))
        tree.setCurrent(shot)
        tree.createPulse(0)
        tree = MDSplus.Tree('daqtest', 0)

        tree.ACQ2106_4353.init()

        time.sleep(10)
        response = requests.post(target, pay_load)
        print("FG trigger button was pressed {}".format(response))

        for remaining in range(timesleep, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("{:2d} seconds remaining.".format(remaining))
            sys.stdout.flush()
            time.sleep(1)

        sys.stdout.write("\rShot Complete!\n")
        
        tree.ACQ2106_4353.stop()
        tree.close()
        time.sleep(10)
