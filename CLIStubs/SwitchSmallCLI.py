import logging

from SSHConnection import SSHConnection


class SwitchSmallCLI(SSHConnection):
    def __init__(self, switch_description):
        log_namespace = "Monitor.Switch"+switch_description["model"]+'CLI'
        self.logger = logging.getLogger(log_namespace)
        self.log_id = "Switch"+switch_description["model"]+":"+switch_description["ip"]+": "
        SSHConnection.__init__(self,switch_description["ip"],switch_description["user"],
                               switch_description["password"],switch_description["cli_name"], log_namespace)
        self.OF_INSTANCE = switch_description["openflow_instance_name"]
        self.connect()
        self.COMMAND_SHOW_CPU = "show cpu 5"
        self.SF_RATE_LIMIT = 10
        self.COMMAND_RESET_OPENFLOW = ["config", "openflow disable", "openflow enable", "exit"]
        self.COMMAND_DISABLE_OPENFLOW_INSTANCE = ["config", "openflow disable", "openflow instance "+self.OF_INSTANCE+" disable", "exit"]
        self.COMMAND_GET_FLOWS_COUNT = "show openflow"
        self.getFlowsCountOverCLI()
        self.updateCPU()

    def setSoftwareFlowTableRateLimit(self, rate):
        if self.isConnected==False:
            self.logger.error(self.log_id+"Not connected!")
            return
        if rate<0 and rate > 10000:
            self.logger.error(self.log_id+"Could not set Openflow Software Rate-limit, value is out of range [0..10000].")
            return
        command = ["config", "openflow instance "+self.OF_INSTANCE+" disable",
                                             "openflow instance "+self.OF_INSTANCE+" limit software-rate "+str(rate),
                                             "openflow instance "+self.OF_INSTANCE+" enable"]
        if self.executeCommand(command):
            self.logger.debug(self.log_id+" OpenFlow "+self.OF_INSTANCE+" Software Rate-limit has been set to "+str(rate)+" pps..")
        else:
            self.logger.debug(self.log_id+" Error settting OpenFlow Software Rate-limit. Connection error!")

    def setPolicyEngineUsageLimit(self, limit):
        if self.isConnected==False:
            self.logger.error(self.log_id+"Not connected!")
            return
        if limit<0 and limit > 100:
            self.logger.error(self.log_id+"Could not set Openflow Policy-Usage limit, value is out of range [0..100].")
            return
        command = ["config","openflow disable","openflow limit policy-engine-usage "+str(limit),"openflow enable"]
        if self.executeCommand(command):
            self.logger.debug(self.log_id+" OpenFlow Policy-Engine usage limit has been set to "+str(limit)+"%.")
        else:
            self.logger.error(self.log_id+" OpenFlow Policy-Engine usage is not set. Connection error!")


    def resetOpenflowInstance(self):
        if self.isConnected==False:
            self.logger.error(self.log_id+"Not connected!")
            return
        command = self.COMMAND_RESET_OPENFLOW
        if self.executeCommand(command):
           self.logger.debug(self.log_id+" OpenFlow has been reset!")
        else:
            self.logger.error(self.log_id+" Error resetting OpenFlow. Connection error!")

    def disableOpenflowInstance(self):
        if self.isConnected==False:
            self.logger.error(self.log_id+"Not connected!")
            return
        command = self.COMMAND_DISABLE_OPENFLOW_INSTANCE
        if self.executeCommand(command):
           self.logger.debug(self.log_id+" OpenFlow instance has been disabled!")
        else:
            self.logger.error(self.log_id+" Error disabling OpenFlow. Connection error!")


    def getFlowsCountOverCLI(self):
        """
        :rtype: [hardware_flows_count,software_flows_count]
        """
        if(self.isConnected==False):
            self.logger.error(self.log_id+"Not connected!")
            return [0,0]
        for item in ([self.COMMAND_GET_FLOWS_COUNT]):
            self.connection.sendline(item)
            self.connection.expect(self.OF_INSTANCE)
            self.connection.expect('# ')
        try:
            s = self.connection.before
            return self.parseFlowsCountOutput(s)
        except:
            self.logger.warning(self.log_id+"Unable to parse SHOW OPENFLOW output!")
            return [0,0]
        #else:
        #    self.logger.info(" Unable to obtain Flows count. Connection error!")
        #    return [0,0]



    def updateCPU(self):
        if(self.isConnected==False):
            self.logger.error(self.log_id+"Not connected!")
            return 0
        if self.executeCommand([self.COMMAND_SHOW_CPU]):
            try:
                s = self.connection.before
                return self.parseCPUOutput(s)
            except:
                self.logger.warning(self.log_id+"Unable to parse SHOW CPU output!")
                return 0
        else:
            self.logger.error(self.log_id+" Unable to obtain CPU load. Connection error!")
            return 0

    def executeCommand(self,command):
        try:
            for item in (command):
                self.connection.sendline(item)
                self.connection.expect('# ',timeout=1000)
            return True
        #except self.connection.TIMEOUT,self.connection.EOF:
        except self.connection.EOF:
            self.logger.error(self.log_id+"Switch CLI doesn't respond.")
            self.logger.debug(self.log_id+"Reconnecting to the Switch CLI...")
            self.connect()
            return False

    def setOpenFlowVersion(self, version):
        if self.isConnected==False:
            self.logger.error(self.log_id+"Not connected!")
            return
        if version is 10:
            command = ["config","openflow disable","openflow instance "+self.OF_INSTANCE+" disable","openflow instance "+self.OF_INSTANCE+" version 1.0","openflow enable","openflow instance "+self.OF_INSTANCE+" enable"]
        elif version is 13:
            command = ["config","openflow disable","openflow instance "+self.OF_INSTANCE+" disable","openflow instance "+self.OF_INSTANCE+" version 1.3","openflow enable","openflow instance "+self.OF_INSTANCE+" enable"]
        else:
            self.logger.error(self.log_id+"Switch doesn't support the specified Openflow version.")
            return
        if self.executeCommand(command):
            self.logger.debug(self.log_id+" OpenFlow version has been set to "+str(version)+".")
        else:
            self.logger.error(self.log_id+" OpenFlow version is not set. Connection error!")



    def parseCPUOutput(self,s):
        lines = s.split()
        obj = lines[3]
        obja = obj.split('/')
        cpu_load = obja[0]
        return cpu_load

    def parseFlowsCountOutput(self,s):
        lines = s.split()
        return [int(lines[1]),int(lines[2])]



