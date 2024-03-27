
import subprocess

def enter_vtysh_config_mode(container_name):
    # Construct the docker command to enter vtysh shell and config mode
    docker_command = ['docker', 'exec', '-it', container_name, 'vtysh', '-c', 'configure terminal']

    # Execute the command to enter configuration mode
    subprocess.run(docker_command, capture_output=True, text=True)

    # Now, execute a command to add a dummy loopback interface configuration
    docker_command = ['docker', 'exec', '-it', container_name, 'vtysh', '-c', 'interface lo0', '-c', 'description Dummy Loopback']
    result = subprocess.run(docker_command, capture_output=True, text=True)
    
    # Print the output and error
    print("Output:", result.stdout)
    print("Error:", result.stderr)

# Call the function with the container name
enter_vtysh_config_mode('clab-frrlab-router2')
