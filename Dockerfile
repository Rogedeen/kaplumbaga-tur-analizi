FROM python:3.11-slim

WORKDIR /app

# Sistem bağımlılıklarını yükle (OpenCV ve YOLO için gerekli)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libxcb1 \
    libsm6 \
    libxext6 \
    libxrender-dev \
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
