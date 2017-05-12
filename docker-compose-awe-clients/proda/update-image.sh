#!/bin/bash

KBASE_DOCKERHUB_HOST=dockerhubhostnamehere
KBASE_BASE_TAG=kbase/kbase_base:rod_auth2.201704121500

KBASE_BASE=$KBASE_DOCKERHUB_HOST/$KBASE_BASE_TAG

# as kbproda or root
echo pulling images
docker pull $KBASE_BASE
docker tag $KBASE_BASE kbase/kbase_base:prod
docker pull $KBASE_DOCKERHUB_HOST/kbase:sdkbase.latest

