# building script
docker compose -f infra/docker-compose.yml up --build

#  cleaing script
docker compose -f infra/docker-compose.yml down --remove-orphans
docker compose -f infra/docker-compose.yml up --build