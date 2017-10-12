#!/usr/bin/python2

#
# This example shows how to dynamically add hosts and switches to a
# running emulation.
# Due to technical limitations it is NOT possible to create a link
# between a switch and a host if these are emulated at DIFFERENT workers
# This limitation does (of course) NOT hold for links between switches.
#
# Dynamic adding and removing of nodes also does not work when using the
# UserSwitch.


import time

from mininet.topo import Topo
from mininet.node import OVSSwitch

from MaxiNet.Frontend import maxinet
from MaxiNet.tools import Tools


# create topology
topo = Topo()
topo.addHost("h1", ip=Tools.makeIP(1), mac=Tools.makeMAC(1))
topo.addHost("h2", ip=Tools.makeIP(2), mac=Tools.makeMAC(2))
topo.addSwitch("s1", dpid=Tools.makeDPID(1))
topo.addLink("h1", "s1")
topo.addLink("h2", "s1")

# start cluster
cluster = maxinet.Cluster(minWorkers=5, maxWorkers=5)

# start experiment with OVSSwitch on cluster
exp = maxinet.Experiment(cluster, topo, switch=OVSSwitch)
exp.setup()

print "waiting 5 seconds for routing algorithms on the controller to converge"
time.sleep(5)

print "pinging h2 from h1 to check network connectivity..."
print exp.get_node("h1").cmd("ping -c 5 10.0.0.2")  # show network connectivity

raw_input("[Continue]")  # wait for user to acknowledge network connectivity
print "adding switch on second worker..."
# Enforce placement
exp.addSwitch("s2", dpid=Tools.makeDPID(2), wid=1)
print "adding hosts h3 and h4 on second worker..."
# Enforce placement of h3 on worker of s2.
# Remember: we cannot have tunnels between hosts and switches
exp.addHost("h3", ip=Tools.makeIP(3), max=Tools.makeMAC(3), pos="s2")
exp.addHost("h4", ip=Tools.makeIP(4), max=Tools.makeMAC(4), pos="s2")
# autoconf parameter configures link-attachment etc for us
exp.addLink("s2", "s1", autoconf=True)
exp.addLink("s2", "h4", autoconf=True)
exp.addLink("s2", "h3", autoconf=True)
time.sleep(2)

print "pinging h4 and h1 from h3 to check connectivity of new host..."
# show network connectivity of new hosts
print exp.get("h3").cmd("ping -c5 10.0.0.4")
print exp.get("h3").cmd("ping -c5 10.0.0.1")
raw_input("[Done 2]")

#Force placemennt of s3 on Worker 3. Otherwise random worker would be chosen
exp.addSwitch("s3", dpid=Tools.makeDPID(3), wid=2)
print "adding hosts h5 and h6 on third worker..."
# Enforce placement of h5 on worker of s3.
# Remember: we cannot have tunnels between hosts and switches
exp.addHost("h5", ip=Tools.makeIP(5), max=Tools.makeMAC(5), pos="s3")
exp.addHost("h6", ip=Tools.makeIP(6), max=Tools.makeMAC(6), pos="s3")
# autoconf parameter configures link-attachment etc for us
exp.addLink("s3", "s1", autoconf=True)
exp.addLink("s3", "h5", autoconf=True)
exp.addLink("s3", "h6", autoconf=True)
time.sleep(2)

print "pinging h5 and h1 from h3 to check connectivity of new host..."
# show network connectivity of new hosts
print exp.get("h5").cmd("ping -c5 10.0.0.4")
print exp.get("h5").cmd("ping -c5 10.0.0.1")
raw_input("[Done 3]")
#Force placemennt of s4 on Worker 4. Otherwise random worker would be chosen
exp.addSwitch("s4", dpid=Tools.makeDPID(4), wid=3)
print "adding hosts h7 and h8 on fourth worker..."
# Enforce placement of h7 on worker of s4.
# Remember: we cannot have tunnels between hosts and switches
exp.addHost("h7", ip=Tools.makeIP(7), max=Tools.makeMAC(7), pos="s4")
exp.addHost("h8", ip=Tools.makeIP(8), max=Tools.makeMAC(8), pos="s4")
# autoconf parameter configures link-attachment etc for us
exp.addLink("s4", "s1", autoconf=True)
exp.addLink("s4", "h7", autoconf=True)
exp.addLink("s4", "h8", autoconf=True)
time.sleep(2)

print "pinging h7 and h1 from h8 to check connectivity of new host..."
# show network connectivity of new hosts
print exp.get("h7").cmd("ping -c5 10.0.0.8")
print exp.get("h7").cmd("ping -c5 10.0.0.1")
raw_input("[Done 4]")

#Force placemennt of s5 on Worker 5. Otherwise random worker would be chosen
exp.addSwitch("s5", dpid=Tools.makeDPID(5), wid=4)
print "adding hosts h5 and h6 on third worker..."
# Enforce placement of h9 on worker of s5.
# Remember: we cannot have tunnels between hosts and switches
exp.addHost("h9", ip=Tools.makeIP(9), max=Tools.makeMAC(9), pos="s5")
exp.addHost("h10", ip=Tools.makeIP(10), max=Tools.makeMAC(10), pos="s5")
# autoconf parameter configures link-attachment etc for us
exp.addLink("s5", "s1", autoconf=True)
exp.addLink("s5", "h9", autoconf=True)
exp.addLink("s5", "h10", autoconf=True)
time.sleep(2)

print "pinging h10 and h9 from h9 to check connectivity of new host..."
# show network connectivity of new hosts
print exp.get("h9").cmd("ping -c5 10.0.0.10")
print exp.get("h9").cmd("ping -c5 10.0.0.1")
raw_input("[Done 5]")

