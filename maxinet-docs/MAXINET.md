# get ec2 set up

Currently, we have 3 boxes. You can see the descriptions here: https://docs.google.com/spreadsheets/d/1WiVmyEVVzeEAftdGhp5gQ6eqKYBj0aLLdjbInvplxXk/edit#gid=0

You need to open 3 tabs and ssh into each one. The username is "capstone" and pw is "maxinet" Go ahead and open up 4 total tabs of the first one. 

~~# in one tab on the first machine (your frontend)~~

~~> MaxiNetFrontendServer~~

~~# on the first (different tab), second, and third machines (all workers)~~

~~> sudo MaxiNetWorker~~

~~You should see that the workers are connecting to the frontend.~~

# on the first machine (different tab): your controller

> cd ~/pox/ && python2 pox.py forwarding.l2_learning

This starts an OpenFlow controller

# on the first machine (different tab): your program

> /usr/local/share/MaxiNet/examples/simplePing.py

This is a good example. In the examples folder, there's plenty of other things. I think dynamicTopologies.py is closest to what we want. You can run that too (all the examples should work already).


# more info

* Maxinet github: http://github.com/MaxiNet/MaxiNet/
* We can get the actual ec2 information, change the number of hosts, etc
* Essentially these 3 hosts are part of a security group on ec2 where they can comunicate with each other via their internal IPs and the outside world can't get in (besides ssh). 
