#!/bin/bash

#  polecenie Docker Compose dla bazy danych
docker compose -f app/databases/docker-compose.yml down

#  polecenie Docker Compose dla logowania i rejestracji
docker compose -f app/login_register/docker-compose.yml down

# przykładowy Docker Compose dla dodawania produktów
docker compose -f app/controllers/admin/update_product/docker-compose.yml down

#  polecenie Docker Compose dla chatbota
docker compose -f app/processes/chatbot/docker-compose.yml down

# polecenie Docker Compose dla forntendu
docker compose -f app/frontend/docker-compose.yml down

# compose for history_orders
docker compose -f app/controllers/customer/history_orders/docker-compose.yml down

# compose for send_order (koszyk zamowien)
docker compose -f app/controllers/customer/send_order/docker-compose.yml down

# compose for reccomendations
docker compose -f app/processes/reccomendation/docker-compose.yml down
# compose for change_order_status 
docker compose -f app/controllers/admin/change_order_status/docker-compose.yml down
# compose for magazyn_stan 
docker compose -f app/controllers/admin/magazyn/docker-compose.yml down
