
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


#########################################################################

package main

import (
    "fmt"
    "regexp"
    "strings"
)

// SSHHandler simulates an SSH connection handler
type SSHHandler struct {
    Prompt string
    ConfigMode bool
}

// SendCommand sends a command over SSH
func (ssh *SSHHandler) SendCommand(command string) string {
    // Simulating command execution and getting the output
    output := "Command output for: " + command
    
    // Update prompt if command changes the mode
    if strings.Contains(command, "exit") {
        ssh.Prompt = "New Prompt"
        ssh.ConfigMode = false
    } else if strings.Contains(command, "vtysh") {
        ssh.Prompt = "vtysh Prompt"
        ssh.ConfigMode = false
    } else if strings.Contains(command, "configure terminal") {
        ssh.Prompt = "Config Prompt"
        ssh.ConfigMode = true
    }
    
    return output
}

// FindPrompt returns the current prompt
func (ssh *SSHHandler) FindPrompt() string {
    return ssh.Prompt
}

// EnterVTYSHRoot enters the vtysh root mode
func EnterVTYSHRoot(ssh *SSHHandler) {
    for strings.Contains(ssh.Prompt, "(config") {
        ssh.SendCommand("exit")
    }
    if ssh.ConfigMode {
        return
    }
    ssh.SendCommand("vtysh")
}

// EnterConfigRoot enters the configuration mode
func EnterConfigRoot(ssh *SSHHandler) {
    for strings.Contains(ssh.Prompt, "(config") && !strings.Contains(ssh.Prompt, "(config)") {
        ssh.SendCommand("exit")
    }
    if ssh.ConfigMode {
        return
    }
    ssh.SendCommand("configure terminal")
    if !strings.Contains(ssh.Prompt, "(config") {
        fmt.Println("Failed to enter config mode from vtysh")
    }
}

func main() {
    // Create an instance of SSHHandler
    ssh := &SSHHandler{
        Prompt:      "Initial Prompt",
        ConfigMode: false,
    }

    // Example usage:
    EnterVTYSHRoot(ssh)
    fmt.Println("Prompt after entering vtysh root:", ssh.FindPrompt())

    EnterConfigRoot(ssh)
    fmt.Println("Prompt after entering config mode:", ssh.FindPrompt())
}

