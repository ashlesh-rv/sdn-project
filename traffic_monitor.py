from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
from pox.lib.recoco import Timer

log = core.getLogger()

def request_stats():
    for connection in core.openflow._connections.values():
        connection.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))

def _handle_ConnectionUp(event):
    log.info("Switch %s connected", dpidToStr(event.dpid))
    Timer(5, request_stats, recurring=True)

def _handle_FlowStatsReceived(event):
    log.info("Traffic Stats:")
    for stat in event.stats:
        log.info("Packets=%s Bytes=%s", stat.packet_count, stat.byte_count)

        with open("report.txt", "a") as f:
            f.write(f"Packets={stat.packet_count}, Bytes={stat.byte_count}\n")

def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("FlowStatsReceived", _handle_FlowStatsReceived)
