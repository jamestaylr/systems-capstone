# CS 4284: Systems Capstone

## rough steps
1. Get mininet on multiple machines working
2. Try different topologies
3. Research virtual data centers
4. Create different topologies using a controller. View GUI results using OpenDaylight controller or similar. 
5. Benchmark mininet (number of switches/hosts & topology vs. memory usage to change topology, time it takes to make that change)
6. Take [some sort of industry problem, dr butt mentioned virtualized data centers] and say SDNs are used here, they make things dynamic and make virtualization easier. [also maybe security? Since easier to change policies?]
This is more of a discussion.
7. Potentially just show how difficult things are to do manually vs doing by a SDN? Dr butt approaches this by telling us to try different topologies and creating them (vs doing manually?) 

## Benchmarking
* http://vlkan.com/blog/post/2013/04/19/benchmarking-mininet/
* https://github.com/jamestaylr/systems-capstone/blob/master/maxinet-docs/BENCHMARKING-MAXINET.md

## next steps
Jamal suggests looking at OpenStack:
* several modules (neutron): hack that, work on that
* mininet is limited functionality-wise; we might pigeonhole ourselves 

Expand on SDN. 
* Dynamic load balancer? 
* Implement a learning switch? 
* Write a firewall (http://www.cs.columbia.edu/~lierranli/coms6998-8SDNFall2013/homeworks/hw1.pdf)? 

## why SDNs?
* good with big data throughput + connectivity
* cloud-based traffic (SDN can deliver on-demand
* managing traffic to IP addresses and VMs (dynamic routing tables!)
* infra scalable and agile (easy to add devices to the network with SDN)
* managing security (SDN can easily change the policies)
