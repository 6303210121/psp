
import netmiko
import types
import pdb


def _send_command(ssh, *args, **kwargs):
    kwargs.update(expect_string=r'[^\n]\S+#\W$')
#    pdb.set_trace()
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



