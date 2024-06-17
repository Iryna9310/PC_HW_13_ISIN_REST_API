FROM python:3.9

# Встановлення робочого каталогу
WORKDIR /app

# Копіювання файлу з залежностями
COPY requirements.txt .

# Встановлення залежностей
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копіювання всього коду в контейнер
COPY . .

# Запуск Uvicorn сервера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]





