FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости (если нужны)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .

# Очистка от BOM и невидимых символов (на всякий случай)
RUN sed -i 's/^\xEF\xBB\xBF//' requirements.txt 2>/dev/null || true && \
    sed -i 's/^\xFF\xFE//' requirements.txt 2>/dev/null || true && \
    sed -i 's/^\xFE\xFF//' requirements.txt 2>/dev/null || true && \
    tr -d '\r\0' < requirements.txt > requirements.txt.tmp && mv requirements.txt.tmp requirements.txt 2>/dev/null || true

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir fastapi uvicorn aiohttp && \
    pip cache purge

# Проверяем установку aiogram 3.x
RUN python -c 'from aiogram.client.default import DefaultBotProperties; print("✅ aiogram 3.x OK")' 2>/dev/null || echo "⚠️ aiogram 3.x not found"

# Копируем весь код приложения
COPY . .

# Создаём main.py (если его нет) – он нужен для Uvicorn
RUN echo "from bot import app" > /app/main.py

# Директория для данных (БД, файлы состояния)
ENV DATA_DIR=/app/data
RUN mkdir -p /app/data && chmod 777 /app/data

# ОЧЕНЬ ВАЖНО: УДАЛЯЕМ СТАРЫЙ HTTP_WRAPPER (если он был создан ранее)
# Этот блок удалён полностью – ничего не копируем в /opt/bothost

# Единственная команда запуска – Uvicorn
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port ${PORT:-3000}"
