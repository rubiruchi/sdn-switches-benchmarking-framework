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
        #print "=================== Test 1:Measuring Standart Pipeline Processing Performance =========================="
        #self.switch3500.cli.disableOpenflowInstance()
        #self.hardwareProcessingPerformance(duration=90)
        #print "==============================================================================================="
        #self.switch3500.cli.setOpenFlowVersion(10)
        # self.switch3500.cli.setPolicyEngineUsageLimit(100)
        # print "=================== Test 1:Measuring Hardware Processing Performance =========================="
        # self.switch3500.cli.resetOpenflowInstance()
        # self.installPingRules(table_id=0)
        # self.hardwareProcessingPerformance(duration=90)
        # print "==============================================================================================="
        # print "=================== Test 2:Measuring Rules Insertion Performance =============================="
        # flow = SwitchParameters.switch2920_rule_10
        # self.measureRuleInsertionPerformance(flow=flow,table_id=0,max_rule_count=500)
        # print "==============================================================================================="
        # print "=================== Test 3:Measuring Max Rule Count ==========================================="
        # self.measureTableSizeForDifferentRules(flow_set=SwitchParameters.switch_compatible_rules["3500_OF10"],table_id=0)
        # print "==============================================================================================="
        # print "=================== Test 4:Flow Pull Performance =============================="
        # flow = SwitchParameters.switch2920_rule_10
        # self.measureGetFlowsImpact(flow=flow,table_id=0,max_table_size=100)
        # print "==============================================================================================="
        # print "=================== Test 5:OpenFlow Policy Engine dependency =============================="
        # self.measureOpenflowPolicyEngineDependency(table_id=0)
        # print "==============================================================================================="
        print "=================== Test 1:Measuring Software Processing Performance =========================="
        self.switch3500.cli.setPolicyEngineUsageLimit(10)
        self.switch3500.cli.setSoftwareFlowTableRateLimit(10000)
        self.fillHWTableWithDummyRules(dummy_rule=SwitchParameters.switch3500_rule_9_OF10,table_size=160,table_id=0)
        self.softwareProcessingPerformance(duration=90)
        print "==============================================================================================="
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
        # print "=================== Test 4:PPS change =============================="
        # self.switch3500.cli.setPolicyEngineUsageLimit(100)
        # self.softwarePPSChange()
        # print "==============================================================================================="
        #print "========================================= Test Rule replacement Engine ==========================="
        #self.switch3500.cli.setPolicyEngineUsageLimit(20)
        #self.switch3500.cli.setSoftwareFlowTableRateLimit(10000)
        #self.fillHWTableWithDummyRules(dummy_rule=SwitchParameters.switch3500_rule_9_OF10,table_size=305,table_id=0)
        # print "==============================================================================================="
        #flow = SwitchParameters.switch3500_rule_ShortDummy_1_OF10


    def iperfComparisonForVariablePacketSize(self,pipeline_type="standard",duration=10):
        self.Iperf = BandwidthMeter("10.1.3.17", "marian", "descartes",
                                   "10.1.3.11", "marian", "descartes",'iperf -c 10.100.3.17 -i 1 -y C','iperf -s')
        self.Iperf.setTestDuraton(10000)
        self.switch3500.cli.setSoftwareFlowTableRateLimit(10000)
        print "Pipeline type: ",pipeline_type
        print "MTUSize\tThroughput\tDelay\n"
        for packet_size in range(20,120,10):
            command = 'iperf -c 10.100.3.17 -i 1 -y C -N -M '+str(packet_size)
            self.Iperf.setClientCommand(command)
            if pipeline_type=="standard":
                self.hardwareProcessingPerformance(duration=duration)
            if pipeline_type=="openflow":
                self.hardwareProcessingPerformance(duration=duration)
            if pipeline_type=="software":
                cpus,flows = self.softwareProcessingPerformance(duration=duration)
            throughputs,delays = self.processIperfAndPingOutput()
            print packet_size,"\t",self.calculateAvarage(throughputs),"\t",self.calculateAvarage(delays)
    def testPipelinePerformance(self):
        self.switch3500.cli.disableOpenflowInstance()
        self.iperfComparisonForVariablePacketSize(pipeline_type="standard")
        self.switch3500.cli.resetOpenflowInstance()
        self.iperfComparisonForVariablePacketSize(pipeline_type="openflow")
        self.switch3500.cli.resetOpenflowInstance()
        self.switch3500.cli.setPolicyEngineUsageLimit(5)
        self.fillHWTableWithDummyRules(dummy_rule=SwitchParameters.switch3500_rule_9_OF10,table_id=0,table_size=80)
        self.installSFPingRules(table_id=0,priority=30000)
        self.iperfComparisonForVariablePacketSize(pipeline_type="software")

    def testRuleReplacementEngine(self):
        self.switch3500.cli.setPolicyEngineUsageLimit(5)
        self.switch3500.cli.setSoftwareFlowTableRateLimit(10000)
        # Dummy rule matches only ipv4-src, priority 100
        # Ping rules matches in_port, ipv4_src and ipv4_dst, priority 2
        print "===================== Ping rules is the MOST EXACT and has LOWEST PRIORITY============="
        flow = SwitchParameters.switch3500_rule_ShortDummy_1_OF10
        flow["flow"]["idle_timeout"]=120
        flow["flow"]["priority"]=100
        self.switch3500.cli.resetOpenflowInstance()
        self.fillHWTableWithDummyRules(dummy_rule=flow,table_size=160,table_id=0)
        self.installSFPingRules(table_id=0,priority=2)
        self.softwareProcessingPerformance(duration=90)
        # Dummy rule machtes all fields, priority 100
        # Ping rules matches in_port, ipv4_src and ipv4_dst, priority 2
        print "===================== Ping rules is the LESS EXACT and has LOWEST PRIORITY============="
        flow = SwitchParameters.switch3500_rule_9_OF10
        flow["flow"]["idle_timeout"]=120
        flow["flow"]["priority"]=100
        self.switch3500.cli.resetOpenflowInstance()
        self.fillHWTableWithDummyRules(dummy_rule=flow,table_size=160,table_id=0)
        self.installSFPingRules(table_id=0, priority=2)
        self.softwareProcessingPerformance(duration=90)
        # Dummy rule machtes all fields, priority 100
        # Ping rules matches in_port, ipv4_src and ipv4_dst, priority 30000
        print "===================== Ping rules is the LESS EXACT and has HIGHEST PRIORITY============="
        flow = SwitchParameters.switch3500_rule_9_OF10
        flow["flow"]["idle_timeout"]=120
        flow["flow"]["priority"]=100
        self.switch3500.cli.resetOpenflowInstance()
        self.fillHWTableWithDummyRules(dummy_rule=flow,table_size=160,table_id=0)
        self.installSFPingRules(table_id=0, priority=30000)
        self.softwareProcessingPerformance(duration=90)
        # Dummy rule matches only ipv4-src, priority 100
        # Ping rules matches in_port, ipv4_src and ipv4_dst, priority 30000
        print "===================== Ping rules is the MOST EXACT and has HIGHEST PRIORITY============="
        flow = SwitchParameters.switch3500_rule_ShortDummy_1_OF10
        flow["flow"]["idle_timeout"]=120
        flow["flow"]["priority"]=100
        self.switch3500.cli.resetOpenflowInstance()
        self.fillHWTableWithDummyRules(dummy_rule=flow,table_size=160,table_id=0)
        self.installSFPingRules(table_id=0, priority=30000)
        self.softwareProcessingPerformance(duration=90)


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
        throughput_values = throughput_values[0:l]
        delay_values = delay_values[0:l]
        #avarage_throughput = self.calculateAvarage(throughput_values)
        #avarage_delay = self.calculateAvarage(delay_values)
        #print "Avarage Bandwidth: ",avarage_throughput
        #print "Avarage Delay: ",avarage_delay
        return throughput_values,delay_values

    def calculateAvarage(self,array):
        if len(array)==0:
            return 0
        sum = float(0)
        for i in array:
            sum+=int(i)
        return float(sum/len(array))


    def installPingRules(self, table_id=0, priority=0):
        flow1 = SwitchParameters.testbed_ping_rule_1_OF10
        flow2 = SwitchParameters.testbed_ping_rule_2_OF10
        flow1["flow"]["table_id"]=table_id
        flow2["flow"]["table_id"]=table_id
        flow1["flow"]["priority"]=priority
        flow2["flow"]["priority"]=priority
        self.controller.addFlow(self.switch3500.getDPID(),flow1)
        self.controller.addFlow(self.switch3500.getDPID(),flow2)


