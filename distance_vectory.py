

import random

from utils import LINKCHANGES, TRACE, YES, NO, FROM_LAYER2, LINK_CHANGE, Rtpkt, Event, evlist, clocktime, insertevent
from node0 import rtinit0, rtupdate0, rtlinkhandler0
from node1 import rtinit1, rtupdate1, rtlinkhandler1
from node2 import rtinit2, rtupdate2
from node3 import rtinit3, rtupdate3



import utils

def main():
    init()
    
    while evlist:
        event = evlist.pop(0)
        if TRACE > 1:
            print("MAIN: rcv event, t=%.3f, at %d" % (event.evtime, event.eventity))
            if event.evtype == FROM_LAYER2:
                print(" src:%2d," % event.rtpktptr.sourceid)
                print(" dest:%2d," % event.rtpktptr.destid)
                print(" contents: %3d %3d %3d %3d\n" %
                      (event.rtpktptr.mincost[0], event.rtpktptr.mincost[1],
                       event.rtpktptr.mincost[2], event.rtpktptr.mincost[3]))
        utils.clocktime = event.evtime;   

        if event.evtype == FROM_LAYER2:
            if event.eventity == 0:
                rtupdate0(event.rtpktptr)
            elif event.eventity == 1:
                rtupdate1(event.rtpktptr)
            elif event.eventity == 2:
                rtupdate2(event.rtpktptr)
            elif event.eventity == 3:
                rtupdate3(event.rtpktptr)
            else:
                print("Panic: unknown event entity\n")
                exit(0)
        elif event.evtype == LINK_CHANGE:
            if (utils.clocktime<10001.0):
                rtlinkhandler0(1,20)
                rtlinkhandler1(0,20)
            else:
                rtlinkhandler0(1,1)
                rtlinkhandler1(0,1)
        else:
            print("Panic: unknown event type\n")
            exit(0)

        if event.evtype == FROM_LAYER2:
            del event.rtpktptr      
        del event                  


    print("\nSimulator terminated at t=%f, no packets in medium\n" % utils.clocktime)



def init():

    global TRACE

    TRACE = int(input("Enter TRACE:"))

    random.seed(9999)            
    utils.clocktime = 0.0               
    rtinit0()
    rtinit1()
    rtinit2()
    rtinit3()

    # initialize future link changesuti
    if LINKCHANGES == 1:
        event = Event(evtime=10000.0,
                      evtype=LINK_CHANGE,
                      eventity=-1,
                      rtpktptr=None)
        insertevent(event)
        event = Event(evtime=20000.0,
                      evtype=LINK_CHANGE,
                      eventity=-1,
                      rtpktptr=None)
        insertevent(event)

if __name__ == '__main__':
    main()
