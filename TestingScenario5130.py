import logging

from Configurations import SwitchParameters
from ExternalTools.DelayThread import DelayMonitor
from ExternalTools.IperfThread import BandwidthMeter
from Models.HPSDNController import HPSDNController
from Models.SwitchMonitor import SwitchMonitor
from datetime import datetime
import time
import threading



class TestingScenario5130:
    def __init__(self):
        self.logger = logging.getLogger("Monitor.TestScenario")
        self.logger.setLevel(logging.DEBUG)
        self.switch5130 = SwitchMonitor("00:00:00:00:00:00:00:42")
        self.controller = HPSDNController("10.1.3.16")
        self.Iperf5130 = BandwidthMeter("10.1.3.17", "marian", "descartes",
                                   "10.1.3.11", "marian", "descartes",
                                   'iperf -c 10.100.3.17 -i 1 -y C', 'iperf -s')
        self.Iperf5130.setTestDuraton(10000)
        self.Ping5130 = DelayMonitor("10.1.3.11", "marian", "descartes", "10.100.3.17", 1000)
        self.Ping5130.setPingCount(10000)

    def start(self):
        self.switch5130.cli.enableExtensibilityTable()
        #print "=================== Test 1:Measuring Hardware Processing Performance =========================="
        #self.hardwareProcessingPerformance(60)
        #print "==============================================================================================="
        #return
        print "=================== Test 2:Measuring Rules Insertion Performance =============================="
        flow = SwitchParameters.switch5700_rule_1
        self.measureRuleInsertionPerformance(flow,20,512)
        print "==============================================================================================="
        #self.switch5130.cli.enableMacIPTable()
        #print "=================== Test 3:Measuring Max Rule Count ==========================================="
        #self.measureTableSizeForDifferentRules()
        #print "==============================================================================================="
        #print "=================== Test 4:Flow Pull Performance =============================="
        #flow = SwitchParameters.switch5700_rule_10
        #self.measureGetFlowsImpact(flow,20,512)
        #print "==============================================================================================="
        #self.switch5130.cli.enableMacIPTable()
        #print "=================== Test 1:Measuring Hardware Processing Performance =========================="
        #self.hardwareProcessingPerformance(60)
        #print "==============================================================================================="
        #return
        #print "=================== Test 2:Measuring Rules Insertion Performance =============================="
        #flow = SwitchParameters.switch5700_mac_ip_rule
        #self.measureRuleInsertionPerformance(flow,10,1000)
        #print "==============================================================================================="
        #print "=================== Test 3:Flow Pull Performance =============================="
        #flow = SwitchParameters.switch5700_mac_ip_rule
        #self.measureGetFlowsImpact(flow,10,1000)
        #print "==============================================================================================="


    def installPingRules(self, table_id=20, priority=0):
        flow1 = SwitchParameters.testbed_ping_rule_1_OF10
        flow2 = SwitchParameters.testbed_ping_rule_2_OF10
        flow1["flow"]["table_id"]=table_id
        flow2["flow"]["table_id"]=table_id
        flow1["flow"]["priority"]=priority
        flow2["flow"]["priority"]=priority
        self.controller.addFlow(self.switch5130.getDPID(),flow1)
        self.controller.addFlow(self.switch5130.getDPID(),flow2)


#=========================================  Hardware Processing Perfoemance performance =========================
    def hardwareProcessingPerformance(self,duration):
        p1 = self.Iperf5130.startCapturingThroughput()
        p2 = self.Ping5130.startCapturingDelay()
        time.sleep(duration)
        self.Iperf5130.stopCapturingThroughput()
        self.Ping5130.stopCapturingDelay()
        time.sleep(5)
        print self.processIperfAndPingOutput()

    def processIperfAndPingOutput(self):
        while self.Iperf5130.finished==False:
            time.sleep(1)
        while self.Ping5130.finished==False:
            time.sleep(1)
        throughput_values = self.Iperf5130.values
        delay_values = self.Ping5130.values
        if len(throughput_values)<len(delay_values):
            l = len(throughput_values)
        else:
            l = len(delay_values)
        throughput_values = throughput_values[0:l]
        delay_values = delay_values[0:l]
        avarage_throughput = self.calculateAvarage(throughput_values)
        avarage_delay = self.calculateAvarage(delay_values)
        print "Avarage Bandwidth: ",avarage_throughput
        print "Avarage Delay: ",avarage_delay
        return throughput_values,delay_values

    def calculateAvarage(self,array):
        if len(array)==0:
            return 0
        sum = float(0)
        for i in array:
            sum+=int(i)
        return float(sum/len(array))





