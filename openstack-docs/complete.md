## Install Ubuntu on Machine
-   Download `Ubuntu 16.04 Desktop Version` and put it on a flash drive.
-   Plug flash drive into machine that needs Ubuntu   
-   Turn on machine you want to install Ubuntu on   
-   Press F12 to get into the Boot Options   
-   Select the option that represents your hard drive (we previously selected USB-HDD)  
-   Follow menus to install  
    *  Don't install extras that were offered  
    *  Wipe disk and install Ubuntu  
    *  Sit back and wait for it to finish  
    *  Unplug USB when it prompts -- then you should be good to go  
   
## Configure the Network variables
-   Click on the network logo in the top right of the screen (if you're looking at GUI)
-   It'll probably look like an ethernet port or 2 up/down arrows
-   Click on Edit Connections
-   Click Edit for Wired Connection 1
-   Set Method to Manual
-   Click Add in the Addresses section
-   Enter the correct IP address for this machine in the Address part
    ```
      Capstone0 IP is 192.168.0.219  
      Capstone1 IP is 192.168.0.220  
      Capstone2 IP is 192.168.0.221  
      Capstone3 IP is 192.168.0.222  
      Capstone4 IP is 192.168.0.223  
     ```
-   Press Tab (we found that the interface wasn't cooperative if you tried to click to the next option)
-   Enter 24 for NetMask
-   Press Tab
-   Enter `192.168.0.100` for Gateway
-   Press Tab
-   Click on DNS Servers and enter `198.82.247.66, 192.82.247.98, 8.8.8.8`
-   Click Save
-   Open a terminal and run `sudo service network-manager restart`
-   After this you should be good for this step (ping google.com or open a browswer to test)
  
## Install OpenSSH-Server
   Type `sudo apt-get install openssh-server`  
   Password is `maxinet`

## SSH into machine from Hydra to set up known_hosts
-   ` ssh -p 3775 cs5204dpdk@hydra.cs.vt.edu`
-   Password: in email
-   `ssh capstoneX@192.168.0.XX` (fill in the correct `X's` for the machine you want)
    *  If you get an error that says you're not allowed in, and you have just reimaged a machine, go into Hydra's
       `known_hosts` file and delete the entry for that machine.  
    *  This will be the entry that begins with the IP of the machine you just reimaged. You will have to then do this 
       for all of the other nodes because it will have an outdated `known_hosts` entry for the machine you reimaged. 
       (trust me its fine just do it) 
   
## Create stack user for OpenStack and clone DevStack from git 
  `sudo su - `  
  `adduser stack`  
  `echo "stack ALL=(ALL) NOPASSWD: ALL" » /etc/sudoers`  
  `exit`  
  `su stack`  
  `sudo apt-get install git -y`  
  `git clone https://github.com/openstack-dev/devstack.git`  
  `cd devstack`  
  
## Copy in local.conf file in your devstack directory
  ```
  [[local|localrc]]
  ADMIN_PASSWORD=maxinet
  DATABASE_PASSWORD=maxinet
  RABBIT_PASSWORD=maxinet
  SERVICE_PASSWORD=$ADMIN_PASSWORD

  HOST_IP=[YOUR IP]

  LOGFILE=$DEST/logs/stack.sh.log
  LOGDAYS=2

  SWIFT_HASH=66a3d6b56c1f479c8b4e70ab5c2000f5
  SWIFT_REPLICAS=1
  SWIFT_DATA_DIR=$DEST/data

  FLOATING_RANGE=192.168.0.28/30 <<<< change the 28 to one of these based on machine 0 -> 27, 1 -> 30, 2 -> 29, 3 -> 28, 4 -> 31 >>>
  ```
## Run Stack.sh script
  `sudo chown -R stack:stack /opt/stack`  
  `sudo apt-get install tmux`
  `tmux`
  `./stack.sh`  
  `<ctr-b and then press the ‘d’ key>`  
  `To get back to your tmux session, type in “tmux attach” wow!`  
  `source openrc`  
  `openstack` (this starts the CLI)

### More Detail
-----------------
-   http://www.rushiagr.com/blog/2014/04/03/openstack-in-an-hour-with-devstack/
