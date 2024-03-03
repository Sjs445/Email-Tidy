#!/usr/bin/env bash

# Build the production containers
docker-compose build

# Push containers to docker hub
containers=("db" "py" "react" "nginx" "celery" "flower")

for container in "${containers[@]}"; do
    docker push "zimd00d/email-tidy:$container"
done
