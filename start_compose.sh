#!/bin/bash

#  polecenie Docker Compose dla bazy danych
docker compose -f app/databases/docker-compose.yml up -d --build

#  polecenie Docker Compose dla logowania i rejestracji
docker compose -f app/login_register/docker-compose.yml up -d --build

# przykładowy Docker Compose dla dodawania produktów
docker compose -f app/controllers/admin/update_product/docker-compose.yml up -d --build

#  polecenie Docker Compose dla chatbota
docker compose -f app/processes/chatbot/docker-compose.yml up -d --build

# polecenie Docker Compose dla forntendu
docker compose -f app/frontend/docker-compose.yml up -d --build

# compose for history_orders
docker compose -f app/controllers/customer/history_orders/docker-compose.yml up -d --build

# compose for send_order (koszyk zamowien)
docker compose -f app/controllers/customer/send_order/docker-compose.yml up -d --build

# compose for changing ordres
docker compose -f app/processes/chatbot/docker-compose.yml up -d --build

# compose for change_order_status 
docker compose -f app/controllers/admin/change_order_status/docker-compose.yml up -d --build