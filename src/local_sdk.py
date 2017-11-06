
from openstack import connection

#create a connection object for the given cloud - devstack (found in clouds.yaml)
# so we're creating with user admin
conn = connection.from_config(cloud_name='devstack-admin')

#list servers and delete all of them (if wanted)
print("List Servers:")

for server in conn.compute.servers():
	print(server)
#	conn.compute.delete_server(server.id)

# list networks
print("list networks: ")
network_uuid = ""
for network in conn.network.networks():
	print(network)	
	if network.name == "public":
		network_uuid = network.id
		print("Found the public network!")

#flavor id (1= m1.tiny)
fid = '1'

#network is public
networks=[{"uuid": network_uuid}]

#image id (cirros)
for image in conn.compute.images():
	iid = image.id

#create instance 1

# auto creates with the availability zone that the node you're running on is currently a part of 
instance1 = conn.compute.create_server(name='instance1', flavor_id=fid, image_id=iid)
instance1 = conn.compute.wait_for_server(instance1)

#create instane 2
#instance2 = conn.compute.create_server(name='instance2', flavor_id=fid, image_id=iid, availability_zone='AZ1', networks=networks)
#instance2 = conn.compute.wait_for_server(instance2)

print(instance1)
#print(instance2)

#conn.compute.delete_server(instance1)
#conn.compute.delete_server(instance2)
