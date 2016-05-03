import logging

from Configurations import SwitchParameters
from ExternalTools.DelayThread import DelayMonitor
from ExternalTools.IperfThread import BandwidthMeter
from Models.HPSDNController import HPSDNController
from Models.SwitchMonitor import SwitchMonitor
from datetime import datetime
import time
import threading



class TestingScenario3500:
    def __init__(self):
        self.logger = logging.getLogger("Monitor.TestScenario")
        self.logger.setLevel(logging.DEBUG)
        self.switch2920 = SwitchMonitor("00:64:38:63:bb:58:eb:00")
        self.controller = HPSDNController("10.1.3.16")
        #self.Iperf = BandwidthMeter("10.1.3.17", "marian", "descartes",
        #                           "10.1.3.11", "marian", "descartes",
        #                           'iperf -c 10.100.3.17 -i 1 -y C', 'iperf -s')
        #self.Iperf.setTestDuraton(10000)
        #self.Ping = DelayMonitor("10.1.3.11", "marian", "descartes", "10.100.3.17", 1000)
        #self.Ping.setPingCount(10000)

    def start(self):
        # print "=================== Test 1:Measuring Hardware Processing Performance =========================="
        # self.hardwareProcessingPerformance()
        # print "==============================================================================================="
        # print "=================== Test 2:Measuring Rules Insertion Performance =============================="
        # flow = SwitchParameters.switch3500_rule_9_OF10
        # self.measureRuleInsertionPerformance(flow,100,100)
        # print "==============================================================================================="
        #print "=================== Test 3:Measuring Max Rule Count ==========================================="
        #self.switch2920.cli.setPolicyEngineUsageLimit(10)
        #self.measureTableSizeForDifferentRules()
        #print "==============================================================================================="
        # print "=================== Test 4:Flow Pull Performance =============================="
        # flow = SwitchParameters.switch3500_rule_9_OF13
        # self.measureGetFlowsImpact(flow,100,512)
        # print "==============================================================================================="
        #In order to work only with SF table OF policy usage resource should equal 0
        print "=================== Test 5:OpenFlow Policy Engine dependency =============================="
        self.openflowPolicyEngineDependency()
        print "==============================================================================================="
        #self.switch3500.cli.setPolicyEngineUsageLimit(0)
        # print "=================== Test 1:Measuring Software Processing Performance =========================="
        # self.switch3500.cli.resetOpenflowInstance()
        # self.installPingRules(200)
        # self.softwareProcessingPerformance()
        # print "==============================================================================================="
        # print "=================== Test 2:Measuring Rules Insertion Performance =============================="
        # flow = SwitchParameters.switch3500_rule_9_OF13
        # self.measureRuleInsertionPerformance(flow,200,1000)
        # print "==============================================================================================="
        # print "=================== Test 3:Flow Pull Performance =============================="
        # flow = SwitchParameters.switch3500_rule_9_OF13
        # self.measureGetFlowsImpact(flow,10,200)
        # print "==============================================================================================="
        # print "=================== Test 4:PPS change =============================="
        # self.switch3500.cli.setPolicyEngineUsageLimit(100)
        # self.softwarePPSChange()
        # print "==============================================================================================="






    def installPingRules(self,table_id):
        flow1 = SwitchParameters.testbed_ping_rule_1
        flow2 = SwitchParameters.testbed_ping_rule_2
        flow1["flow"]["table_id"]=table_id
        flow2["flow"]["table_id"]=table_id
        self.controller.addFlow(self.switch3500.getDPID(),flow1)
        time.sleep(1)
        self.controller.addFlow(self.switch3500.getDPID(),flow2)


#=========================================  Hardware Processing Perfoemance performance =========================
    def hardwareProcessingPerformance(self):
        self.switch3500.cli.resetOpenflowInstance()
        self.installPingRules(100)
        p1 = self.Iperf.startCapturingThroughput()
        p2 = self.Ping.startCapturingDelay()
        time.sleep(15)
        self.Iperf.stopCapturingThroughput()
        self.Ping.stopCapturingDelay()
        time.sleep(5)

#=========================================  Software Processing Perfoemance performance =========================
    def softwareProcessingPerformance(self):
        cpus = []
        p1 = self.Iperf.startCapturingThroughput()
        p2 = self.Ping.startCapturingDelay()
        for i in range(0,15,1):
            time.sleep(1)
            cpus.append(self.switch3500.getCurrentCPU())
        self.Iperf.stopCapturingThroughput()
        self.Ping.stopCapturingDelay()
        time.sleep(5)
        print "[Switch3500-CPU] ",cpus


    def softwarePPSChange(self):
        for i in range(1000,10000,1000):
            self.switch3500.cli.setSoftwareFlowTableRateLimit(i)
            self.installSFPingRules(200)
            self.softwareProcessingPerformance()

    def installSFPingRules(self,table_id):
        flow1 = SwitchParameters.switch3500_ping_rule_1
        flow2 = SwitchParameters.switch3500_ping_rule_2
        flow1["flow"]["table_id"]=200
        flow2["flow"]["table_id"]=200
        while(self.switch3500.getSoftwareFlowsCount()<3):
            self.controller.addFlow(self.switch3500.getDPID(),flow1)
            self.controller.addFlow(self.switch3500.getDPID(),flow2)

