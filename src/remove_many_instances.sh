"""
Do not run this!
It is a shell for future occurances.
You must first disassociate the floating IP
with the server, as there seems to be a bug
if you delete a server without first doing so.


for x in {1..10};
do 
	. openrc admin admin
	openstack server delete  c$x
done
"""
