
import subprocess

def enter_vtysh_config_mode(container_name):
    # Construct the docker command to enter vtysh shell and config mode
    docker_command = ['docker', 'exec', '-it', container_name, 'vtysh', '-c', 'show running-config']

    try:
        # Execute the command
        result = subprocess.run(docker_command, capture_output=True, text=True, check=True)

        # Print the output
        print("Output:", result.stdout)

    except subprocess.CalledProcessError as e:
        # Print any errors
        print("Error:", e.stderr)

# Call the function with the container name
enter_vtysh_config_mode('clab-frrlab-router2')
