"""
D-Tacq ACQ2106 with ACQ435 Digitizers (up to 6)  real time streaming support.

This code does some kind of QA test of the different sample rates that the ACQ can run.
For each SR, starting at 4KHz to 16KHz, a consecutive series of shots at each freq. is done.
The trigger is hardware, done by connecting to the Func. Generator using it's REST API.

"""

import MDSplus
import time
import sys

def main(argv):
    timesleep = 60 #secs
    tree = MDSplus.Tree('daqtest', -1)
    node = tree.ACQ_194.NODE.data()

    print("Open daqtest tree {} {}".format(tree, node))
    tree    = MDSplus.Tree('daqtest', -1)

    time.sleep(1)
    shot = int(sys.argv[1])
    print("Shot # {}".format(shot))
    tree.setCurrent(shot)
    tree.createPulse(0)
    tree = MDSplus.Tree('daqtest', 0)

    tree.ACQ_194.init()

    for remaining in range(timesleep, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write("\n\rShot Complete!\n")

    tree.ACQ_194.stop()
    tree.close()
    time.sleep(5)


if __name__ == "__main__":
   main(sys.argv[1:])