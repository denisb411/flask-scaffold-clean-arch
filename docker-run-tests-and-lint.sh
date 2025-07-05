#!/bin/bash

docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
docker compose -f docker-compose.test.yml run --rm app make lint
