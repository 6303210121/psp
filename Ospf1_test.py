
import subprocess
from pyats import aetest
from pyats.topology import loader
from ospf_lib import enter_vtysh_root, enter_config_root

class OSPFTest(aetest.Testcase):

    @aetest.setup
    def setup(self):
        # Load testbed and connect to device
        self.testbed = loader.load('testbed.yaml')
        self.device = self.testbed.devices['router']
        self.device.connect()

    @aetest.test
    def test_enter_vtysh_root(self):
        enter_vtysh_root(self.device)

    @aetest.test
    def test_enter_config_root(self):
        enter_config_root(self.device)

    @aetest.test
    def test_run_docker_command(self):
        # Run the docker command
        docker_command = ['docker', 'exec', '-it', 'clab-frrlab-router2', '/bin/bash']
        subprocess.run(docker_command)

    @aetest.cleanup
    def cleanup(self):
        # Disconnect from the device
        if hasattr(self, 'device') and hasattr(self.device, 'is_connected') and self.device.is_connected():
            self.device.disconnect()

if __name__ == '__main__':
    # Execute the test script
    aetest.main()
