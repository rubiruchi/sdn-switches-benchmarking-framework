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
        self.switch3500 = SwitchMonitor("00:0a:74:46:a0:5f:1e:80")
        self.controller = HPSDNController("10.1.3.16")
        self.Iperf = BandwidthMeter("10.1.3.17", "marian", "descartes",
                                   "10.1.3.11", "marian", "descartes",
                                   'iperf -c 10.100.3.17 -i 1 -y C', 'iperf -s')
        self.Iperf.setTestDuraton(10000)
        self.Ping = DelayMonitor("10.1.3.11", "marian", "descartes", "10.100.3.17", 1000)
        self.Ping.setPingCount(10000)

    def start(self):
        # self.testActionsPerformace()
        # self.switch3500.cli.setOpenFlowVersion(10)
        # self.switch3500.cli.setPolicyEngineUsageLimit(100)
        # print "=================== Test 1:Measuring Hardware Processing Performance =========================="
        # self.hardwareProcessingPerformance(duration=20)
        # print "==============================================================================================="
        # print "=================== Test 2:Measuring Rules Insertion Performance =============================="
        # self.measureRuleInsertionPerformance(flow=flow,table_id=100,max_rule_count=20)
        # print "==============================================================================================="
        # print "=================== Test 3:Measuring Max Rule Count ==========================================="
        # self.measureTableSizeForDifferentRules()
        # print "==============================================================================================="
        # print "=================== Test 4:Flow Pull Performance =============================="
        # flow = SwitchParameters.switch3500_rule_9_OF13
        # self.measureGetFlowsImpact(flow=flow,table_id=100,max_table_size=20)
        # print "==============================================================================================="
        # print "=================== Test 5:OpenFlow Policy Engine dependency =============================="
        # self.measureOpenflowPolicyEngineDependency(table_id=100)
        # print "==============================================================================================="
        #self.switch3500.cli.setPolicyEngineUsageLimit(100)
        # print "=================== Test 1:Measuring Software Processing Performance =========================="
        # self.switch3500.cli.setSoftwareFlowTableRateLimit(10000)
        # self.installSFPingRules(200)
        # self.softwareProcessingPerformance()
        # print "==============================================================================================="
        # self.switch3500.cli.setSoftwareFlowTableRateLimit(10000)
        # print "=================== Test 2:Measuring Rules Insertion Performance =============================="
        # flow = SwitchParameters.switch3500_rule_9_OF13
        # self.measureRuleInsertionPerformance(flow,200,1526)
        # print "==============================================================================================="
        # print "=================== Test 3:Flow Pull Performance =============================="
        # flow = SwitchParameters.switch3500_rule_9_OF13
        # self.switch3500.cli.setSoftwareFlowTableRateLimit(10000)
        # self.measureGetFlowsImpact(flow,200,1526)
        # print "==============================================================================================="
        print "=================== Test 4:PPS change =============================="
        self.switch3500.cli.setPolicyEngineUsageLimit(100)
        self.softwarePPSChange()
        print "==============================================================================================="
        return

    def testActionsPerformace(self):
        self.switch3500.cli.resetOpenflowInstance()
        for i in range(0,10,1):
            for flow in SwitchParameters.switch3500_rule_action_performace_output_setipsrc:
                flow["flow"]["table_id"]=200
                self.controller.addFlow(self.switch3500.getDPID(),flow)
        self.hardwareProcessingPerformance(30)
        print self.processIperfAndPingOutput()
        return






    def processIperfAndPingOutput(self):
        while self.Iperf.finished==False:
            time.sleep(1)
        while self.Ping.finished==False:
            time.sleep(1)
        ia = self.Iperf.values
        pa = self.Ping.values
        if len(pa)<len(ia):
            l = len(pa)
        else:
            l = len(ia)
        ias = 0
        pas = 0
        for i in range(0,l,1):
            ias+=ia[i]
            pas+=pa[i]
            print ia[i],"\t",pa[i]
        aia = ias/l
        apa = pas/l
        print "Avarage Bandwidth: ",aia
        print "Avarage Delay: ",apa
        return [aia,apa]





    def installPingRules(self,table_id):
        flow1 = SwitchParameters.testbed_ping_rule_1
        flow2 = SwitchParameters.testbed_ping_rule_2
        flow1["flow"]["table_id"]=table_id
        flow2["flow"]["table_id"]=table_id
        self.controller.addFlow(self.switch3500.getDPID(),flow1)
        time.sleep(1)
        self.controller.addFlow(self.switch3500.getDPID(),flow2)
        time.sleep(1)


#=========================================  Hardware Processing Perfoemance performance =========================
    def hardwareProcessingPerformance(self,duration):
        #self.switch3500.cli.resetOpenflowInstance()
        #self.installPingRules(100)
        p1 = self.Iperf.startCapturingThroughput()
        p2 = self.Ping.startCapturingDelay()
        time.sleep(duration)
        self.Iperf.stopCapturingThroughput()
        self.Ping.stopCapturingDelay()
        time.sleep(5)
        self.processIperfAndPingOutput()

