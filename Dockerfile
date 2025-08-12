FROM python:3.11-slim

# تثبيت الاعتماديات للنظام (ffmpeg مطلوب لمعالجة الصوت/فيديو)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# exposed port (Render يعطي PORT كمتغير بيئي)
ENV PORT 10000
CMD exec gunicorn --bind 0.0.0.0:$PORT main:app