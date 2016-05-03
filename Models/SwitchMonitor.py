import logging
import threading
import time

from Monitor.CLIStubs.SwitchSmallCLI import SwitchSmallCLI

from Monitor.Configurations import SwitchParameters
from Monitor.CLIStubs.SwitchBigCLI import SwitchBigCLI


class SwitchMonitor(threading.Thread):
    def __init__(self, dpid):
        threading.Thread.__init__(self)
        self.switch_description = None
        if SwitchParameters.datapathList.__contains__(dpid):
            self.switch_description = SwitchParameters.datapathList[dpid]
        self.logger = logging.getLogger("Monitor."+__name__)
        self.logger.setLevel(logging.DEBUG)
        if self.switch_description["model"] is "2920":
            self.cli = SwitchSmallCLI(self.switch_description)
        elif self.switch_description["model"] is "3500":
            self.cli = SwitchSmallCLI(self.switch_description)
        elif self.switch_description["model"] is "5700":
            self.cli = SwitchBigCLI(self.switch_description)
        elif self.switch_description["model"] is "5130":
            self.cli = SwitchBigCLI(self.switch_description)
        self.currentCPU = 0
        self.software_flows_count = 0
        self.hardware_flows_count = 0
        self.hardware_tables = {}
        self.software_tables = {}
        for id in self.switch_description["software_tables"]:
            self.hardware_tables[id] = []
        for id in self.switch_description["hardware_tables"]:
            self.hardware_tables[id] = []




    def addFlow(self,flow):
        table_id = str(flow["flow"]["table_id"])
        if self.hardware_tables.has_key(table_id):
            self.hardware_tables[table_id].append(flow)
            return
        if self.software_tables.has_key(table_id):
            self.software_tables[table_id].append(flow)
            return

    def removeFlow(self,flow):
        table_id = str(flow["flow"]["table_id"])
        if self.hardware_tables.has_key(table_id):
            self.hardware_tables[table_id].remove(flow)
            return
        if self.software_tables.has_key(table_id):
            self.software_tables[table_id].remove(flow)
            return

    def printHardwareTables(self):
        for table in self.hardware_tables:
            print table

    def printSoftwareTables(self):
        for table in self.software_tables:
            print table




    def run(self):
        for i in  range(0,2,1):
            self.hardware_flows_count, self.software_flows_count = self.cli.getFlowsCountOverCLI()
            self.currentCPU = self.cli.updateCPU()
            self.logger.info("HW="+str(self.hardware_flows_count)+" SF="+str(self.software_flows_count)+" CPU="+str(self.currentCPU))
            time.sleep(2)



    def getCurrentCPU(self):
        self.currentCPU = self.cli.updateCPU()
        return self.currentCPU

    def getSoftwareFlowsCount(self):
        self.hardware_flows_count, self.software_flows_count = self.cli.getFlowsCountOverCLI()
        return self.software_flows_count

    def getHardwareFlowsCount(self):
        self.hardware_flows_count, self.software_flows_count = self.cli.getFlowsCountOverCLI()
        return self.hardware_flows_count

    def getDPID(self):
        return self.switch_description["dpid"]

    def getSwitchModel(self):
        return self.switch_description["model"]