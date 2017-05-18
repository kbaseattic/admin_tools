#!/bin/bash

# must run as root
# this script probably needs some updating, but we don't
# add new hardware nodes very often

apt-get update
apt-get install -y xfsprogs python-pip nfs-common lvm2
pip install docker-compose
# to do:
# install docker-compose from pip

# get nfs and bind mounts in fstab

# this one should be in already for existing VMs
#10.1.20.9:/mnt/kbase /mnt/kbase nfs ro
# this one is just on prodawe4 right now (dec2016)
#/mnt/kbase/data /kb/data none ro,bind 0 0

echo stopping docker
service docker stop

#cp fstab.kbase /etc/fstab

echo installing docker
apt-get install -y docker-engine

echo stopping docker again
service docker stop

echo putting xfs on vdb
umount /kb/data
umount /var/lib/docker
umount /mnt/kbase
umount /mnt
mkfs -t xfs -f /dev/vdb
mount /mnt
mkdir -p /mnt/kbase /mnt/docker /mnt/awe /kb/data
mount /mnt/kbase
mount /kb/data

echo restarting clean docker
rm -rf /var/lib/docker
#ln -s /mnt/docker /var/lib/
mkdir /var/lib/docker
mount /var/lib/docker
service docker start

