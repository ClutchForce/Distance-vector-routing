from utils import TRACE, YES, NO, Rtpkt, tolayer2
import utils
class DistanceTable:
    costs = [[0 for j in range(4)] for i in range(4)]

dt = DistanceTable()
edges = [7, 999, 2, 0]
node_id = 3
is_processing = False
packet_queue = []

def rtinit3():
    global dt, edges, is_processing
    is_processing = False
    print("rtinit3 is called at time t=%.3f" % utils.clocktime)
    
    for i in range(4):
        for j in range(4):
            if i == j:
                dt.costs[i][j] = edges[i]
            else:
                dt.costs[i][j] = 999  
    printdt3(dt)
    send_to_neighbors()

def rtupdate3(rcvdpkt):
    global dt, is_processing, packet_queue

    if is_processing:
        packet_queue.append(rcvdpkt)
        return

    is_processing = True
    print("rtupdate3 is called at time t=%.3f as node %d sent a packet with [%d %d %d %d]" % (
        utils.clocktime, rcvdpkt.sourceid, rcvdpkt.mincost[0], rcvdpkt.mincost[1], rcvdpkt.mincost[2], rcvdpkt.mincost[3]))
    
    updated = False
    src = rcvdpkt.sourceid

    for i in range(4):
        possible_cost = dt.costs[src][src] + rcvdpkt.mincost[i]
        if possible_cost < 999:
            dt.costs[i][src] = possible_cost

        else:
            dt.costs[i][src] = 999
    printdt3(dt)

    old_edges = list(edges)
    for j in range(4):
        edges[j] = min(dt.costs[j])
    if old_edges != edges:
        send_to_neighbors()
    else:
        print("Minimum cost didn't change. No new packets are sent")

    is_processing = False
    process_packet_queue()


def send_to_neighbors():
    global dt, node_id, edges

    mincost = [0] * 4
    for i in range(4):
        mincost[i] = min(dt.costs[i])

    
    for dest in range(4):
        if dest == node_id or edges[dest] == 999: 
            continue
        pkt = Rtpkt(srcid=node_id, destid=dest, mincost=mincost)
        tolayer2(pkt)
        print("At time t=%.3f, node %d sends packet to node %d with: [%d %d %d %d]" %
                (utils.clocktime, pkt.sourceid, pkt.destid, pkt.mincost[0], pkt.mincost[1], pkt.mincost[2], pkt.mincost[3]))
        process_packet_queue()

def printdt3(dtptr):
    print("             via     \n")
    print("   D3 |    0     2 \n")
    print("  ----|-----------\n")
    print("     0|  %3d   %3d\n" % (dtptr.costs[0][0], dtptr.costs[0][2]))
    print("dest 1|  %3d   %3d\n" % (dtptr.costs[1][0], dtptr.costs[1][2]))
    print("     2|  %3d   %3d\n" % (dtptr.costs[2][0], dtptr.costs[2][2]))

def process_packet_queue():
    global packet_queue, is_processing

    while packet_queue and not is_processing:
        pkt_to_process = packet_queue.pop(0)
        rtupdate3(pkt_to_process)
