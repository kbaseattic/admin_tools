#!/bin/bash

# Simpler entrypoint script for awe client

clientgroup=$1
vmhostname=$2

echo clientgroup is $clientgroup
echo vmhostname is $vmhostname

# it would be nice to clean this up
containername=$(docker inspect $(hostname)|grep aweworker|grep Name|cut -f2 -d '/'|cut -f1 -d '"')

clientname=${clientgroup}_${vmhostname}_${containername}

# for njsw reporting
export AWE_CLIENTNAME=$clientname
export AWE_CLIENTGROUP=$clientgroup

env

cat /config/config/$clientgroup.token
echo /config/config/$clientgroup.token

/kb/deployment/bin/awe-client --conf /kb/deployment/awe-client.cfg --name=$clientname --data=/mnt/awe/$clientgroup/$clientname/data --logs=/mnt/awe/$clientgroup/$clientname/logs --workpath=/mnt/awe/$clientgroup/$clientname/work --group=$clientgroup --clientgroup_token=$(cat /config/config/$clientgroup.token)


