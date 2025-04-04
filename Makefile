ENV_NAME = rss

up:
	@docker compose -f docker-compose.yml -p $(ENV_NAME) up --build -d --force-recreate
	@docker compose -f docker-compose.yml -p $(ENV_NAME) logs -f

bg:
	@docker compose -f docker-compose.yml -p $(ENV_NAME) up -d

dn:
	@docker compose -f docker-compose.yml -p $(ENV_NAME) down

cl:
	@docker compose -f docker-compose.yml -p $(ENV_NAME) down --volumes --rmi all --remove-orphans

en:
	cp .env.example .env