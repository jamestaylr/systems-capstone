import time
import logging

from MaxiNet.tools import Tools

class SwitchNode():
    def __init__(self, switch_id, worker_id, children):
        self._sid = switch_id
        self._wid = worker_id
        self._children = children

    def build_links(self):
        for child in self._children:
            if (self._sid, child) not in self.expr.links:
                self.create_link_with(child)
                self.expr.links.add((child, self._sid))

    # Build the switch on the worker
    def create_switch(self):
        switch_name = 's{}'.format(self._sid)
        host_name = 'h{}'.format(self._sid)
        self.expr.addSwitch(switch_name,
            dpid=Tools.makeDPID(self._sid), wid=self._wid)
        self.expr.addHost(host_name,
            ip=Tools.makeIP(self._sid), max=Tools.makeMAC(self._sid),
            pos=switch_name)
        self.expr.addLink(switch_name, host_name, autoconf=True)

        logging.info('Created switch {} on worker {}'.format(
            self._sid, self._wid + 1))
        time.sleep(2)

    def create_link_with(self, link_switch):
        switch_name_1 = 's{}'.format(self._sid)
        switch_name_2 = 's{}'.format(link_switch)
        self.expr.addLink(switch_name_1, switch_name_2, autoconf=True)
        logging.info('Built link: {} <-> {}'.format(self._sid, link_switch))
        time.sleep(2)
