from openstack import connection
from novaclient import client
import os_client_config
import sys

#helper function to get the hostname from the host id
#assuptions- all instances come from same project/cloud
def gethostn(id):
        name = ''
        if (id == 'aaa42642a90d9ba95e16db9a50cfe9c9e4706cb6a7aaa33be2995cd1'):
                name = 'capstone0'
        if (id == '013dfd300c014ce94b7e7a6a977b19d9f20272312925b9d1ca36488b'):
                name = 'capstone1'
        if (id == '2c99511cac82792db0da7e39f55236a37f017f0868c5494f547ced53'):
                name = 'capstone2'
        if (id == 'c2918820cbd8131b9955fe1fa7c28f1bc89eb275deacca9dbc0b6694'):
                name = 'capstone3'
        if (id == '8184e99bfcc828d5db19e0ad09e962b97411f0208c3530b28df5ae29'):
                name = 'capstone4'

        return name


def getHostId(name):
        id = ''
        if (name == 'capstone0'):
                id = 'aaa42642a90d9ba95e16db9a50cfe9c9e4706cb6a7aaa33be2995cd1')
        if (name == 'capstone1'):
                id = '013dfd300c014ce94b7e7a6a977b19d9f20272312925b9d1ca36488b'
        if (name == 'capstone2'):
                id = '2c99511cac82792db0da7e39f55236a37f017f0868c5494f547ced53'
        if (name == 'capstone3'):
                id = 'c2918820cbd8131b9955fe1fa7c28f1bc89eb275deacca9dbc0b6694'
        if (name == 'capstone4'):
                id = '8184e99bfcc828d5db19e0ad09e962b97411f0208c3530b28df5ae29'
        return id


def main():
        #create a connection object for the given cloud - devstack (found in clouds.yaml)
        # so we're creating with user admin
        conn = connection.from_config(cloud_name='devstack-admin')
        nova = os_client_config.make_client('compute', cloud='devstack-admin')
        #list servers and delete all of them (if wanted)
        #print("List Servers:")

        id = 'fbd6f273-579b-427e-b8fd-1993cb897170' #id of im1- an instance i made for testing
        tomove= nova.servers.get(id)

        if (len(sys.argv > 1):
                hid = getHostId(sys.argv[1])
                #print(dir(tomove))
                for server in nova.servers.list():
                        #print(server)
                        if (server.hostId == hid):
                                tomove = server
                                break

        # list networks
        #print("list networks: ")


        #flavor id (1= m1.tiny)
        fid = '1'

        #image id (cirros)
        for image in conn.compute.images():
                iid = image.id

        #if not specified - put on capstone4
        destname = 'capstone4'
        if (len(sys.argv) >= 3):
                destname = sys.argv[2]
        print(nova.servers.list())
        #print(dir(tomove))
        print(tomove.hostId)
        print('now migrate')
        tomove.live_migrate(host=destname, block_migration=True)

if __name__ == "__main__":
        main()
