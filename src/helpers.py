import subprocess

def bootImage(azName, imageName):
        subprocess.call(["openstack", "server" " create", "--flavor m1.tiny", "--image cirros-0.3.5-x86_64-disk", "--nic net-name=public", "--availability-zone " + azName, imageName])

# Returns a list of all the servers (aka instances) on the given node number (0-4) ssh -X capstone2@192.168.0.221
def serversOnNode(nodeNum):
	subprocess.call(["openstack, ]);  


