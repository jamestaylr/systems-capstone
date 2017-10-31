import time
import logging

from MaxiNet.Frontend.maxinet import Experiment

class SwitchExperiment(Experiment):
    links = set()

    def __init__(self, cluster, topology, switches, *args, **kwargs):
        super(SwitchExperiment, self).__init__(cluster, topology, *args, **kwargs)
        logging.info('Setting up experiment and monitoring...')
        self.setup()
        self.monitor()
        time.sleep(5)

        self._switches = switches
        logging.info('Building switch links...')
        for switch in switches.values():
            switch.expr = self
            switch.create_switch()

        for switch in switches.values():
            switch.build_links()

    def permute(self):
        v = self._switches.values()
        for sink, sources in [(v[i], v[i+1:] + v[:i]) for i in range(len(v))]:
            time.sleep(10)
            pass
