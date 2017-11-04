
from openstack import connection

#create a connection object for the given cloud - devstack (found in clouds.yaml)
conn = connection.from_config(cloud_name='devstack')

#flavor id (1= m1.tiny)
fid = '1'

#image id (cirros)
iid = '20f69164-a011-4454-8eea-c1dd6ea5b181'
#create instance 1
instance1 = conn.compute.create_server(name='instance1', flavor_id=fid, image_id=iid)

print(instance1)

conn.compute.delete_server(instance1)
