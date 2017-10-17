<b>what are good topologies for (virtual) data centers?</b>

---

<b>some resources</b>:

low-level ppts: https://www.cs.cornell.edu/courses/cs5413/2014fa/lectures/09-vl2.pdf, https://www.cse.wustl.edu/~jain/cse570-13/ftp/m_03dct.pdf

"Topology-Aware Virtual Machine Placement in Data Centers": https://link.springer.com/article/10.1007/s10723-015-9343-x
- virtual data centers create VMs for a target workload, then release them once the workload is processed 
- clients usually request multiple VMs
- VMs that communicate should be closer together (on physical machines) to reduce resource usage 

topologies and their advantages/disadvantages: http://www.cse.wustl.edu/~jain/cse567-08/ftp/topology/index.html

---

first, what are we looking for in a topology?
- traffic of one service should not affect traffic of other services 
- easy server to service assignment 
- easy to move across subnets 
- scalability

fat-tree and VL2 topologies are common ones?

http://inf.ufrgs.br/~marinho/wp-content/uploads/How-physical-network-topologies-affect-virtual-network-embedding-quality-A-characterization-study-based-on-ISP-and-datacenter-networks.pdf
- conventional vs. switch-oriented topologies (fat-tree, VL2) 
- scalability and fault-tolerance? 
- results: topologies w more connections --> fewer rejected requests, but higher resource consumption

ok i couldn't find anything abt specific topologies used in virtudal date centers 
