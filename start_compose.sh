#!/bin/bash


#  polecenie Docker Compose dla logowania i rejestracji
docker compose -f app/login_register/docker-compose.yml up -d --build

# przykładowy Docker Compose dla dodawania produktów
docker compose -f app/controllers/admin/add_product/docker-compose.yml up -d --build

# przykładowy Docker Compose dla dodawania produktów
docker compose -f app/controllers/admin/update_product/docker-compose.yml up -d --build

#  polecenie Docker Compose dla bazy danych
docker compose -f app/databases/docker-compose.yml up -d --build

#  polecenie Docker Compose dla chatbota
docker compose -f app/processes/chatbot/docker-compose.yml up -d --build

# polecenie Docker Compose dla forntendu
docker compose -f app/frontend/docker-compose.yml up -d --build

docker compose -f app/controllers/customer/history_orders/docker-compose.yml up -d --build

