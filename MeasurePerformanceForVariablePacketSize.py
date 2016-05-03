import logging

from Configurations import SwitchParameters
from ExternalTools.DelayThread import DelayMonitor
from ExternalTools.IperfThread import BandwidthMeter
from Models.HPSDNController import HPSDNController
from Models.SwitchMonitor import SwitchMonitor
from datetime import datetime
import time
import threading



class MeasurePerformanceForVariablePacketSize:
    def __init__(self):
        self.logger = logging.getLogger("Monitor.TestScenario")
        self.logger.setLevel(logging.DEBUG)
        self.controller = HPSDNController("10.1.3.16")
        self.Iperf = BandwidthMeter("10.1.3.17", "marian", "descartes",
                                   "10.1.3.11", "marian", "descartes",
                                   'iperf -c 10.100.3.17 -i 1 -y C', 'iperf -s')
        self.Iperf.setTestDuraton(10000)
        self.Ping = DelayMonitor("10.1.3.11", "marian", "descartes", "10.100.3.17", 1000)
        self.Ping.setPingCount(10000)

    def start(self):
        # NO OpenFlow Pipeline
        self.measurePerformanceForVariablePacketSize("5130_PerformanceForVariablePacketSize_NoOpenFlow.txt")
        #self.measureSwitch5130()


    def measureSwitch5130(self):
        self.switch5130 = SwitchMonitor("00:00:00:00:00:00:00:42")
        print "=================== Switch5130: Extensibility Table =========================="
        self.switch5130.cli.enableExtensibilityTable()
        self.measurePerformanceForVariablePacketSize("5130_PerformanceForVariablePacketSize_20.txt")
        print "=============================================================================="
        print "=================== Switch5130: MAC-IP Table =========================="
        self.switch5130.cli.enableMacIPTable()
        self.measurePerformanceForVariablePacketSize("5130_PerformanceForVariablePacketSize_10.txt")
        print "=============================================================================="



    def measurePerformanceForVariablePacketSize(self,filename="X_PerformanceForVariablePacketSize.txt"):
        f = open(filename,"w")
        s = "Packet Size\tThroughput\tDelay\n"
        f.write(s)
        print s
        for size in range(60,1520,20):
            self.Iperf.setClientCommand('iperf -c 10.100.3.17 -i 1 -y C -M '+str(size))
            self.hardwareProcessingPerformance(20)
            throughput_values,delay_values = self.processIperfAndPingOutput()
            avarage_throughput = self.calculateAvarage(throughput_values)
            avarage_delay = self.calculateAvarage(delay_values)
            s = str(size)+"\t"+str(avarage_throughput)+"\t"+str(avarage_delay)+"\t\n"
            print s,
            f.write(s)
        f.close()





    #USED TO INSTALL FLOWS IN DIFFERENT TABLES
    def installPingRules(self, switch, flow1, flow2, table_id=20, priority=0):
        flow1 = SwitchParameters.testbed_ping_rule_1_OF10
        flow2 = SwitchParameters.testbed_ping_rule_2_OF10
        flow1["flow"]["table_id"]=table_id
        flow2["flow"]["table_id"]=table_id
        flow1["flow"]["priority"]=priority
        flow2["flow"]["priority"]=priority
        for i in range(0,5,1):
            self.controller.addFlow(switch.getDPID(),flow1)
            self.controller.addFlow(switch.getDPID(),flow2)


#=========================================  Hardware Processing Perfoemance performance =========================
    def hardwareProcessingPerformance(self,duration):
        self.Iperf.startCapturingThroughput()
        self.Ping.startCapturingDelay()
        time.sleep(duration)
        self.Iperf.stopCapturingThroughput()
        self.Ping.stopCapturingDelay()


    def processIperfAndPingOutput(self):
        while self.Iperf.finished==False:
            time.sleep(1)
        while self.Ping.finished==False:
            time.sleep(1)
        throughput_values = self.Iperf.values
        delay_values = self.Ping.values
        if len(throughput_values)<len(delay_values):
            l = len(throughput_values)
        else:
            l = len(delay_values)
        # Since IPERF and Ping are not synchronized, output arrays have differnt lengths
        throughput_values = throughput_values[0:l]
        delay_values = delay_values[0:l]
        return throughput_values,delay_values

    def calculateAvarage(self,array):
        if len(array)==0:
            return 0
        sum = float(0)
        for i in array:
            sum+=int(i)
        return float(sum/len(array))






def main():
    test = MeasurePerformanceForVariablePacketSize()
    test.start()


if __name__ == '__main__':
    main()