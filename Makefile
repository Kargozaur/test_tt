.PHONY: up down up-build

up:
	docker-compose up -d

down:
	docker-compose down

up-build:
	docker-compose up -d --build