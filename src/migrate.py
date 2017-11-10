from openstack import connection
from novaclient import client
import os_client_config
import sys
import argparse

def main():
	parser = argparse.ArgumentParser(description='Migrate a random instance from host x to host y.')
	parser.add_argument('--dest', dest='host_to_move_to',  default='capstone1',
                    help='hostname destination to move to (default: capstone1')
	parser.add_argument('--source', dest='host_to_move_from',  default='capstone0',
                    help='hostname source (default: capstone0')


	args = parser.parse_args()
	host_to_move_to = args.host_to_move_to
	host_to_move_from = args.host_to_move_from


        #create a connection object for the given cloud - devstack (found in clouds.yaml)
        # so we're creating with user admin
        conn = connection.from_config(cloud_name='devstack-admin')
        nova = os_client_config.make_client('compute', cloud='devstack-admin')

	# finding the server to move -----------------

	server_to_move = None
	for server in nova.servers.list():
		# check that the hostname is the same
		dd = server.to_dict()
		if (dd['OS-EXT-SRV-ATTR:host'] == host_to_move_from):
			server_to_move = server
			break


	# other variables ---------------------------

	# flavor id. we're using "tiny" by default
        fid = '1'

        #image id (cirros): there's only one 
        iid = conn.compute.images().next().id

	# destination host logic -------------------

        if server_to_move == None:
		print "There are no servers on " + host_to_move_from
		sys.exit()
		
	print("now migrating " + server_to_move.human_id + " to: " + host_to_move_to)
	print("that's id: " + str(server_to_move.id))
        server_to_move.live_migrate(host=host_to_move_to, block_migration=True)

if __name__ == "__main__":
        main()
