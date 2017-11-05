# controller & compute nodes

### floating ips

**Update 10/29**: Based on a suggestion by James, we're using 192.168.2.0/24 for our subnet network address. 

**Update 10/30**: We are now using availability zones, not host aggregates.

### local.conf for the controller node

```
[[local|localrc]]

ADMIN_PASSWORD=maxinet
DATABASE_PASSWORD=maxinet
RABBIT_PASSWORD=maxinet
SERVICE_PASSWORD=$ADMIN_PASSWORD

HOST_IP=192.168.0.221                   # this is CONTROLLER ip

LOGFILE=$DEST/logs/stack.sh.log
LOGDAYS=2

SWIFT_HASH=66a3d6b56c1f479c8b4e70ab5c2000f5
SWIFT_REPLICAS=1
SWIFT_DATA_DIR=$DEST/data

FLOATING_RANGE=192.168.2.0/24           #important! need to have enough floating ips 

FLAT_INTERFACE=enp2s0                   #how we connect to internet
MULTI_HOST=1                            #turn on multi host
```


### local.conf for the compute node

This code is also linked to [here](https://github.com/jamestaylr/systems-capstone/blob/master/openstack-docs/compute-node-local-conf).

```
[[local|localrc]]
HOST_IP=192.168.0.223                              # CHANGE this per compute node
FLAT_INTERFACE=enp2s0
FIXED_RANGE=10.4.128.0/20
FIXED_NETWORK_SIZE=4096
FLOATING_RANGE=192.168.2.0/24                      # not sure if you need to change this
MULTI_HOST=1
LOGFILE=/opt/stack/logs/stack.sh.log
ADMIN_PASSWORD=maxinet
DATABASE_PASSWORD=maxinet
RABBIT_PASSWORD=maxinet
SERVICE_PASSWORD=maxinet
DATABASE_TYPE=mysql
SERVICE_HOST=192.168.0.221                         # CHANGE to ip of controller node
MYSQL_HOST=$SERVICE_HOST
RABBIT_HOST=$SERVICE_HOST
GLANCE_HOSTPORT=$SERVICE_HOST:9292
ENABLED_SERVICES=n-cpu,q-agt,n-api-meta,c-vol,placement-client
NOVA_VNC_ENABLED=True
NOVNCPROXY_URL="http://$SERVICE_HOST:6080/vnc_auto.html"
VNCSERVER_LISTEN=$HOST_IP
VNCSERVER_PROXYCLIENT_ADDRESS=$VNCSERVER_LISTEN
```

### getting set up

Run `./stack.sh` on the controller and any compute nodes.

On the controller node:
```
. openrc admin admin
nova service-list --binary nova-compute
```
Validate that all of the compute nodes show up. Expected output is similar to:
```
+--------------------------------------+--------------+-----------+------+---------+-------+----------------------------+-----------------+-------------+
| Id                                   | Binary       | Host      | Zone | Status  | State | Updated_at                 | Disabled Reason | Forced down |
+--------------------------------------+--------------+-----------+------+---------+-------+----------------------------+-----------------+-------------+
| 87b3dd00-19b5-42eb-89e8-3467a52e0a12 | nova-compute | capstone2 | nova | enabled | up    | 2017-10-27T15:48:29.000000 | -               | False       |
| c3d705de-f072-47a3-a579-793b98cc27fb | nova-compute | capstone4 | nova | enabled | up    | 2017-10-27T15:48:30.000000 | -               | False       |
+--------------------------------------+--------------+-----------+------+---------+-------+----------------------------+-----------------+-------------+

```

I **believe** but cannot verify that in order to do this next part, the controller network must 
have a "public" network with a working subnet and some floating IPs. Floating IPs can be allocated through the dashboard, under the network > public > subnets menu. There should be enough if you set FLOATING_RANGE in local.conf like above. 
You can verify that you have public floating IPs like so:

```
[controller node] openstack floating ip list --network public
```

### creating availability zones

Previously, we were using host aggregates to actually assign a VM to one particular host. Please see the [previous version](https://github.com/jamestaylr/systems-capstone/blob/6f8dc2c7567eb93191a490d94bb0f2188cd03041/openstack-docs/controller-compute-setup.md) of this file in order to see the instructions for that. After doing some research - [notes are here](https://docs.google.com/document/u/1/d/1vW7TuM4CfDum1luivbGjrQAwzAkShKEgQGEPJlWfXvQ/edit) - I determined that availability zones are essentially an easier way of doing what we want.

There are still better ways probably, but this will work. 

```
# nova aggregate-create <aggregate name> <availability zone name>
nova aggregate-create HA1 AZ1
+----+---------+-------------------+-------+------------------------+
| Id | Name    | Availability Zone | Hosts | Metadata               |
+----+---------+-------------------+-------+------------------------+
| 4  |   HA1   | AZ1               |       | 'availability_zone=AZ1'|
+----+---------+-------------------+-------+------------------------+

nova availability-zone-list
| AZ1               | available                              |
| |- node-27        |                                        |
| | |- nova-compute | enabled :-) 2016-11-06T05:13:48.000000 |
+-------------------+----------------------------------------+

```

Now, add a host to the availability zone. Here, HA1 is your aggreagte name and "node-27" is what we're using as our host
name. Presumably it will be capstone0, capstone2, etc. Add your compute nodes!!

```
nova aggregate-add-host HA1 node-27
Host node-27 has been successfully added for aggregate 7
+----+------+-------------------+----------+------------------------+
| Id | Name | Availability Zone | Hosts    | Metadata               |
+----+------+-------------------+----------+------------------------+
| 7  | HA1  | AZ1               | 'node-27'| 'availability_zone=AZ1'|
+----+------+-------------------+----------+------------------------+
```

Now, create the instance. It will be automatically added to one of the nodes that's part of our availibility zones. 

```
openstack server create [name-of-instance] --flavor [your-flavor-name]  --image [your-image, probably cirrOS] --nic net-id=public --availability-zone [your-az-name]

ex: openstack server create testinstance  --flavor m1.flavor_2  --image  cirros-0.3.5-x86_64-disk  --nic net-id=public 
-- availability-zone AZ1
+-------------------------------------+-----------------------------------------------------------------+
| Field                               | Value                                                           |
+-------------------------------------+-----------------------------------------------------------------+
| OS-DCF:diskConfig                   | MANUAL                                                          |
| OS-EXT-AZ:availability_zone         |                                                                 |
| OS-EXT-SRV-ATTR:host                | None                                                            |
| OS-EXT-SRV-ATTR:hypervisor_hostname | None                                                            |
| OS-EXT-SRV-ATTR:instance_name       |                                                                 |
| OS-EXT-STS:power_state              | NOSTATE                                                         |
| OS-EXT-STS:task_state               | scheduling                                                      |
| OS-EXT-STS:vm_state                 | building                                                        |
| OS-SRV-USG:launched_at              | None                                                            |
| OS-SRV-USG:terminated_at            | None                                                            |
| accessIPv4                          |                                                                 |
| accessIPv6                          |                                                                 |
| addresses                           |                                                                 |
| adminPass                           | 6Zh6BAjU8Qy5                                                    |
| config_drive                        |                                                                 |
| created                             | 2017-10-27T16:08:04Z                                            |
| flavor                              | m1.flavor_2 (c48d78ba-dd0c-4bc6-8a99-13718a19311d)              |
| hostId                              |                                                                 |
| id                                  | 6f192c2a-bd69-42d9-8b43-2a1f52d6eec3                            |
| image                               | cirros-0.3.5-x86_64-disk (377a1f15-82fe-4868-afc4-8cb91f8a9a0e) |
| key_name                            | None                                                            |
| name                                | testinstance                                                    |
| progress                            | 0                                                               |
| project_id                          | 0b290de9e6c440c184ee3e8b40a6e6ea                                |
| properties                          |                                                                 |
| security_groups                     | name='default'                                                  |
| status                              | BUILD                                                           |
| updated                             | 2017-10-27T16:08:04Z                                            |
| user_id                             | 388c21296def4404b442fb74ffe85f50                                |
| volumes_attached                    |                                                                 |
+-------------------------------------+-----------------------------------------------------------------+

```


## further questions & concerns

1. what are availability zones? how do they relate to host aggregates?
2. does this randomly put the host on a random machine in the host aggregate? can we control it?
3. i believe that this is roughly doing the load balancing for us so we might need a simpler way of doing this.
4. [open stack host aggregate notes](https://docs.openstack.org/nova/pike/user/aggregates.html)

### resources
* https://docs.openstack.org/nova/pike/user/aggregates.html
* https://support.metacloud.com/hc/en-us/articles/115007191687-Using-Host-Aggregates-for-More-Flexible-Instance-Management
