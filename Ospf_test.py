
from pyats.topology import loader
from pyats import aetest
from netmiko import ConnectHandler
import types

def _send_command(ssh, *args, **kwargs):
    kwargs.update(expect_string=r'[^\n]\S+#\W$')
    return ssh.send_command(*args, **kwargs)

def enter_vtysh_root(handler):
    prompt = handler.find_prompt()
    is_config_mode = '(config' in prompt  #checks if initially in config mode
    if not getattr(handler, 'is_wrapped', False):
        handler.send_command_frr = types.MethodType(_send_command, handler)
        handler.is_wrapped = True
    while '(config' in prompt:
        handler.send_command('exit', expect_string=r'[^\n]\S+#\W$')
        prompt = handler.find_prompt()
    if is_config_mode:
        # we have reached the vtysh root using exit command(s)
        return
    #if we are in linux prompt do the following
    handler.send_command('vtysh', expect_string=r'[^\n]\S+#\W$')


def enter_config_root(handler):
    prompt = handler.find_prompt()
    is_config_mode = '(config' in prompt  #checks if initially in config mode
    while '(config' in prompt and '(config)' not in prompt:
        handler.send_command('exit', expect_string=r'[^\n]\S+#\W$')
        prompt = handler.find_prompt()
    if is_config_mode:
        # we have reached the vtysh root using exit command(s)
        return
    #if we are in vtysh root, do the following
    handler.send_command('configure terminal', expect_string=r'[^\n]\S+#\W$')
    assert '(config' in handler.find_prompt(), 'Failed to enter config mode from vtysh'

class OSPFTest(aetest.Testcase):

    @aetest.setup
    def setup(self):
        # Load testbed and connect to device
        self.testbed = loader.load('testbed.yaml')
        self.device = self.testbed.devices['device']
        self.device.connect()

    @aetest.test
    def test_enter_vtysh_root(self):
        enter_vtysh_root(self.device)

    @aetest.test
    def test_enter_config_root(self):
        enter_config_root(self.device)

    @aetest.cleanup
    def cleanup(self):
        self.device.disconnect()

if __name__ == '__main__':
    # Execute the test script
    aetest.main()
