import logging

from Configurations import SwitchParameters
from ExternalTools.DelayThread import DelayMonitor
from ExternalTools.IperfThread import BandwidthMeter
from Models.HPSDNController import HPSDNController
from Models.SwitchMonitor import SwitchMonitor
from datetime import datetime
import time
import threading



class TestingScenario5700:
    def __init__(self):
        self.logger = logging.getLogger("Monitor.TestScenario")
        self.logger.setLevel(logging.DEBUG)
        self.switch5700 = SwitchMonitor("00:00:00:00:00:00:00:16")
        self.controller = HPSDNController("10.1.3.16")
        self.Iperf5700 = BandwidthMeter("10.1.3.17", "marian", "descartes",
                                   "10.1.3.11", "marian", "descartes",
                                   'iperf -c 10.100.3.17 -i 1 -y C', 'iperf -s')
        self.Iperf5700.setTestDuraton(10000)
        self.Ping5700 = DelayMonitor("10.1.3.11", "marian", "descartes", "10.100.3.17", 1000)
        self.Ping5700.setPingCount(10000)

    def start(self):
        self.switch5700.cli.enableExtensibilityTable()
        print "=================== Test 1:Measuring Hardware Processing Performance =========================="
        self.hardwareProcessingPerformance()
        print "==============================================================================================="
        print "=================== Test 2:Measuring Rules Insertion Performance =============================="
        flow = SwitchParameters.switch5700_rule_10
        self.measureRuleInsertionPerformance(flow,20,20)
        print "==============================================================================================="
        # print "=================== Test 3:Measuring Max Rule Count ==========================================="
        # self.measureTableSizeForDifferentRules()
        # print "==============================================================================================="
        print "=================== Test 4:Flow Pull Performance =============================="
        flow = SwitchParameters.switch5700_rule_10
        self.measureGetFlowsImpact(flow,20,512)
        print "==============================================================================================="
        self.switch5700.cli.enableMacIPTable()
        print "=================== Test 1:Measuring Hardware Processing Performance =========================="
        self.hardwareProcessingPerformance()
        print "==============================================================================================="
        print "=================== Test 2:Measuring Rules Insertion Performance =============================="
        flow = SwitchParameters.switch5700_mac_ip_rule
        self.measureRuleInsertionPerformance(flow,10,1000)
        print "==============================================================================================="
        print "=================== Test 3:Flow Pull Performance =============================="
        flow = SwitchParameters.switch5700_mac_ip_rule
        self.measureGetFlowsImpact(flow,10,1000)
        print "==============================================================================================="




    def installPingRules(self):
        flow1 = SwitchParameters.testbed_ping_rule_1
        flow2 = SwitchParameters.testbed_ping_rule_2
        flow1["flow"]["table_id"]=20
        flow2["flow"]["table_id"]=20
        self.controller.addFlow(self.switch5700.getDPID(),flow1)
        self.controller.addFlow(self.switch5700.getDPID(),flow2)


#=========================================  Hardware Processing Perfoemance performance =========================
    def hardwareProcessingPerformance(self):
        self.switch5700.cli.resetOpenflowInstance()
        self.installPingRules()
        p1 = self.Iperf5700.startCapturingThroughput(20)
        p2 = self.Ping5700.startCapturingDelay(30)
        p1.join()
        p2.join()
        #@time.sleep(20)
        #self.Iperf5700.stopCapturingThroughput()
        #self.Ping5700.stopCapturingDelay()
        #time.sleep(15)

#=========================================  Rule insetion performance =========================
    def measureRuleInsertionPerformance(self,flow,table_id,max_rule_count):
        cpus = {}
        flow_insertion_delays = {}
        flow_insertion_moments = {}
        flow = flow
        flow["flow"]["table_id"]=table_id
        self.switch5700.cli.resetOpenflowInstance()
        self.installPingRules()
        self.Iperf5700.startCapturingThroughput(180)
        self.Ping5700.startCapturingDelay(180)
        rules_count = self.switch5700.getHardwareFlowsCount()
        start_time = datetime.now()
        while rules_count<max_rule_count:
            print "\r Rules = {0}".format(rules_count),
            flow = self.controller.buildDummyFlow(flow)
            flow["flow"]["priority"]=rules_count+1
            a = datetime.now()
            self.controller.addFlow(self.switch5700.getDPID(),flow)
            b = datetime.now()
            c = (b-a).microseconds
            flow_insertion_delays[rules_count]= c
            flow_insertion_moments[rules_count]= c
            if(rules_count%10)==0:
                cpus[rules_count]= self.switch5700.getCurrentCPU()
            else:
                cpus[rules_count]= 0
            rules_count+=1
        print
        end_time = datetime.now()
        duration = end_time - start_time
        self.Iperf5700.stopCapturingThroughput()
        self.Ping5700.stopCapturingDelay()
        time.sleep(5)
        print "Experiment duration = "+str(duration)
        f = open("5700_RuleInsertionPerformance_"+str(table_id)+".txt","w")
        f.write("Rule\tMoment\tDelay\tCPU\n")
        for key in flow_insertion_moments.keys():
            f.write(str(key)+"\t"+
                    str(flow_insertion_moments[key])+"\t"+
                    str(flow_insertion_delays[key])+"\t"+
                    str(cpus[key])+"\t\n")


#=========================================  MAX TABLE SIZES =========================
    def measureTableSizeForDifferentRules(self):
        table_id = 20
        for flow in SwitchParameters.switch_compatible_rules["5700_NORMAL"]:
            self.switch5700.cli.resetOpenflowInstance()
            flow["flow"]["table_id"]=table_id
            self.measureMaxRuleCountInHardware(flow)
        print "========================================================="

    def measureMaxRuleCountInHardware(self,flow):
        print "Flow Pattern:", flow
        print "Number of wildcards: ",int(13-len(flow["flow"]["match"]))
        hw_table_size = self.switch5700.getHardwareFlowsCount()
        while True:
            print "\r Rules = {0}".format(hw_table_size),
            for i in range(0,100,1):
                flow["flow"]["priority"]=hw_table_size+i
                flow = self.controller.buildDummyFlow(flow)
                self.controller.addFlow(self.switch5700.getDPID(),flow)
            current_count = self.switch5700.getHardwareFlowsCount()
            if hw_table_size==current_count:
                break
            hw_table_size = current_count
        print
        print "Rules number limit = ",str(hw_table_size)

#=========================================================================================
    #mac-ip aware enabled
    def measureGetFlowsImpact(self, flow, table_id, max_table_size):
        self.switch5700.cli.resetOpenflowInstance()
        #self.installPingRules()
        self.Iperf5700.startCapturingThroughput(180)
        self.Ping5700.startCapturingDelay(180)
        time.sleep(5)
        flow = flow
        flow["flow"]["table_id"] = table_id
        rules_count = self.switch5700.getHardwareFlowsCount()
        while rules_count<=max_table_size:
            flow = self.controller.buildDummyFlow(flow)
            flow["flow"]["priority"]=rules_count+1
            self.controller.addFlow(self.switch5700.getDPID(),flow)
            if(rules_count%10)==0:
                for i in range(0,10,1):
                    print self.controller.getTableFlowsCount(self.switch5700.getDPID(),table_id)
            rules_count+=1
        time.sleep(5)
        self.Iperf5700.stopCapturingThroughput()
        self.Ping5700.stopCapturingDelay()













def main():
    test = TestingScenario5700()
    test.start()


if __name__ == '__main__':
    main()