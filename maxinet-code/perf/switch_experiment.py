import itertools
import threading
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

    def expr_node(self, node):
        return self.get_node('s{}'.format(node._sid))

    def test_link(self, link):
        src, dest = link
        src_node = self._switches[src]
        dest_node = self._switches[dest]
        self.expr_node(src_node).cmd('ping -c 5 {}'.format(dest_node._ip_addr))
        self.expr_node(dest_node).cmd('ping -c 5 {}'.format(src_node._ip_addr))

    def ping_all(self):
        for src, dest in self.links:
            src_node = self._switches[src]
            dest_node = self._switches[dest]
            logging.info('Testing link {} ({}) <-> {} ({})'.format(
                src_node._sid,
                src_node._ip_addr,
                dest_node._sid,
                dest_node._ip_addr,
            ))
            self.expr_node(src_node).cmd('ping -c 5 {}'.format(dest_node._ip_addr))
            self.expr_node(dest_node).cmd('ping -c 5 {}'.format(src_node._ip_addr))

        for i in range(0, len(self._switches)):
            for srcs in itertools.permutations(self._switches.keys(), i):
                dests = set(self._switches.keys()) - set(srcs)
                links = [(s, d) for s, d in self.links \
                        if (s in srcs and d in dests) \
                            or (d in srcs and s in srcs)]
                if links == []:
                    continue

                logging.info('Concurrently testing: {}'.format(links))
                threads = []
                for link in links:
                    t = threading.Thread(target=self.test_link, args=(link,))
                    t.start()
                    threads.append(t)

                for t in threads:
                    t.join()
