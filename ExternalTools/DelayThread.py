import logging
import pexpect
import threading
from multiprocessing import Process
import sys
class DelayMonitor():
    def __init__(self, client_ip, client_user, client_pass, server_ip, ping_count):
        #threading.Thread.__init__(self)
        log_namespace = "Monitor."+__name__
        self.logger = logging.getLogger(log_namespace)
        self.logger.setLevel(logging.DEBUG)
        self.thread_name = "[PING:"+client_ip+"->"+server_ip+"]"
        self.CLIENT_IP = client_ip
        self.CLIENT_USER = client_user
        self.CLIENT_PASS = client_pass
        self.SERVER_IP = server_ip
        self.PING_COMMAND = "ping "+server_ip+" -i 1"
        self.ping_count = ping_count
        self.values = []
        self.finished = False
        self.CONNECT_COMMAND = 'ssh '+self.CLIENT_USER+'@'+self.CLIENT_IP
        self.c_pexpect = self.connectClient()
        self.isConnected = False
        if(self.c_pexpect!=None):
            self.isConnected = True
        self.currentDelay = 0

    def setPingCount(self, count):
        self.ping_count = count

    def startCapturingDelay(self):
        self.values = []
        p = threading.Thread(target=self.run)
        p.start()
        self.finished = False
        return p

    def run(self):
        try:
            if(self.isConnected!=True):
                return
            command = self.PING_COMMAND+" -c "+str(self.ping_count)
            self.c_pexpect.sendline(s=command)
            self.c_pexpect.expect(self.CLIENT_USER+'@', timeout=1000, searchwindowsize=1000)
            s = self.c_pexpect.before
            self.pingAllLinesParser(s)
            self.finished = True
            return True
        except:
            print sys.exc_info()[1]
            return False

    def pingAllLinesParser(self,output):
        try:
            lines = output.split('\n')
            for line in lines:
                if line.__contains__("icmp")==False:
                    continue
                columns = line.split(' ')
                col = columns[6]
                col = col.split('=')
                rtt_avg = float(col[1])
                self.values.append(rtt_avg)
                self.currentDelay = rtt_avg
            #print self.thread_name, self.values
        except:
            self.logger.error(self.thread_name+"Error parsing output.")


    def stopCapturingDelay(self):
        self.c_pexpect.sendcontrol('c')

    def getCurrentDelay(self):
        return self.currentDelay

    def connectClient(self):
        p = pexpect.spawn(self.CONNECT_COMMAND)
        while True:
            i=p.expect(['password:','Welcome to Ubuntu',pexpect.EOF, "Are you sure you want to continue connecting (yes/no)?"])
            if i==0:
                p.sendline(self.CLIENT_PASS)
            elif i==1:
                self.logger.debug(self.thread_name+"Login Successfull!")
                self.logger.debug(self.thread_name+"Client at %s ready."%self.CLIENT_IP)
                p.expect(self.CLIENT_USER+'@')
                return p
            elif i==2:
                self.logger.error(self.thread_name+"Connection timeout.")
                return None
            elif i==3:
                p.sendline("yes")
        return None

    def updatePing(self,ping_count):
        if(self.isConnected!=True):
            return
        self.c_pexpect.sendline(s=self.PING_COMMAND+" -c "+str(ping_count))
        self.c_pexpect.expect(self.CLIENT_USER+'@')
        s = self.c_pexpect.before
        self.pingOutputParser(s)


    def pingOutputParser(self, output):
        try:
            lines = output.split( )
            if(len(lines)>2):
                last_line = lines[len(lines)-2]
                columns = last_line.split('/')
                rtt_avg = float(columns[1])
                self.currentDelay = rtt_avg
        except:
            self.logger.error(self.thread_name+"Error parsing output.")

