import logging
import pexpect
import subprocess
import threading
from multiprocessing import Process
import time
import sys

class BandwidthMeter():
    def __init__(self, server, server_user, server_pass, client, client_user, client_pass, client_command, server_command):
        #threading.Thread.__init__(self)
        log_namespace = "Monitor."+__name__
        self.logger = logging.getLogger(log_namespace)
        self.logger.setLevel(logging.DEBUG)

        #self.thread_client_name = "[IPERF-Client-"+client+"]"
        #self.thread_server_name = "[IPERF-Server-"+server+"]"
        self.thread_name = self.thread_name = "[IPERF:"+client+"->"+server+"]"
        self.server = server
        self.server_user = server_user
        self.server_pass = server_pass
        self.client = client
        self.client_user = client_user
        self.client_pass = client_pass
        self.S_COMMAND = server_command
        self.C_COMMAND = client_command
        self.test_duration = 1
        self.values = []
        self.finished = False
        self.s_pexpect = self.connectServer()
        if(self.s_pexpect!=None):
            self.c_pexpect = self.connectClient()
        self.currentBandwidth = 0

    def getCurrentBandwidth(self):
        return self.currentBandwidth

    def setTestDuraton(self, duration):
        self.test_duration = duration

    def startCapturingThroughput(self):
        self.values = []
        p = threading.Thread(target=self.run)
        p.start()
        self.finished = False
        return p

    def run(self):
        try:
            self.c_pexpect.sendline(s=self.C_COMMAND+" -t "+str(self.test_duration))
            self.c_pexpect.expect(self.client_user+'@',timeout=self.test_duration+30,searchwindowsize=1000)
            s = self.c_pexpect.before
            #print s
            self.iperfAllLinesParser(s)
            self.finished = True
            return True
        except:
            self.logger.error(self.thread_name,sys.exc_info())
            return False

    def stopCapturingThroughput(self):
        self.c_pexpect.sendcontrol('c')

    def connectClient(self):
        p = pexpect.spawn('ssh '+self.client_user+'@'+self.client)
        while True:
            i=p.expect(['password:','Last login',pexpect.EOF, "Are you sure you want to continue connecting (yes/no)?"])
            if i==0:
                p.sendline(self.client_pass)
            elif i==1:
                self.logger.debug(self.thread_name+" Login successful to "+self.client_user+'@'+self.client)
                self.logger.debug(self.thread_name+" Client at %s started."%self.client)
                p.expect(self.client_user+'@')
                return p
            elif i==2:
                self.logger.error(self.thread_name+": Timeout connecting to server!")
                return None
            elif i==3:
                p.sendline("yes")
        return None

    def setClientCommand(self,command):
        self.C_COMMAND = command

    def updateBandwidth(self,duration):
        self.c_pexpect.sendline(s=self.C_COMMAND+" -t "+str(duration))
        self.c_pexpect.expect(self.client_user+'@')
        s = self.c_pexpect.before
        self.iperfOutputParser(s)

    def connectServer(self):
        p = pexpect.spawn('ssh '+self.server_user+'@'+self.server)
        while True:
            i=p.expect(['password:','Last login',pexpect.EOF, "Are you sure you want to continue connecting (yes/no)?"])
            if i==0:
                p.sendline(self.server_pass)
            elif i==1:
                self.logger.debug(self.thread_name+" Login successful to "+self.server_user+'@'+self.server)
                self.logger.debug(self.thread_name+" Server at %s started."%self.server)
                p.sendline(s=self.S_COMMAND)
                p.expect(self.server_user+'@')
                return p
            elif i==2:
                self.logger.error(self.thread_name+": Timeout connecting to server!")
                return None
            elif i==3:
                p.sendline("yes")
            else:
                self.logger.error(self.thread_name+": Error server initialization!")
                return None

        return None

    def stopServer(self):
        res = subprocess.check_output(chr(3))
        print self.thread_name+" Server stopped!"


    def iperfAllLinesParser(self, output):
        try:

            lines = output.split( )
            for line in lines:
                if(len(line)<20):
                    continue
                columns = line.split(',')
                bw = float(columns[8])/1000000
                self.values.append(bw)
            #print self.thread_name,self.values
        except:
            self.logger.error(self.thread_name+": Error parsing output.")
            #iperf_result_parsed = "[Time] "+columns[0]+" [SRC]:"+columns[1]+":"+columns[2]+" [DST:]"+columns[3]+":"+columns[4]+ \
            #                      " [ID:]"+columns[5]+" [Interval:]"+columns[6]+" [Transfer:]"+columns[7]+" [Bandwidth:]"+str(bw)+"Mbit/s"
            #return iperf_result_parsed

    def iperfOutputParser(self, output):
        try:
            #print output
            lines = output.split( )
            if(len(lines)>1):
                last_line = lines[len(lines)-1]
                columns = last_line.split(',')
                bw = float(columns[8])/1000000
                self.currentBandwidth = bw
        except:
            self.logger.error(self.thread_name+": Error parsing output.")
            #iperf_result_parsed = "[Time] "+columns[0]+" [SRC]:"+columns[1]+":"+columns[2]+" [DST:]"+columns[3]+":"+columns[4]+ \
            #                      " [ID:]"+columns[5]+" [Interval:]"+columns[6]+" [Transfer:]"+columns[7]+" [Bandwidth:]"+str(bw)+"Mbit/s"
            #return iperf_result_parsed