
import subprocess
from pyats import topology

# Load testbed from testbed.yaml file
testbed = topology.loader.load('testbed.yaml')

# Access devices from the testbed
router1 = testbed.devices['clab-frrlab-router1']
router2 = testbed.devices['clab-frrlab-router2']
router3 = testbed.devices['clab-frrlab-router3']
pc1 = testbed.devices['clab-frrlab-PC1']
pc2 = testbed.devices['clab-frrlab-PC2']
pc3 = testbed.devices['clab-frrlab-PC3']

# Print device details for verification
print(router1)
print(router2)
print(router3)
print(pc1)
print(pc2)
print(pc3)

# Execute docker command
docker_command = ['docker', 'exec', '-it', 'clab-frrlab-router2', '/bin/bash']
subprocess.run(docker_command)
