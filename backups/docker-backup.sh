#!/usr/bin/env bash

docker_images_names=( $(docker images | grep -v \<none\> |  awk '{if (NR>1) print}' | awk '{print $1}') )
docker_images_tags=( $(docker images | grep -v \<none\> | awk '{if (NR>1) print}' | awk '{print $2}') )

for i in "${!docker_images_names[@]}"; do
     name=$(echo "${docker_images_names[$i]}" | sed 's/\//__/')
     tag=$(echo "${docker_images_tags[$i]}")

     echo $name:$tag
     [[ $tag != latest ]] && docker save "${docker_images_names[$i]}:${docker_images_tags[$i]}" -o ${name}_${tag}.tar
done

# docker load -i <image_file>