#=========================================  Rule insetion performance =========================
    def measureRuleInsertionPerformance(self,flow,table_id,max_rule_count):
        cpus = {}
        flow_insertion_delays = {}
        flow_insertion_moments = {}
        flow = flow
        flow["flow"]["table_id"]=table_id
        self.switch5130.cli.resetOpenflowInstance()
        #self.installPingRules()
        #self.Iperf5130.startCapturingThroughput()
        #self.Ping5130.startCapturingDelay()
        rules_count = self.switch5130.getHardwareFlowsCount()
        start_time = datetime.now()
        while rules_count<max_rule_count:
            print "\r Rules = {0}".format(rules_count),
            flow = self.controller.buildDummyFlow(flow)
            flow["flow"]["priority"]=rules_count+1
            a = datetime.now()
            self.controller.addFlow(self.switch5130.getDPID(),flow)
            b = datetime.now()
            c = (b-a).microseconds
            flow_insertion_delays[rules_count]= c
            flow_insertion_moments[rules_count]= c
            if(rules_count%10)==0:
                cpus[rules_count]= self.switch5130.getCurrentCPU()
            else:
                cpus[rules_count]= 0
            rules_count+=1
        print
        end_time = datetime.now()
        duration = end_time - start_time
        #self.Iperf5130.stopCapturingThroughput()
        #self.Ping5130.stopCapturingDelay()
        #time.sleep(5)
        print "Experiment duration = "+str(duration)
        f = open("5130_RuleInsertionPerformance_"+str(table_id)+".txt","w")
        f.write("Rule\tMoment\tDelay\tCPU\n")
        for key in flow_insertion_moments.keys():
            f.write(str(key)+"\t"+
                    str(flow_insertion_moments[key])+"\t"+
                    str(flow_insertion_delays[key])+"\t"+
                    str(cpus[key])+"\t\n")
        #self.processIperfAndPingOutput()


#=========================================  MAX TABLE SIZES =========================
    def measureTableSizeForDifferentRules(self):
        table_id = 20
        for flow in SwitchParameters.switch_compatible_rules["5130_NORMAL"]:
            self.switch5130.cli.resetOpenflowInstance()
            flow["flow"]["table_id"]=table_id
            self.measureMaxRuleCountInHardware(flow)
        print "========================================================="

    def measureMaxRuleCountInHardware(self,flow):
        print "Flow Pattern:", flow
        print "Number of wildcards: ",int(13-len(flow["flow"]["match"]))
        hw_table_size = self.switch5130.getHardwareFlowsCount()
        while True:
            print "\r Rules = {0}".format(hw_table_size),
            for i in range(0,100,1):
                flow["flow"]["priority"]=hw_table_size+i
                flow = self.controller.buildDummyFlow(flow)
                #print flow
                self.controller.addFlow(self.switch5130.getDPID(),flow)
            current_count = self.switch5130.getHardwareFlowsCount()
            if hw_table_size==current_count:
                break
            hw_table_size = current_count
        print
        print "Rules number limit = ",str(hw_table_size)

#=========================================================================================
    #mac-ip aware enabled
    def measureGetFlowsImpact(self, flow, table_id, max_table_size):
        self.switch5130.cli.resetOpenflowInstance()
        #self.installPingRules()
        self.Iperf5130.startCapturingThroughput(180)
        self.Ping5130.startCapturingDelay(180)
        time.sleep(5)
        flow = flow
        flow["flow"]["table_id"] = table_id
        rules_count = self.switch5130.getHardwareFlowsCount()
        while rules_count<=max_table_size:
            flow = self.controller.buildDummyFlow(flow)
            flow["flow"]["priority"]=rules_count+1
            self.controller.addFlow(self.switch5130.getDPID(),flow)
            if(rules_count%10)==0:
                for i in range(0,10,1):
                    print self.controller.getTableFlowsCount(self.switch5130.getDPID(),table_id)
            rules_count+=1
        time.sleep(5)
        self.Iperf5130.stopCapturingThroughput()
        self.Ping5130.stopCapturingDelay()













def main():
    test = TestingScenario5130()
    test.start()


if __name__ == '__main__':
    main()