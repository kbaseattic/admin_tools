#!/bin/bash

# as kbproda
echo starting docker-compose
cd /home/kbproda/proda/

# dumb hack to get correct vmhostname into docker-compose.yml
export HOSTNAME=$(hostname)
#perl -pi -e 's/prodaweNN/$ENV{HOSTNAME}/' docker-compose.yml
perl -pi -e 's/vmhostname/$ENV{HOSTNAME}/' docker-compose.yml

docker-compose up -d njsaweworker
