# =========================
# STAGE 1: Builder
# =========================
FROM python:3.13-slim AS builder

# Ustawienie katalogu roboczego
WORKDIR /build

# Skopiuj tylko pliki wymagane do zainstalowania zależności — optymalizacja cache'a
COPY requirements.txt .

# Instalacja zależności w katalogu tymczasowym
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

# =========================
# STAGE 2: Final image
# =========================
FROM python:3.13-alpine3.18

# OCI standard labels (autor itd.)
LABEL org.opencontainers.image.title="Weather Flask App"
LABEL org.opencontainers.image.description="A lightweight weather application with Flask and Waitress"
LABEL org.opencontainers.image.authors="Mateusz Kozieł"
LABEL org.opencontainers.image.version="1.0"
LABEL org.opencontainers.image.licenses="MIT"

# Ustawienie katalogu roboczego
WORKDIR /app

# Skopiuj zbudowane zależności z etapu buildera
COPY --from=builder /install /usr/local

# Skopiuj kod źródłowy aplikacji do kontenera
COPY . /app

# Otwórz port aplikacji
EXPOSE 8000

# Dodanie HEALTHCHECK — sprawdzanie co 30s, timeout 3s
HEALTHCHECK --interval=30s --timeout=3s \
    CMD wget --spider -q http://localhost:8000/ || exit 1

# Komenda startowa
CMD ["python", "./server.py"]
