import logging

from SSHConnection import SSHConnection


class SwitchBigCLI(SSHConnection):
    def __init__(self, switch_description):
        log_namespace = "Monitor.Switch"+switch_description["model"]+'CLI'
        self.logger = logging.getLogger(log_namespace)
        self.log_id = "Switch"+switch_description["model"]+":"+switch_description["ip"]+": "
        SSHConnection.__init__(self,switch_description["ip"],switch_description["user"],
                               switch_description["password"],switch_description["cli_name"],log_namespace)
        self.OF_INSTANCE = switch_description["openflow_instance_name"]
        self.connect()
        self.COMMAND_SHOW_CPU = "display cpu-usage"
        self.COMMAND_RESET_OPENFLOW = ["openflow instance "+self.OF_INSTANCE, "undo active instance", "active instance", "quit"]
        self.COMMAND_GET_FLOWS_COUNT = "display openflow instance "+str(self.OF_INSTANCE)
        self.ENABLE_EXTENSIBILITY_TABLE = ["openflow instance "+self.OF_INSTANCE, "undo active instance", "flow-table extensibility 20", "active instance", "quit"]
        self.ENABLE_MACIP_TABLE = ["openflow instance "+self.OF_INSTANCE, "undo active instance", "flow-table mac-ip 10", "active instance", "quit"]
        self.executeCommand(["system-view"])



    def resetOpenflowInstance(self):
        if self.isConnected==False:
            self.logger.error(self.log_id+" Not connected!")
            return
        command = self.COMMAND_RESET_OPENFLOW
        if self.executeCommand(command):
           self.logger.debug(self.log_id+"OpenFlow has been reset!")
        else:
            self.logger.error(self.log_id+" Error resetting OpenFlow. Connection error!")

    def enableExtensibilityTable(self):
        if self.isConnected==False:
            self.logger.error(self.log_id+" Not connected!")
            return
        command = self.ENABLE_EXTENSIBILITY_TABLE
        if self.executeCommand(command):
           self.logger.debug(self.log_id+"Extensibility tables has been enabled, ID = 20!")
        else:
            self.logger.error(self.log_id+" Error changing OpenFlow table. Connection error!")

    def enableMacIPTable(self):
        if self.isConnected==False:
            self.logger.error(self.log_id+" Not connected!")
            return
        command = self.ENABLE_MACIP_TABLE
        if self.executeCommand(command):
           self.logger.debug(self.log_id+"MAC-IP table has been enabled, ID = 10!")
        else:
            self.logger.error(self.log_id+" Error changing OpenFlow table. Connection error!")


    def getFlowsCountOverCLI(self):
        """
        :rtype: [hardware_flows_count]
        """
        if(self.isConnected==False):
            self.logger.error(self.log_id+"Not connected!")
            return [0,0]
        self.connection.sendline(self.COMMAND_GET_FLOWS_COUNT)
        self.connection.expect('Flow-entry max-limit:')
        s=self.connection.before
        self.connection.sendline('q')
        self.connection.expect(']')
        try:
            table_size = self.parseFlowsCountOutput(s)
            return [table_size,0]
        except:
            self.logger.warning(self.log_id+"Unable to parse SHOW OPENFLOW output!")
            return [0,0]


    #
    # def updateCPU(self):
    #     if(self.isConnected==False):
    #         self.logger.error("Not connected!")
    #         return 0
    #     if self.executeCommand([self.COMMAND_SHOW_CPU]):
    #         try:
    #             s = self.connection.before
    #             return self.parseCPUOutput(s)
    #         except:
    #             self.logger.warning("Unable to parse SHOW CPU output!")
    #             return 0
    #     else:
    #         self.logger.info(" Unable to obtain CPU load. Connection error!")
    #         return 0

    def updateCPU(self):
        self.connection.sendline(self.COMMAND_SHOW_CPU)
        self.connection.expect('minutes')
        s = self.connection.before
        try:
            cpu_load = self.parseCPUOutput(s)
            return cpu_load
        except:
            self.logger.warning(self.log_id+"Unable to parse DISPLAY CPU-USAGE output!")


    def executeCommand(self,command):
        try:
            for item in (command):
                self.connection.sendline(item)
                self.connection.expect(']')
            return True
        #except self.connection.TIMEOUT,self.connection.EOF:
        except self.connection.EOF:
            self.logger.error(self.log_id+"Switch CLI doesn't respond.")
            self.logger.debug(self.log_id+"Reconnecting to the Switch CLI...")
            self.connect()
            return False



    def parseCPUOutput(self,s):
        lines = s.split()
        if lines.__contains__("seconds"):
            i = lines.index('seconds')
            obj = lines[i-4]
            obj = obj.split('%')
            cpu_load = obj[0]
            return int(cpu_load)
        return 0

    def parseFlowsCountOutput(self,s):
        lines = s.split()
        try:
            return int(lines[len(lines)-1])
        except:
            self.logger.error(self.log_id+" Unable to parse SHOW OPENFLOW output")




