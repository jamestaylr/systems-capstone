#!/usr/bin/env python2
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create the experiment
switches = {
    1: SwitchNode(1, 0, [3]),
    2: SwitchNode(2, 0, [3]),
    3: SwitchNode(3, 1, [1, 2, 4, 5]),
    4: SwitchNode(4, 1, [3]),
    5: SwitchNode(5, 1, [3]),
}
expr = SwitchExperiment(Cluster(), Topo(), switches, switch=OVSSwitch)