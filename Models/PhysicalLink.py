
class PhysicalLink(object):
    def __init__(self, dpid1, port1, dpid2, port2):
        self.dpid1 = dpid1
        self.port1 = port1
        self.dpid2 = dpid2
        self.port2 = port2

    def __getattribute__(self, name):
        return super(PhysicalLink, self).__getattribute__(name)

    def toString(self):
        s = ""
        s = str(self.port1)
        s = s + "<-->"
        s = s + str(self.port2)
        return s

    def getdpid1(self):
        return self.dpid1

    def getdpid2(self):
        return self.dpid2

    def getport1(self):
        return self.port1

    def getport2(self):
        return self.port2
