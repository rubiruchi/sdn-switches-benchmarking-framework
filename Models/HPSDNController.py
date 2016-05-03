import logging

from Configurations import ControllerParameters
from Monitor.HPRestAPI import RequestFabric
from Monitor.HPRestAPI import RestAPIParser


class HPSDNController:
    def __init__(self,ip):
        self.controller_description = None
        if ControllerParameters.controllerList.__contains__(ip):
            self.controller_description = ControllerParameters.controllerList[ip]
        RequestFabric.getControllerAuthenticationToken(self.controller_description["user"], self.controller_description["password"])
        self.logger = logging.getLogger("Monitor."+__name__)
        self.logger.setLevel(logging.DEBUG)
        if RequestFabric.token is not "":
            self.logger.debug("Authentication token: " + RequestFabric.token)
        else:
            self.logger.error("Failed obtaining authentication token.")

        self.NEXT_LAST_OCTET = 4
        self.LAST_OCTET = 1
        self.FOOL_FLOW_DST_IP = "10.0.3.3"
        self.FOOL_FLOW_SRC_IP = "10.0."
        self.FOOL_MAC_ADDRESS = 100000000000
        self.tcp_port = 1


    def addFlow(self,dpid,flow):
        RequestFabric.addFlow(dpid, flow)

    def deleteFlow(self, dpid, flow):
        RequestFabric.deleteFlow(dpid, flow)

    def getFlowsCountForAllTables(self, dpid):
        json_flows = RequestFabric.getDataPathFlows(dpid=dpid)
        flows_count = RestAPIParser.getDataPathFlowsCountForAllTables(json=json_flows)
        return flows_count

    def getTableFlowsCount(self, dpid, table_id):
        json_flows = RequestFabric.getDataPathFlowsForTable(dpid=dpid, table_id=table_id)
        flows_count = RestAPIParser.getDataPathFlowsCountForAllTables(json=json_flows)
        return flows_count


    def buildDeletingFlow(self,flow):
        if flow["flow"].__contains__("idle_timeout"):
            flow["flow"].__delitem__("idle_timeout")
        if flow["flow"].__contains__("instructions"):
            flow["flow"].__delitem__("instructions")
        if flow["flow"].__contains__("actions"):
            flow["flow"].__delitem__("actions")
        if flow["flow"].__contains__("flow_mod_cmd"):
            flow["flow"].__delitem__("flow_mod_cmd")
        return flow

    def buildDummyFlow(self,flow):
        if flow["flow"].__contains__("match"):
            match_fields = flow["flow"]["match"]
            for field in match_fields:
                if field.has_key("eth_src"):
                    field["eth_src"] = self.buildFakeMAC()
                if field.has_key("eth_dst"):
                    field["eth_dst"] = self.buildFakeMAC()
                if field.has_key("ipv4_src"):
                    field["ipv4_src"] = self.buildFakeIP()
                if field.has_key("ipv4_dst"):
                    field["ipv4_dst"] = self.buildFakeIP()
                if field.has_key("tcp_src"):
                    field["tcp_src"] = str(self.tcp_port)
                if field.has_key("tcp_dst"):
                    self.tcp_port+=1
                    field["tcp_dst"] = self.tcp_port
            flow["flow"]["match"] = match_fields
            return flow


    def buildFakeIP(self):
        self.LAST_OCTET += 1
        if self.LAST_OCTET == 256:
            self.LAST_OCTET = 1
            self.NEXT_LAST_OCTET += 1
            if self.NEXT_LAST_OCTET == 256:
                self.NEXT_LAST_OCTET = 4
        return self.FOOL_FLOW_SRC_IP+str(self.NEXT_LAST_OCTET)+"."+str(self.LAST_OCTET)

    def buildFakeMAC(self):
        self.FOOL_MAC_ADDRESS+=1
        return str(self.FOOL_MAC_ADDRESS)






