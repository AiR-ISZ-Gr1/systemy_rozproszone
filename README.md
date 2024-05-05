# Systemy Rozproszone

## Spis Treści
1. [Wprowadzenie](#Wprowadzenie)
2. [Frontend](#Frontend)
# 1. Wprowadzenie
TO DO

# 2. Frontend

### DOCKER RUN
```bash
cd app/frontend
docker build --tag rozproszone_front .
docker run -p 8501:850 rozproszone_front
```

### RUN IN BASH
```bash
cd app/frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```
### To open frontend you should go to:
`app/frontend`

### and in bash pass
`streamlit run streamlit_app.py`

