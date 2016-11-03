#!/bin/bash

# Do nothing if neither docker nor docker-latest service is running
if ! systemctl --quiet is-active docker-latest && ! systemctl --quiet is-active docker; then
  exit 0
fi

# If there are no dead containers, exit.
DEAD_CONTAINERS=`docker ps -aq -f status=dead`

[ -z "$DEAD_CONTAINERS" ] && exit 0

# Try to cleanup dead containers
docker rm $DEAD_CONTAINERS
