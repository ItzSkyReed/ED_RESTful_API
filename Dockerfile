# Используем официальный образ Python в качестве базового образа
FROM python:3.12.7-bookworm

# Отключаем буферизацию и запись .pyc файлов
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /backend

# Копируем файл requirements.txt в рабочую директорию
COPY requirements.txt /backend/

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем всё остальное в контейнер
COPY . /backend/

# Запускаем сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
