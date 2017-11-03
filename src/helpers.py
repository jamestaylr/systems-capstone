def admin():
        subprocess.call([".", "openrc", "admin", "admin"])

def bootImage(azName, imageName):
        admin()
        subprocess.call(["nova", "boot", "--flavor m1.tiny", "--image cirros-0.3.5-x86_64-disk", "--nic net-name=public", "--availability-zone " + azName", imageName])
