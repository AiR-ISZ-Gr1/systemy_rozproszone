# Pobierz oficjalny obraz Pythona
FROM python:3.9

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj plik wymagany do instalacji zależności
COPY requirements.txt .

# Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj resztę aplikacji
COPY . .

# Exponuj port, na którym będzie działać aplikacja
EXPOSE 8002
VOLUME [ "/products" ]

# Komenda do uruchomienia aplikacji
CMD ["uvicorn", "collect_product:app", "--host", "0.0.0.0", "--port", "8002"]
