
import random
import copy

LINKCHANGES = 1

TRACE = 1;             
YES = 1
NO = 0

evlist = []   
clocktime = 0.000


class Rtpkt:


    def __init__(self, srcid, destid, mincost):
        self.sourceid = srcid
        self.destid = destid
        self.mincost = mincost[:4]

    def __repr__(self):
        return (#'Packet Object:\n'
                '    Source ID: %s\n'
                '    Destination ID: %s\n'
                '    Cost: %s\n' % (self.sourceid, self.destid, self.mincost))

class Event:

    def __init__(self, evtime=None, evtype=None, eventity=None, rtpktptr=None):
        self.evtime = evtime
        self.evtype = evtype
        self.eventity = eventity
        self.rtpktptr = rtpktptr

    def __repr__(self):
        return ('Event Object:\n'
                '  Time: %s\n'
                '  Type: %s\n'
                '  Entity: %s\n'
                '  Packet: \n%s\n' % (self.evtime, self.evtype,
                                      self.eventity, self.rtpktptr))

FROM_LAYER2 = 2
LINK_CHANGE = 10




def insertevent(p):

    if TRACE > 3:
        print("            INSERTEVENT: time is %lf\n" % clocktime)
        print("            INSERTEVENT: future time will be %lf\n" % p.evtime)

    evlist.append(p)
    evlist.sort(key=lambda e: e.evtime)

def printevlist():
    print("--------------\nEvent List Follows:\n")
    for event in evlist:
        print("Event time: %f, type: %d entity: %d\n" % (event.evtime, event.evtype, event.eventity))
    print("--------------\n")


def tolayer2(packet):
    connectcosts = [[0 for j in range(4)] for i in range(4)]

    connectcosts[0][0]=0 
    connectcosts[0][1]=1 
    connectcosts[0][2]=3
    connectcosts[0][3]=7
    connectcosts[1][0]=1 
    connectcosts[1][1]=0 
    connectcosts[1][2]=1
    connectcosts[1][3]=999
    connectcosts[2][0]=3 
    connectcosts[2][1]=1 
    connectcosts[2][2]=0
    connectcosts[2][3]=2
    connectcosts[3][0]=7 
    connectcosts[3][1]=999
    connectcosts[3][2]=2
    connectcosts[3][3]=0

    if (packet.sourceid < 0) or (packet.sourceid > 3):
        print("WARNING: illegal source id in your packet, ignoring packet!\n")
        return
    if (packet.destid < 0) or (packet.destid > 3):
        print("WARNING: illegal dest id in your packet, ignoring packet!\n")
        return
    if (packet.sourceid == packet.destid):
        print("WARNING: source and destination id's the same, ignoring packet!\n")
        return
    if (connectcosts[packet.sourceid][packet.destid] == 999):
        print(packet)
        print("WARNING: source and destination not connected, ignoring packet!\n")
        return

    mypktptr = copy.deepcopy(packet)
    if TRACE > 2:
        print("    TOLAYER2: source: %d, dest: %d\n              costs:" %
              (mypktptr.sourceid, mypktptr.destid))
        for i in range(4):
            print("%d  " % (mypktptr.mincost[i]))
        print("\n")

    evptr = Event(evtype=FROM_LAYER2, eventity=packet.destid, rtpktptr=mypktptr)


    lastime = clocktime
    for q in evlist:
        if ( (q.evtype == FROM_LAYER2)  and (q.eventity == evptr.eventity) ):
            lastime = q.evtime
    evptr.evtime =  lastime + 2. * random.uniform(0, 1)


    if TRACE > 2:
        print("    TOLAYER2: scheduling arrival on other side\n")
    insertevent(evptr)
