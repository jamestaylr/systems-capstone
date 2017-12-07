import os
from openstack import connection
import argparse
import subprocess

fid = 3
AZ="mainag"
KEYPAIR_NAME = "demo"
PRIVATE_KEYPAIR_FILE = "~/devstack/id_rsa_demo"

def create_keypair(conn):
	keypair = conn.compute.find_keypair(KEYPAIR_NAME)
	keypair_exists = False
	for keypair in conn.compute.keypairs():
    		if keypair.name == KEYPAIR_NAME:
 		       	keypair_exists = True

	if keypair_exists:
    		print('Keypair ' + KEYPAIR_NAME + ' already exists. Skipping import.')
		return keypair
	
	else:
    		print('adding keypair...')
    	pub_key_file = open(os.path.expanduser(PRIVATE_KEYPAIR_FILE)).read()
    	keypair_args = {
    	    "name": KEYPAIR_NAME,
    	    "public_key": pub_key_file
   	 }
    	keypair = conn.compute.create_keypair(**keypair_args)

	return keypair

def create_sec_group(conn):
	print('Checking for existing security group...')
	security_group_name = 'all-in-one'
	security_group_exists = False
	for security_group in conn.network.security_groups():
	    if security_group.name == security_group_name:
        	all_in_one_security_group = security_group
        	security_group_exists = True		

	if security_group_exists:
    		print('Security Group ' + all_in_one_security_group.name + ' already exists. Skipping creation.')
		return all_in_one_security_group
	security_group_args = {
        	'name' : security_group_name,
        	'description': 'network access for all-in-one application.'
    	}
   	all_in_one_security_group = conn.network.create_security_group(**security_group_args)

    	security_rule_args = {
        	'security_group_id': all_in_one_security_group,
        	'direction': 'ingress',
        	'protocol': 'tcp',
        	'port_range_min': '80',
        	'port_range_max': '80'
    	}
    	conn.network.create_security_group_rule(**security_rule_args)

    	security_rule_args['port_range_min'] = '22'
    	security_rule_args['port_range_max'] = '22'
    	conn.network.create_security_group_rule(**security_rule_args)

	for security_group in conn.network.security_groups():
		print(security_group)
	return all_in_one_security_group



def create_keypair(conn):
        keypair = conn.compute.find_keypair(KEYPAIR_NAME)
        keypair_exists = False
        for keypair in conn.compute.keypairs():
                if keypair.name == KEYPAIR_NAME:
                        keypair_exists = True

        if keypair_exists:
                print('Keypair ' + KEYPAIR_NAME + ' already exists. Skipping import.')
                return keypair

        else:
                print('adding keypair...')
        pub_key_file = open(os.path.expanduser(PRIVATE_KEYPAIR_FILE)).read()
        keypair_args = {
            "name": KEYPAIR_NAME,
            "public_key": pub_key_file
         }
        keypair = conn.compute.create_keypair(**keypair_args)

        return keypair

def create_sec_group(conn):
        print('Checking for existing security group...')
        security_group_name = 'all-in-one'
        security_group_exists = False
        for security_group in conn.network.security_groups():
            if security_group.name == security_group_name:
                all_in_one_security_group = security_group
                security_group_exists = True

        if security_group_exists:
                print('Security Group ' + all_in_one_security_group.name + ' already exists. Skipping creation.')
                return all_in_one_security_group
        security_group_args = {
                'name' : security_group_name,
                'description': 'network access for all-in-one application.'
        }
        all_in_one_security_group = conn.network.create_security_group(**security_group_args)

        security_rule_args = {
                'security_group_id': all_in_one_security_group,
                'direction': 'ingress',
                'protocol': 'tcp',
                'port_range_min': '80',
                'port_range_max': '80'
        }
        conn.network.create_security_group_rule(**security_rule_args)

        security_rule_args['port_range_min'] = '22'
        security_rule_args['port_range_max'] = '22'
        conn.network.create_security_group_rule(**security_rule_args)

        for security_group in conn.network.security_groups():
                print(security_group)
        return all_in_one_security_group

def setup_floating(conn, testing_instance):
        print('Checking if Floating IP is already assigned to testing_instance...')
        testing_instance_floating_ip = None
        for values in testing_instance.addresses.values():
            for address in values:
                if address['OS-EXT-IPS:type'] == 'floating':
                    testing_instance_floating_ip = conn.network.find_ip(address['addr'])

        unused_floating_ip = None
        if not testing_instance_floating_ip:
                print('Checking for unused Floating IP...')
                for floating_ip in conn.network.ips():
                        if not floating_ip.fixed_ip_address:
                                unused_floating_ip = floating_ip
                                break
        if not testing_instance_floating_ip and not unused_floating_ip:
                print('No free unused Floating IPs. Allocating new Floating IP...')
                public_network_id = conn.network.find_network('public').id
                try:
                        unused_floating_ip = conn.network.create_ip(floating_network_id=public_network_id)
                        unused_floating_ip = conn.network.get_ip(unused_floating_ip)
                        print(unused_floating_ip)
                except exceptions.HttpException as e:
                        print(e)


        if testing_instance_floating_ip:
            print('Instance ' + testing_instance.name + ' already has a public ip. Skipping attachment.')
        else:
                for port in conn.network.ports():
                        if port.device_id == testing_instance.id:
                                testing_instance_port = port
                                print(port)
                                testing_instance_floating_ip = unused_floating_ip
		                setattr(testing_instance_floating_ip, 'port_id', testing_instance_port.id)
				
				#cli as a backup
				subprocess.call(['openstack', 'floating', 'ip', 'create','--port', testing_instance_port.id, 'public'])	


#parsing args
parser = argparse.ArgumentParser(description='Creating a new instance in this aggregate zone.')
parser.add_argument('-n', dest='name',  default='newinstance',
	    help='name of new instance! (default: newinstance')

args = parser.parse_args()
INSTANCENAME = args.name

#create a connection object for the given cloud - devstack (found in clouds.yaml)
# so we're creating with user admin
conn = connection.from_config(cloud_name='devstack-admin')

#get private network
network_uuid = ""
for network in conn.network.networks():
	if network.name == "private":
		network_uuid = network.id

#network is private
networks=[{"uuid": network_uuid}]


#image id (cirros)
for image in conn.compute.images():
        iid = image.id

#security group
security_group_name = "default"
for security_group in conn.network.security_groups():
            if security_group.name == security_group_name:
                sec_group  = security_group

#create instance 1
# auto creates with the availability zone that the node you're running on is currently a part of 
instance1 = conn.compute.create_server(name=INSTANCENAME, flavor_id=fid, image_id=iid, key_name=KEYPAIR_NAME, networks=networks, availability_zone=AZ)
instance1 = conn.compute.wait_for_server(instance1)
#conn.compute.add_security_group_to_server(server=instance1, security_group=sec_group)
setup_floating(conn, instance1)
print(instance1)

#conn.compute.delete_server(instance1)
