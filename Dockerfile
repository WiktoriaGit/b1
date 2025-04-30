FROM python:3.11-slim

# 1. Ustawiamy katalog roboczy
WORKDIR /app

# 2. Najpierw kopiujemy requirements do /app
COPY ./app/requirements.txt /app/requirements.txt

# 3. Instalujemy paczki
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 4. Kopiujemy cały folder app do /app/app
COPY ./app /app/app

# 5. Otwieramy port
EXPOSE 8000

# 6. Uruchamiamy Uvicorn, wskazując "app.main:app"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

