#!/bin/bash
docker run --rm  -v /root/check_mk_awe:/kb/config  --entrypoint=/kb/config/entrypoint.sh kbase/kbase_base:prod
