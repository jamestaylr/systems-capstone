
from openstack import connection

# generate with: openstack keypair create mykey --private-key mykeyfile
KEYPAIR_NAME = "mykey"
PRIVATE_KEYPAIR_FILE = "~/devstack/mykeyfile"


def create_keypair(conn):
    keypair = conn.compute.find_keypair(KEYPAIR_NAME)

    if not keypair:
        print("Create Key Pair:")

        keypair = conn.compute.create_keypair(name=KEYPAIR_NAME)

        print(keypair)

        try:
            os.mkdir(SSH_DIR)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e

        with open(PRIVATE_KEYPAIR_FILE, 'w') as f:
            f.write("%s" % keypair.private_key)

        os.chmod(PRIVATE_KEYPAIR_FILE, 0o400)

    return keypair


#create a connection object for the given cloud - devstack (found in clouds.yaml)
# so we're creating with user admin
conn = connection.from_config(cloud_name='devstack-admin')

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

#keypair
keypair = create_keypair(conn)


#create instance 1
# auto creates with the availability zone that the node you're running on is currently a part of 
instance1 = conn.compute.create_server(name='instance1', flavor_id=fid, image_id=iid, key_name=keypair.name)
instance1 = conn.compute.wait_for_server(instance1)

print(instance1)

#conn.compute.delete_server(instance1)
