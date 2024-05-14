#!/bin/bash

# Pierwsze polecenie Docker Compose dla bazy danych
docker compose -f app/databases/docker-compose.yml up &

# Drugie polecenie Docker Compose dla logowania i rejestracji
docker compose -f app/login_register/docker-compose.yml up &
