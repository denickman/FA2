# Slim-образ достаточно — у проекта нет тяжёлых нативных зависимостей,
# кроме psycopg2/cryptography, а psycopg2-binary уже несёт свои скомпилированные бинарники.
FROM python:3.12-slim

WORKDIR /app

# Сначала копируем только requirements.txt — так Docker кэширует этот слой
# и не переустанавливает зависимости при каждом изменении кода, только когда
# меняется сам requirements.txt. Это реально экономит время при пересборках.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Теперь копируем всё остальное (TodoApp/, alembic/, alembic.ini и т.д.)
COPY . .

EXPOSE 8000

# main.py использует относительные импорты (from .models, from .routers import ...),
# поэтому TodoApp нужно запускать как пакет — отсюда "TodoApp.main:app", а не "main:app".
# --host 0.0.0.0 обязателен, иначе сервер не будет доступен снаружи контейнера.
CMD ["uvicorn", "TodoApp.main:app", "--host", "0.0.0.0", "--port", "8000"]
