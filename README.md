# Systemy Rozproszone

## Spis Treści
1. [Wprowadzenie](#Wprowadzenie)
2. [Frontend](#Frontend)
# 1. Wprowadzenie
TO DO

# 2. Frontend

### DOCKER BUILD & RUN 
```bash
cd app/frontend
docker build --tag rozproszone_front .
docker run -p 8501:8501 -p 8000:8000 rozproszone_front
```

### RUN IN BASH
```bash
cd app/frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```



### RUN DATABASES & CRUD API
```bash
docker compose -f app/databases/docker-compose.yml up
```
