#!/bin/bash

# Zatrzymanie i usunięcie kontenerów dla bazy danych
docker compose -f app/databases/docker-compose.yml down

# Zatrzymanie i usunięcie kontenerów dla logowania i rejestracji
docker compose -f app/login_register/docker-compose.yml down

# Zatrzymanie i usunięcie kontenerów dla dodawania produktów
docker compose -f app/controllers/admin/update_product/docker-compose.yml down

# Zatrzymanie i usunięcie kontenerów dla chatbota
docker compose -f app/processes/chatbot/docker-compose.yml down

# Zatrzymanie i usunięcie kontenerów dla frontendu
docker compose -f app/frontend/docker-compose.yml down

# Zatrzymanie i usunięcie kontenerów dla historii zamówień
docker compose -f app/controllers/customer/history_orders/docker-compose.yml down

# Zatrzymanie i usunięcie kontenerów dla koszyka zamówień
docker compose -f app/controllers/customer/send_order/docker-compose.yml down

# Zatrzymanie i usunięcie kontenerów dla zmiany statusu zamówienia
docker compose -f app/controllers/admin/change_order_status/docker-compose.yml down

# Zatrzymanie i usunięcie kontenerów dla stanu magazynu
docker compose -f app/controllers/admin/magazyn/docker-compose.yml down


echo "Wszystkie kontenery zostały zatrzymane i usunięte."