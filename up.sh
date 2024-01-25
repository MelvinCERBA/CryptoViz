#!/bin/bash

# downs all containers if they're up
# ./down.sh
# docker network prune

# Function to check if a Docker network exists
check_network() {
    docker network ls --filter name=$1 -q | wc -l
}

# Create "confluent-network" if it doesn't exist
# if [ $(check_network "confluent-network") -eq 0 ]; then
#     echo "Creating confluent-network..."
#     docker network create confluent-network
# fi

# Create "db-network" if it doesn't exist
# if [ $(check_network "db-network") -eq 0 ]; then
#     echo "Creating db-network..."
#     docker network create db-network
# fi

# # Create "api-network" if it doesn't exist
# if [ $(check_network "api-network") -eq 0 ]; then
#     echo "Creating api-network..."
#     docker network create api-network
# fi

# Remove all exited docker containers
docker ps -a --filter "status=exited" -q | xargs -r docker rm

# Array of specific directories with Docker Compose projects, in the order they should be started
declare -a dirs=("_Infra/confluent" "Database/" "Scrapper/" "SparksApp/"  "Grafana/")

# Start Docker Compose projects in specified directories
for dir in "${dirs[@]}"; do
    if [ -f "$dir/docker-compose.yml" ]; then
        echo " "
        echo -e "\e[1mStarting Docker Compose project in \e[33m$dir\e[0m"
        echo "- - - - - - - - - - - - - - - - - - - -"
        (cd "$dir" && docker-compose up -d)
    else
        echo "No docker-compose.yml found in $dir. Skipping..."
    fi
done