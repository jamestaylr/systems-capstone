### creating two VMs and getting them to talk to each other
- Create two vagrant boxes. Same vagrant file in each.
- Start them both up.
- Ping each other. You'll notice that this works.
- Run "xterm &" on VM1. Type in "controller -v ptcp:6633"
- Copy the .py files for VM1 and VM2 from https://techandtrains.com/2014/01/20/connecting-two-mininet-networks-with-gre-tunnel-part-2/
- Make sure that you change the IP addresses to the eth1 addresses of VM1 and VM2. Controller IP is the eth1 of VM1. 
- Run them.
- You can see that both VMs connect to the controllers.
- You should be able to do "h1 ping -c 10.0.0.3" but this does not seem to work yet.
