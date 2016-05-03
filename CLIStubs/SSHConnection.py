import logging
import pexpect


class SSHConnection:
    def __init__(self, ip, user, password, cli_name, log_namespace):
        self.logger = logging.getLogger(log_namespace+".SSHConnection")
        self.log_id = "[SSH:"+user+'@'+ip+"]"
        self.logger.setLevel(logging.DEBUG)
        self.IP = ip
        self.USER = user
        self.PASS = password
        self.CLI_NAME = cli_name
        self.isConnected = False
        self.connection = None


    def connect(self):
        self.connection = self.connectSSH()
        if(self.connection!=None):
            self.isConnected = True

    def setIP(self, ip):
        self.IP=ip

    def getIP(self):
        return self.IP

    def setUser(self, user):
        self.USER=user

    def setPassword(self, password):
        self.PASS = password

    def setCLIName(self,name):
        self.CLI_NAME = name


    def connectSSH(self):
        cli = pexpect.spawn('ssh '+self.USER+'@'+self.IP)
        while True:
            i= cli.expect(['Press any key to continue',
                         'password:',
                         self.CLI_NAME,
                         pexpect.EOF,
                         "Are you sure you want to continue connecting (yes/no)?",
                         pexpect.TIMEOUT])
            if i==0:
                cli.sendline('yes')
            elif i==1:
                cli.sendline(self.PASS)
            elif i==2:
                self.logger.debug(self.log_id+"Login Successfull!")
                return cli
            elif i==3:
                self.logger.error(self.log_id+"Connection timeout.")
                return None
            elif i==4:
                cli.sendline("yes")
            elif i==4:
                self.logger.error(self.log_id+"Connection timeout.")
                return None
        return None





