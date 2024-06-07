#!/usr/bin/env pwsh

# Docker Compose command for the database
docker compose -f app/databases/docker-compose.yml up -d --build

# Docker Compose command for login and registration
docker compose -f app/login_register/docker-compose.yml up -d --build

# Example Docker Compose command for adding products
docker compose -f app/controllers/admin/update_product/docker-compose.yml up -d --build

# Docker Compose command for the chatbot
docker compose -f app/processes/chatbot/docker-compose.yml up -d --build

# Docker Compose command for the frontend
docker compose -f app/frontend/docker-compose.yml up -d --build

# Docker Compose command for history orders
docker compose -f app/controllers/customer/history_orders/docker-compose.yml up -d --build

# Docker Compose command for sending order (order basket)
docker compose -f app/controllers/customer/send_order/docker-compose.yml up -d --build

# Docker Compose command for recommendations
docker compose -f app/processes/reccomendation/docker-compose.yml up -d --build

# Docker Compose command for changing order status
docker compose -f app/controllers/admin/change_order_status/docker-compose.yml up -d --build

# Docker Compose command for warehouse status
docker compose -f app/controllers/admin/magazyn/docker-compose.yml up -d --build
