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
        self.switch5130 = SwitchMonitor("00:00:00:00:00:00:00:16")
        self.controller = HPSDNController("10.1.3.16")


    def start(self):
        #self.measureExtensibilityTable()
        self.measureMacIPTable5700()


#=========================================  MAX TABLE SIZES 5700 =========================
    def measureExtensibilityTable5700(self):
        print "=================== Test 3:Measuring Max Rule Count for EXTENSIBILITY Table====================="
        table_id = 20
        self.switch5700.cli.enableExtensibilityTable()
        rules = SwitchParameters.switch_compatible_rules["5700_NORMAL"]
        for i in range(0,len(rules)-1,1):
            self.switch5700.cli.resetOpenflowInstance()
            self.measureMaxRuleCountInHardware(self.switch5700,rules[i],table_id)
        print "========================================================="

    def measureMacIPTable5700(self):
        print "=================== Test 3:Measuring Max Rule Count for EXTENSIBILITY Table====================="
        table_id = 10
        self.switch5700.cli.enableMacIPTable()
        rule = SwitchParameters.switch_compatible_rules["5700_MAC_IP"][0]
        self.switch5700.cli.resetOpenflowInstance()
        self.measureMaxRuleCountInHardware(self.switch5700,rule,table_id)
        print "========================================================="

#=========================================  MAX TABLE SIZES 5130 =========================
    def measureExtensibilityTable5130(self):
        print "=================== Test 3:Measuring Max Rule Count for EXTENSIBILITY Table====================="
        table_id = 20
        self.switch5130.cli.enableExtensibilityTable()
        rules = SwitchParameters.switch_compatible_rules["5130_NORMAL"]
        for i in range(0,len(rules)-1,1):
            self.switch5130.cli.resetOpenflowInstance()
            self.measureMaxRuleCountInHardware(self.switch5130,rules[i],table_id)
        print "========================================================="

    def measureMacIPTable5130(self):
        print "=================== Test 3:Measuring Max Rule Count for EXTENSIBILITY Table====================="
        table_id = 10
        self.switch5130.cli.enableMacIPTable()
        rule = SwitchParameters.switch_compatible_rules["5130_MAC_IP"][0]
        self.switch5130.cli.resetOpenflowInstance()
        self.measureMaxRuleCountInHardware(self.switch5130,rule,table_id)
        print "========================================================="

    def measureMaxRuleCountInHardware(self,switch,flow,table_id):
        flow["flow"]["table_id"]=table_id
        print "Flow Pattern:", flow
        print "Number of wildcards: ",int(13-len(flow["flow"]["match"]))
        hw_table_size = switch.getHardwareFlowsCount()
        while True:
            print "\r Rules = {0}".format(hw_table_size),
            for i in range(0,100,1):
                flow["flow"]["priority"]=hw_table_size+i
                flow = self.controller.buildDummyFlow(flow)
                #print flow
                self.controller.addFlow(switch.getDPID(),flow)
            current_count = switch.getHardwareFlowsCount()
            if hw_table_size==current_count:
                break
            hw_table_size = current_count
        print
        print "Rules number limit = ",str(hw_table_size)

#=========================================================================================


def main():
    test = TestingScenario5700()
    test.start()


if __name__ == '__main__':
    main()