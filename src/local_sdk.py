
from openstack import connection
import time
#create a connection object for the given cloud - devstack (found in clouds.yaml)
conn = connection.from_config(cloud_name='devstack')

#flavor id (1= m1.tiny)
fid = '1'

#image id (cirros)
for image in conn.compute.images():
	iid = image.id
#create instance 1
instance1 = conn.compute.create_server(name='instance1', flavor_id=fid, image_id=iid)

#create instane 2
instance2 = conn.compute.create_server(name='instance2', flavor_id=fid, image_id=iid, availability_zone='az-capstone4')

print(instance1)
print(instance2)

#conn.compute.delete_server(instance1)
#conn.compute.delete_server(instance2)

time.sleep(1000)
