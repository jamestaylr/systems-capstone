#!/usr/bin/env python2
import logging
import sys
from switch_node import SwitchNode
from switch_experiment import SwitchExperiment
from MaxiNet.Frontend.maxinet import Cluster
from mininet.topo import Topo
from mininet.node import OVSSwitch


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create the experiment
if (len(sys.argv) < 2):
	print "Name the topology: fork, star, mesh, or tree"
else:
	if (sys.argv[1] == "star"):
		switches = {
    			1: SwitchNode(1, 0, [3]),
    			2: SwitchNode(2, 0, [3]),
    			3: SwitchNode(3, 0, [1, 2, 4, 5, 6, 7]),
    			4: SwitchNode(4, 1, [3]),
    			5: SwitchNode(5, 1, [3]),
			6: SwitchNode(6, 1, [3]),
			7: SwitchNode(7, 1, [3]),
		}
        	expr = SwitchExperiment(Cluster(), Topo(), switches, switch=OVSSwitch)
        	expr.ping_all()

	elif (sys.argv[1] == "mesh"):
                switches = {
                        1: SwitchNode(1, 0, [2, 3, 4, 5, 6, 7]),
                        2: SwitchNode(2, 0, [1, 3, 4, 5, 6, 7]),
                        3: SwitchNode(3, 0, [1, 2, 4, 5, 6, 7]),
                        4: SwitchNode(4, 1, [1, 2, 3, 5, 6, 7]),
                        5: SwitchNode(5, 1, [1, 2, 3, 4, 6, 7]),
			6: SwitchNode(6, 1, [1, 2, 3, 4, 5, 7]),
			7: SwitchNode(7, 1, [1, 2, 3, 4, 5, 6]),
                }
	        expr = SwitchExperiment(Cluster(), Topo(), switches, switch=OVSSwitch)
	        expr.ping_all()

	elif (sys.argv[1] == "fork"):
                switches = {
                        1: SwitchNode(1, 0, [2, 3]),
                        2: SwitchNode(2, 0, [1]),
                        3: SwitchNode(3, 0, [1, 4, 6]),
                        4: SwitchNode(4, 1, [3, 5]),
                        5: SwitchNode(5, 1, [4]),
			6: SwitchNode(6, 1, [3, 7]),
			7: SwitchNode(7, 1, [6])
                }
	        expr = SwitchExperiment(Cluster(), Topo(), switches, switch=OVSSwitch)
       		expr.ping_all()

	else: #assume tree
                switches = {
                        1: SwitchNode(1, 0, [3, 4, 5]),
                        2: SwitchNode(2, 0, [3, 6, 7]),
                        3: SwitchNode(3, 0, [1, 2]),
                        4: SwitchNode(4, 1, [1]),
                        5: SwitchNode(5, 1, [1]),
			6: SwitchNode(6, 1, [2]),
			7: SwitchNode(7, 1, [2])
                }
	        expr = SwitchExperiment(Cluster(), Topo(), switches, switch=OVSSwitch)
	        expr.ping_all()

