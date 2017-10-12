#!/usr/bin/python2

#
# star topo example showing how to use MaxiNet
#

import time

from MaxiNet.Frontend import maxinet
from MaxiNet.tools import FatTree
from mininet.node import OVSSwitch


# messing with topo
from mininet.topo import Topo
from MaxiNet.tools import Tools

topo = Topo() #empty topo
cluster = maxinet.Cluster(minWorkers=5, maxWorkers=5)
exp = maxinet.Experiment(cluster, topo, switch=OVSSwitch)
exp.setup()

# SIGN

print "adding switches on workers..."
exp.addSwitch("s1", dpid=Tools.makeDPID(1), wid=0)
exp.addSwitch("s2", dpid=Tools.makeDPID(2), wid=1)
exp.addSwitch("s3", dpid=Tools.makeDPID(3), wid=2)
exp.addSwitch("s4", dpid=Tools.makeDPID(4), wid=3)
exp.addSwitch("s5", dpid=Tools.makeDPID(5), wid=4)

print "adding 5 hosts..."
exp.addHost("h1", ip=Tools.makeIP(1), max=Tools.makeMAC(1), pos="s1")
exp.addHost("h2", ip=Tools.makeIP(2), max=Tools.makeMAC(2), pos="s2")
exp.addHost("h3", ip=Tools.makeIP(3), max=Tools.makeMAC(3), pos="s3")
exp.addHost("h4", ip=Tools.makeIP(4), max=Tools.makeMAC(4), pos="s4")
exp.addHost("h5", ip=Tools.makeIP(5), max=Tools.makeMAC(5), pos="s5")


print "add links between h_i and s_i"
exp.addLink("s1", "h1", autoconf=True)
exp.addLink("s2", "h2", autoconf=True)
exp.addLink("s3", "h3", autoconf=True)
exp.addLink("s4", "h4", autoconf=True)
exp.addLink("s5", "h5", autoconf=True)

print "add links between s1 and s2345..."
exp.addLink("s1", "s2", autoconf=True)
exp.addLink("s1", "s3", autoconf=True)
exp.addLink("s1", "s4", autoconf=True)
exp.addLink("s1", "s5", autoconf=True)


print exp.get_node("h1").cmd("ifconfig")  # call mininet cmd function of h1

print "waiting 5 seconds for routing algorithms on the controller to converge"
time.sleep(5)

# TESTING PING ALL
s = []
sent = 0.0
received = 0.0
if(len(s) == 0):
    for host in exp.hosts:
        for target in exp.hosts:
            if(target == host):
                continue
            print(host.name + " -> " + target.name + " " + target.IP())
            sent += 1.0

	    returnvals = host.pexec("ping -c1 " + target.IP())
            if(returnvals[2] != 0):
                print " X"
            else:
                received += 1.0
                print returnvals[0]

print "*** Results: %.2f%% dropped (%d/%d received)" % \
            ((1.0 - received / sent) * 100.0, int(received), int(sent))



exp.CLI(locals(), globals())

exp.stop()
