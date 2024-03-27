
ospf_test.py
from pyats import aetest
from pyats.topology import loader
from ospf_lib import OSPFConfig, OSPFMonitor

class OSPFTest(aetest.Testcase):

    @aetest.setup
    def setup(self):
        # Load testbed and connect to device
        self.testbed = loader.load('testbed.yaml')
        self.device = self.testbed.devices['device']
        self.device.connect()

    @aetest.test
    def test_configure_ospf(self):
        ospf_config = OSPFConfig(self.device)
        ospf_config.configure_ospf(process_id='1', network='10.0.0.0 0.255.255.255', area='0')

    @aetest.test
    def test_monitor_ospf(self):
        ospf_monitor = OSPFMonitor(self.device)
        neighbors = ospf_monitor.get_ospf_neighbors()
        self.passed('OSPF neighbors: {}'.format(neighbors))

    @aetest.cleanup
    def cleanup(self):
        self.device.disconnect()

if __name__ == '__main__':
    aetest.main()
