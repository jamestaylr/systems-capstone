#!/usr/bin/env python3
import time
import logging
from threading import Thread

from typing import List

from mininet.topo import Topo
from mininet.node import OVSSwitch
from MaxiNet.Frontend.maxinet import Cluster, Experiment
from MaxiNet.tools import Tools

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def parse_ping_results(output):
    for line in output.splitlines():
        for t in [s for s in line.split() if 'time=' in s]:
            time = float(t.split('=')[-1])
            times.append(time)
    return sum(times) / len(times)

links = set()

class SwitchNode():
    def __init__(self, switch_id: int, worker_id: int, children: List[int]):
        self._sid = switch_id
        self._wid = worker_id
        self.create_switch()
        self._children = children
        logger.debug('Created switch {} on worker {}'.format(
            self._sid, self._wid))
        

    def build_links():
        for child in self._children:
            if (self._sid, child) not in links
                self.create_link_with(child)
                links.add((child, self._sid))

    # Build the switch on the worker
    def create_switch(self) -> None:
        switch_name = 's{}'.format(self._sid)
        host_name = 'h{}'.format(self._sid)
        expr.addSwitch(switch_name,
            dpid=Tools.makeDPID(switch_id), wid=self._wid)
        expr.addHost(host_name,
            ip=Tools.makeIP(self._sid), max=Tools.makeMAC(self._sid),
            pos=switch_name)
        expr.addLink(switch_name, host_name, autoconf=True)
        time.sleep(2)

    def create_link_with(self, link_switch: int) -> None:
        switch_name_1 = 's{}'.format(self._sid)
        switch_name_2 = 's{}'.format(link_switch)
        expr.addLink(switch_name_1, switch_name_2, autoconf=True)
        logger.debug('Built link: {} <-> {}'.format(self._sid, link_switch))
        time.sleep(2)


class SwitchExperiment(Experiment):
    def __init__(self, cluster, topology, switches, *args, **kwargs):
        super().__init__(cluster, topology, *args, **kwargs)
        logger.debug('Setting up experiment and monitoring...')
        self.setup()
        self.monitor()
        time.sleep(5)

        self._switches = switches
        logger.debug('Building switch links...')
        for switch in switches.values():
            switch.build_links()

    def permute():
        v = self._switches.values()
        for sink, *sources in [v[i:] + v[:i] for i in range(len(v))]:
            time.sleep(10)
            pass

# Create the experiment
switches = {
    1: SwitchNode(1, 0, [3]),
    2: SwitchNode(2, 0, [3]),
    3: SwitchNode(3, 1, [1, 2, 4, 5]),
    4: SwitchNode(4, 1, [3]),
    5: SwitchNode(5, 1, [3]),
}
expr = SwitchExperiment(Cluster(), Topo(), switches, switch=OVSSwitch)

def iperf_ping(string):
    pass

t = threading.Thread(target=iperf_ping, args=['hello'])
