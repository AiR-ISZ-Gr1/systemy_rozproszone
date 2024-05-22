#!/bin/bash

#  polecenie Docker Compose dla bazy danych
docker compose -f app/databases/docker-compose.yml up

#  polecenie Docker Compose dla logowania i rejestracji
docker compose -f app/login_register/docker-compose.yml up

# polecenie Docker Compose dla forntendu
docker compose -f app/frontend/docker-compose.yml up

# przykładowy Docker Compose dla dodawania produktów
docker compose -f /app/controllers/admin/add_product/docker-compose.yml up

# przykładowy Docker Compose dla dodawania produktów
docker compose -f /app/controllers/admin/update_product/docker-compose.yml up