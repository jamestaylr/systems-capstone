import subprocess

def bootImage(azName, imageName):
        subprocess.call(["openstack", "server", "create", "--flavor m1.tiny", "--image cirros-0.3.5-x86_64-disk", "--nic net-name=public", "--availability-zone " + azName, imageName])
