from pox.core import core
import pox.openflow.libopenflow_01 as of #communicate with switch
from pox.lib.util import dpidToStr   #converts switch into readable form
from pox.lib.recoco import Timer    #run a function again and again

log = core.getLogger()  #prints 

def request_stats():               #asks switch for data
    for connection in core.openflow._connections.values():
        connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request())) #sends request to switch

def _handle_ConnectionUp(event):  #switch connects to controller
    log.info("Switch %s connected", dpidToStr(event.dpid))
    Timer(5, request_stats, recurring=True)

def _handle_FlowStatsReceived(event):  #runs when switch sends data
    log.info("Traffic Stats:")
    for stat in event.stats:
        log.info("Packets=%s Bytes=%s", stat.packet_count, stat.byte_count)  #displays 

        with open("report.txt", "a") as f:
            f.write(f"Packets={stat.packet_count}, Bytes={stat.byte_count}\n")

def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("FlowStatsReceived", _handle_FlowStatsReceived)
