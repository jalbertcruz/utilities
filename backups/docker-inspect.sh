#!/usr/bin/env bash

docker_containers=( $(docker ps -a | grep -v CONTAINER | awk '{print $1}') )

for i in "${!docker_containers[@]}"; do
     docker inspect "${docker_containers[$i]}" > "${docker_containers[$i]}.txt"
done


# docker ps -a | grep -v CONTAINER | awk '{print $1}' | xargs -L 1 docker inspect > $0.txt
