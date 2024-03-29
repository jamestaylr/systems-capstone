# Set Up Machines

Currently, we have 3 boxes deployed on Amazon EC2. You can see the descriptions here: https://docs.google.com/spreadsheets/d/1WiVmyEVVzeEAftdGhp5gQ6eqKYBj0aLLdjbInvplxXk/edit#gid=0

You need to open 3 tabs and ssh into each one. The username is `capstone` and password is `maxinet`. Go ahead and open up 4 total tabs of the first one.

~~# in one tab on the first machine (your frontend)~~

~~```bash
MaxiNetFrontendServer
```~~

~~# Setup the Worker Daemon ~~
Perform on all worker nodes:

~~```bash
sudo MaxiNetWorker
```~~

~~You should see that the workers are connecting to the frontend.~~

# Controller
Perform on the first machine:

```bash
cd ~/pox/ && python2 pox.py --verbose forwarding.l2_learning
```

This starts an OpenFlow controller

If you want to see the GUI of the topologies, I _think_ that this will work (you might have to install gelphi first):

```bash
sudo ~/pox/pox.py forwarding.l2_learning \
    openflow.discovery misc.gephi_topo \
    openflow.spanning_tree --no-flood --hold-down \
    host_tracker info.packet_dump \
    samples.pretty_log log.level --DEBUG
```

# Configure Your Program
Perform on the first machine:

```bash
usr/local/share/MaxiNet/examples/simplePing.py
```

This is a good example. In the examples folder, there's plenty of other things. I think `dynamicTopologies.py` is closest to what we want. You can run that too (all the examples should work already).

# More Info

* Maxinet GitHub: http://github.com/MaxiNet/MaxiNet/
* We can get the actual EC2 information, change the number of hosts, etc
* Essentially these 3 hosts are part of a security group on EC2 where they can comunicate with each other via their internal IPs and the outside world can't get in (besides ssh)
* There's a config file in `~/.MaxiNet.cfg`
