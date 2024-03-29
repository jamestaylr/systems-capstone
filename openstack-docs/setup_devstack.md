# setting up devstack

## on ubuntu, in the prompt
sudo apt-get install git

git clone http://github.com/openstack-dev/devstack
cd devstack/

## modify file

vim local.conf

There are several different local.confs floating around.

It seems like you can use this one:

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

FLOATING_RANGE=192.168.0.28/30 <<<< change the .28 to something else (bump it up one ex: 29) >>>
```

Or you can use the default local.conf on the devstack website. Both seem to work? 


## in the prompt
`sudo chown -R stack:stack /opt/stack`

`./stack.sh`

`source openrc` 

then to start the openstack cli: `openstack` !

## more detail

- http://www.rushiagr.com/blog/2014/04/03/openstack-in-an-hour-with-devstack/

# Configuring SSH Tunnels
In computer networks, a tunneling protocol allows a network user to access or
provide a network service that the underlying network does not support or
provide directly. SSH tunneling allows us to redirect a port on a local machine
to a port on a host machine, thus exposing a network service we might otherwise
be unable to reach.

The syntax typically is:
```fish
ssh -L 9000:127.0.0.1:80 jamestay@rlogin.cs.vt.edu
```

Where `9000` is the local host binding of the port `80` on the host's
`127.0.0.1`. You can use this to route any arbitrary traffic. In our case, we
will use SSH tunneling to access port `80` on the server configured with dev
stack. We would be otherwise unable to reach these nodes because they sit in a
DMZ behind `hydra`.

The command I use is:
```fish
sshpass ssh -L 9000:127.0.0.1:80 capstone4
```

Where `capstone4` is:
```text
Host capstone4
    Hostname 192.168.0.223
    User capstone4
    ProxyCommand ssh -q -W %h:%p hydra
```

This configures SSH to connect to `capstone4` via an SSH connection to `hydra`.
`hydra` stupidly uses password authentication, so we get around this by using
`sshpass`, which has the alias:

```fish
alias sshpass 'sshpass -p password'
```

This must wrap `ssh` because it responds to the first password prompt from
`hydra`. I don't think this tunneling approach will work unless you have key
authentication configured on all the capstone nodes.

You also should be able to access the nodes by:
```fish
sshpass ssh capstone0
```