#=========================================  Hardware Processing Perfoemance performance =========================
    def hardwareProcessingPerformance(self,duration):
        p1 = self.Iperf.startCapturingThroughput()
        p2 = self.Ping.startCapturingDelay()
        time.sleep(duration)
        self.Iperf.stopCapturingThroughput()
        self.Ping.stopCapturingDelay()
        time.sleep(5)
        #print self.processIperfAndPingOutput()


#=========================================  Software Processing Perfoemance performance =========================

    def installSFPingRules(self,table_id=0, priority=0):
        flow1 = SwitchParameters.testbed_ping_rule_1_OF10
        flow2 = SwitchParameters.testbed_ping_rule_2_OF10
        flow1["flow"]["table_id"]=table_id
        flow2["flow"]["table_id"]=table_id
        self.controller.addFlow(self.switch3500.getDPID(),flow1)
        self.controller.addFlow(self.switch3500.getDPID(),flow2)


    def softwareProcessingPerformance(self,duration=90):
        cpus = {}
        flows = {}  #Only For Test placement rule
        p1 = self.Iperf.startCapturingThroughput()
        p2 = self.Ping.startCapturingDelay()
        for i in range(0,duration,1):
            time.sleep(1)
            cpus[i]=(self.switch3500.getCurrentCPU())
            flows[i] = (self.switch3500.cli.getFlowsCountOverCLI()) #Only For Test placement rules
        self.Iperf.stopCapturingThroughput()
        self.Ping.stopCapturingDelay()
        time.sleep(2)
        #results = self.processIperfAndPingOutput()
        #avarage_cpu = self.calculateAvarage(cpus.values())
        #for key in cpus.keys():
        #    print cpus[key],"\t",flows[key][0],"\t",flows[key][1]
        #print "Avarage CPU: ",avarage_cpu
        return cpus,flows


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
        flow = SwitchParameters.switch2920_rule_10
        flow["flow"]["table_id"]=table_id
        for i in range(0,100,10):
            self.switch3500.cli.setPolicyEngineUsageLimit(i)
            time.sleep(3)
            self.measureMaxRuleCountInHardware(flow)



#=========================================  MAX TABLE SIZES =========================
    def measureTableSizeForDifferentRules(self,flow_set,table_id):
        for flow in flow_set:
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
        while i<1000:
            i+=1
            self.controller.getTableFlowsCount(self.switch3500.getDPID(),0)
            print "\rI=",i,

    def fillHWTableWithDummyRules(self,dummy_rule,table_size, table_id):
        flow = dummy_rule
        flow["flow"]["table_id"]=table_id
        for i in range(0,table_size,1):
            flow["flow"]["priority"]=100+i+1
            flow = self.controller.buildDummyFlow(flow=flow)
            print "\rInserting rules: ",i,self.switch3500.cli.getFlowsCountOverCLI(),
            self.controller.addFlow(self.switch3500.getDPID(),flow)
            self.switch3500.addFlow(flow=flow)
        print
        print "{0} rules have been inserted in table={1}".format(table_size,table_id)



def main():
    test = TestingScenario3500()
    test.start()


if __name__ == '__main__':
    main()