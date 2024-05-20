# Systemy Rozproszone

## Spis Treści
1. [Wprowadzenie](#Wprowadzenie)
2. [Frontend](#Frontend)
# 1. Wprowadzenie
TO DO

### RUN ALL DOCKERS CONTAINERS
```bash
. start_compose.sh
```

# 2. Frontend



### FRONTEND 

#### DOCKER BUILD
```bash
cd app/frontend
docker build --tag streamlit_frontend .
```

```bash
docker compose -f app/frontend/docker-compose.yml up
```

### RUN LOGIN AND REGISTER
```bash
docker compose -f app/login_register/docker-compose.yml up
```

### RUN DATABASES & CRUD API
```bash
docker compose -f app/databases/docker-compose.yml up
```





