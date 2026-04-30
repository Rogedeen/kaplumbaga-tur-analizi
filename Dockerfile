FROM python:3.11-slim

WORKDIR /app

# Gerekli sistem kütüphanelerini kur (OpenCV vb. için gerekebilir)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kaynak kodları kopyala
COPY src/ ./src/

# Python path ayarı
ENV PYTHONPATH=/app

EXPOSE 8000

# FastAPI sunucusunu başlat
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