#=========================================  Rule insetion performance =========================
    def measureRuleInsertionPerformance(self,flow,table_id,max_rule_count):
        cpus = {}
        flow_insertion_delays = {}
        flow_insertion_moments = {}
        flow = flow
        flow["flow"]["table_id"]=table_id
        self.switch3500.cli.resetOpenflowInstance()
        self.installPingRules(100)
        self.Iperf.startCapturingThroughput()
        self.Ping.startCapturingDelay()
        rules_count = self.switch3500.getHardwareFlowsCount()
        start_time = datetime.now()
        while rules_count<max_rule_count:
            print "\r Rules = {0}".format(rules_count),
            flow = self.controller.buildDummyFlow(flow)
            flow["flow"]["priority"]=rules_count+1
            a = datetime.now()
            self.controller.addFlow(self.switch3500.getDPID(),flow)
            b = datetime.now()
            c = (b-a).microseconds
            flow_insertion_delays[rules_count]= c
            flow_insertion_moments[rules_count]= c
            if(rules_count%10)==0:
                cpus[rules_count]= self.switch3500.getCurrentCPU()
            else:
                cpus[rules_count]= 0
            rules_count+=1
        print
        end_time = datetime.now()
        duration = end_time - start_time
        self.Iperf.stopCapturingThroughput()
        self.Ping.stopCapturingDelay()
        time.sleep(5)
        print "Experiment duration = "+str(duration)
        f = open("3500_RuleInsertionPerformance_"+str(table_id)+".txt","w")
        f.write("Rule\tMoment\tDelay\tCPU\n")
        for key in flow_insertion_moments.keys():
            f.write(str(key)+"\t"+
                    str(flow_insertion_moments[key])+"\t"+
                    str(flow_insertion_delays[key])+"\t"+
                    str(cpus[key])+"\t\n")
#=========================================  Policy Engine Dependencie =========================
    def openflowPolicyEngineDependency(self):
        results = {}
        table_id = 0
        flow = SwitchParameters.switch2920_rule_10
        flow["flow"]["table_id"]=table_id
        for i in range(100,105,5):
            self.switch2920.cli.setPolicyEngineUsageLimit(i)
            time.sleep(3)
            results[i]=self.measureMaxRuleCountInHardware(flow)
        for key in results.keys():
            print "\r",key,"\t",results[key]



#=========================================  MAX TABLE SIZES =========================
    def measureTableSizeForDifferentRules(self):
        table_id = 0
        for flow in SwitchParameters.switch_compatible_rules["2920"]:
            self.switch2920.cli.resetOpenflowInstance()
            time.sleep(3)
            flow["flow"]["table_id"]=table_id
            self.measureMaxRuleCountInHardware(flow)
        print "========================================================="

    def measureMaxRuleCountInHardware(self,flow):
        print "Flow Pattern:", flow
        print "Number of wildcards: ",int(13-len(flow["flow"]["match"]))
        hw_table_size = self.switch2920.getHardwareFlowsCount()
        while True:
            print "\r Rules = {0}".format(hw_table_size),
            for i in range(0,10,1):
                flow["flow"]["priority"]=hw_table_size+i
                flow = self.controller.buildDummyFlow(flow)
                self.controller.addFlow(self.switch2920.getDPID(),flow)
            current_count = self.switch2920.getHardwareFlowsCount()
            if hw_table_size==current_count:
                break
            hw_table_size = current_count
        print
        print "Rules number limit = ",str(hw_table_size)
        return hw_table_size

#=========================================================================================
    #mac-ip aware enabled
    def measureGetFlowsImpact(self, flow, table_id, max_table_size):
        self.switch3500.cli.resetOpenflowInstance()
        self.installPingRules(table_id)
        self.Iperf.startCapturingThroughput()
        self.Ping.startCapturingDelay()
        time.sleep(5)
        flow = flow
        flow["flow"]["table_id"] = table_id
        rules_count = self.switch3500.getHardwareFlowsCount()
        while rules_count<=50:
            flow = self.controller.buildDummyFlow(flow)
            flow["flow"]["priority"]=rules_count+1
            self.controller.addFlow(self.switch3500.getDPID(),flow)
            if(rules_count%10)==0:
                for i in range(0,10,1):
                    self.controller.getTableFlowsCount(self.switch3500.getDPID(),table_id)
            rules_count+=1
            print "\r",rules_count,
        time.sleep(5)
        self.Iperf.stopCapturingThroughput()
        self.Ping.stopCapturingDelay()




    def fillHWTableWithDummyRules(self):
        flow = SwitchParameters.switch3500_rule_9_OF13
        flow["flow"]["table_id"]=100
        for i in range(0,1527,1):
            flow["flow"]["priority"]=i+1
            print "\r",i,
            self.controller.addFlow(self.switch3500.getDPID(),flow)
        print "HW is full!"









def main():
    test = TestingScenario3500()
    test.start()


if __name__ == '__main__':
    main()