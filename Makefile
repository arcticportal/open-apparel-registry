DC = docker compose -f docker-compose.develop.yml

up:
	$(DC) up

down:
	$(DC) down

buildup:
	$(DC) up --build
