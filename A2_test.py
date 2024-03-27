
import subprocess

def enter_vtysh_config_mode(container_name):
    # Execute docker command to enter vtysh shell and config mode
    docker_command = ['docker', 'exec', '-it', container_name, 'vtysh', '-c', 'configure terminal']
    try:
        result = subprocess.run(docker_command, check=True, capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        
# Call the function with the container name
enter_vtysh_config_mode('clab-frrlab-router2')
