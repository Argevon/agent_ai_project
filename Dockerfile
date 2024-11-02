# Użycie oficjalnego lekkiego obrazu Pythona.
FROM python:3.9-slim

# Ustawienie katalogu roboczego
WORKDIR /app

# Skopiowanie lokalnych plików do kontenera.
COPY web_page /app

# Instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

# Ujawnienie portu, na którym działa aplikacja
EXPOSE 8080

# Uruchomienie aplikacji przy starcie kontenera.
CMD ["python", "app.py"]