#=========================================  Software Processing Perfoemance performance =========================

    def installSFPingRules(self,table_id):
        flow1 = SwitchParameters.switch3500_ping_rule_1
        flow2 = SwitchParameters.switch3500_ping_rule_2
        flow1["flow"]["table_id"]=table_id
        flow2["flow"]["table_id"]=table_id
        while(self.switch3500.getSoftwareFlowsCount()<3):
            self.controller.addFlow(self.switch3500.getDPID(),flow1)
            self.controller.addFlow(self.switch3500.getDPID(),flow2)


    def softwareProcessingPerformance(self):
        cpus = []
        p1 = self.Iperf.startCapturingThroughput()
        p2 = self.Ping.startCapturingDelay()
        for i in range(0,10,1):
            time.sleep(1)
            cpus.append(self.switch3500.getCurrentCPU())
        self.Iperf.stopCapturingThroughput()
        self.Ping.stopCapturingDelay()
        time.sleep(2)
        results = self.processIperfAndPingOutput()
        sum = 0
        for i in cpus:
            sum+=int(i)
        print "Avarage CPU: ",str()
        results.append(float(sum/len(cpus)))
        return results


    def softwarePPSChange(self):
        f = open("3500_SfPpsChangePerformance.txt","w")
        f.write("PPS\tThroughput\tDelay\tCPU\n")
        for i in range(10000,10100,100):
            self.switch3500.cli.setSoftwareFlowTableRateLimit(i)
            self.installSFPingRules(200)
            r = self.softwareProcessingPerformance()
            #print r,"srthsh"
            f.write(str(i)+"\t"+
                    str(r[0])+"\t"+
                    str(r[1])+"\t"+
                    str(r[2])+"\t\n")
        f.close()






#=========================================  Rule insetion performance =========================
    def measureRuleInsertionPerformance(self,flow,table_id,max_rule_count):
        cpus = {}
        flow_insertion_delays = {}
        flow_insertion_moments = {}
        flow = flow
        flow["flow"]["table_id"]=table_id
        self.switch3500.cli.resetOpenflowInstance()
        if table_id is 100:
            self.installPingRules(100)
        if table_id is 200:
            self.installSFPingRules(200)
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
        self.processIperfAndPingOutput()
        print "Experiment duration = "+str(duration)
        f = open("3500_RuleInsertionPerformance_"+str(table_id)+".txt","w")
        f.write("Rule\tMoment\tDelay\tCPU\n")
        for key in flow_insertion_moments.keys():
            f.write(str(key)+"\t"+
                    str(flow_insertion_moments[key])+"\t"+
                    str(flow_insertion_delays[key])+"\t"+
                    str(cpus[key])+"\t\n")
#=========================================  Policy Engine Dependencie =========================


    def measureOpenflowPolicyEngineDependency(self,table_id):
        flow = SwitchParameters.switch3500_rule_9_OF13
        flow["flow"]["table_id"]=table_id
        for i in range(0,100,10):
            self.switch3500.cli.setPolicyEngineUsageLimit(i)
            time.sleep(3)
            self.measureMaxRuleCountInHardware(flow)



#=========================================  MAX TABLE SIZES =========================
    def measureTableSizeForDifferentRules(self):
        table_id = 100
        for flow in SwitchParameters.switch_compatible_rules["3500_OF13"]:
            self.switch3500.cli.resetOpenflowInstance()
            time.sleep(3)
            flow["flow"]["table_id"]=table_id
            self.measureMaxRuleCountInHardware(flow)
        print "========================================================="

    def measureMaxRuleCountInHardware(self,flow):
        print "Flow Pattern:", flow
        print "Number of wildcards: ",int(13-len(flow["flow"]["match"]))
        hw_table_size = self.switch3500.getHardwareFlowsCount()
        #while True:
        while hw_table_size<20:
            print "\r Rules = {0}".format(hw_table_size),
            for i in range(0,10,1):
                flow["flow"]["priority"]=hw_table_size+i
                flow = self.controller.buildDummyFlow(flow)
                self.controller.addFlow(self.switch3500.getDPID(),flow)
            current_count = self.switch3500.getHardwareFlowsCount()
            if hw_table_size==current_count:
                break
            hw_table_size = current_count
        print
        print "Rules number limit = ",str(hw_table_size)

#=========================================================================================
    #mac-ip aware enabled
    def measureGetFlowsImpact(self, flow, table_id, max_table_size):
        self.switch3500.cli.resetOpenflowInstance()
        if table_id is 100:
            self.installPingRules(100)
        if table_id is 200:
            self.installSFPingRules(200)
        time.sleep(5)
        self.Iperf.startCapturingThroughput()
        self.Ping.startCapturingDelay()
        t = threading.Thread(target=self.getFlowsInThread)
        t.start()
        flow = flow
        flow["flow"]["table_id"] = table_id
        rules_count = self.switch3500.getHardwareFlowsCount()
        while rules_count<=max_table_size:
            flow = self.controller.buildDummyFlow(flow)
            flow["flow"]["priority"]=rules_count+1
            self.controller.addFlow(self.switch3500.getDPID(),flow)
            rules_count+=1
            print "\rRules=",rules_count,
        time.sleep(10)
        self.Iperf.stopCapturingThroughput()
        self.Ping.stopCapturingDelay()
        self.processIperfAndPingOutput()
        time.sleep(5)
        del t

    def getFlowsInThread(self):
        i = 0
        while True:
            i+=1
            self.controller.getTableFlowsCount(self.switch3500.getDPID(),100)
            print "\rI=",i,



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