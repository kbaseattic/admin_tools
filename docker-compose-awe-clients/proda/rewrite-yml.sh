#!/bin/bash

# as kbproda
echo rewriting docker-compose.yml
cd /home/kbproda/proda/

# dumb hack to get correct vmhostname into docker-compose.yml
export HOSTNAME=$(hostname)
perl -pi -e 's/vmhostname/$ENV{HOSTNAME}/' docker-compose.yml

