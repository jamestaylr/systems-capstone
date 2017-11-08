from openstack import connection 

# Set to true for print statements
debugMode = True

# Prints and returns a list of the instances on a given host
def getInstancesOnHost(hostname, conn):
	if debugMode: 
		print("instances on " + hostname + ": ")

	instances = []
	
	for server in conn.compute.servers(): 
		if server.hypervisor_hostname ==  hostname:
			instances.append(server)
			if debugMode: 
				print("  " + server.name + " (" + server.id + ")")
	
	return instances

# Prints all the instances and the hosts they are on 
def printInstances():
	print("all instances: ")
	for server in conn.compute.servers():
		print("  " + server.name + " on " + server.hypervisor_hostname)

if __name__ == "__main__":
	# copied from create_instance.py
	conn = connection.from_config(cloud_name='devstack-admin')
	
	getInstancesOnHost("capstone0", conn); 
	getInstancesOnHost("capstone1", conn); 
	getInstancesOnHost("capstone2", conn); 
	getInstancesOnHost("capstone3", conn); 
	getInstancesOnHost("capstone4", conn); 

	printInstances()
