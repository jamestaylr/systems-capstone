# setting up devstack

## on ubuntu, in the prompt
sudo apt-get install git

git clone http://github.com/openstack-dev/devstack
cd devstack/

## modify file

vim local.conf

paste in there:

[[local|localrc]]
ADMIN_PASSWORD=secret

DATABASE_PASSWORD=$ADMIN_PASSWORD

RABBIT_PASSWORD=$ADMIN_PASSWORD

SERVICE_PASSWORD=$ADMIN_PASSWORD


## in the prompt
./stack.sh

## more detail

- http://www.rushiagr.com/blog/2014/04/03/openstack-in-an-hour-with-devstack/
- 
