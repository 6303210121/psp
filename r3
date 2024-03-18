
package main

import (
	"fmt"
	"os/exec"
	"testing"
)

func TestConnectToRouter16(t *testing.T) {
	// Command to list available containers
	psCommand := "docker ps"

	// Execute the command to list available containers
	psOutput, err := exec.Command("sh", "-c", psCommand).Output()
	if err != nil {
		fmt.Println("Error executing docker ps command:", err)
		return
	}

	// Print the output of the docker ps command
	fmt.Println("Available containers:")
	fmt.Println(string(psOutput))

	// Command to log in to bash shell of the container
	loginCommand := "docker exec clab-frrlab-router2 /bin/bash"

	// Execute the command to log in to the bash shell of the container
	loginOutput, err := exec.Command("sh", "-c", loginCommand).CombinedOutput()
	if err != nil {
		fmt.Println("Error logging in to the container:", err)
		return
	}

	// Print the output of the login command
	//fmt.Println("Login output:")
	fmt.Println(string(loginOutput))

	// Command to log in to vtysh
	vtyshCommand := "vtysh"

	// Execute the command to log in to vtysh within the container's environment
	vtyshOutput, err := exec.Command("sh", "-c", loginCommand+" -c '"+vtyshCommand+"'").CombinedOutput()
	if err != nil {
		fmt.Println("Error logging in to vtysh:", err)
		return
	}

	// Print the output of the vtysh command
	fmt.Println("vtysh output:")
	fmt.Println(string(vtyshOutput))

	// Command to show running configuration
	showConfigCommand := "configure"

	// Execute the command to show running configuration within the container's environment
	showConfigOutput, err := exec.Command("sh", "-c", loginCommand+" -c '"+vtyshCommand+" -c \""+showConfigCommand+"\"'").CombinedOutput()
	if err != nil {
		fmt.Println("Error showing running configuration:", err)
		return
	}

	// Print the output of the show running-config command
	fmt.Println("Running configuration:")
	fmt.Println(string(showConfigOutput))

}

=======================================================================
=== RUN   TestConnectToRouter16
Available containers:
CONTAINER ID   IMAGE                             COMMAND                  CREATED      STATUS      PORTS                                  NAMES
b76caafb7ed9   praqma/network-multitool:latest   "/bin/sh /docker/ent…"   3 days ago   Up 3 days   80/tcp, 443/tcp, 1180/tcp, 11443/tcp   clab-frrlab-PC3
e120d7e457b1   frrouting/frr:v7.5.1              "/sbin/tini -- /usr/…"   3 days ago   Up 3 days                                          clab-frrlab-router1
6e920533764d   frrouting/frr:v7.5.1              "/sbin/tini -- /usr/…"   3 days ago   Up 3 days                                          clab-frrlab-router3
45b66f9a311b   praqma/network-multitool:latest   "/bin/sh /docker/ent…"   3 days ago   Up 3 days   80/tcp, 443/tcp, 1180/tcp, 11443/tcp   clab-frrlab-PC1
c9752772f6db   praqma/network-multitool:latest   "/bin/sh /docker/ent…"   3 days ago   Up 3 days   80/tcp, 443/tcp, 1180/tcp, 11443/tcp   clab-frrlab-PC2
34f858a28b4d   frrouting/frr:v7.5.1              "/sbin/tini -- /usr/…"   3 days ago   Up 3 days                                          clab-frrlab-router2


vtysh output:
% Can't open configuration file /etc/frr/vtysh.conf due to 'No such file or directory'.

Hello, this is FRRouting (version 7.5.1_git).
Copyright 1996-2005 Kunihiro Ishiguro, et al.

router2# 

Running configuration:
% Can't open configuration file /etc/frr/vtysh.conf due to 'No such file or directory'.

--- PASS: TestConnectToRouter16 (0.42s)
PASS
ok  	command-line-arguments	0.426s


