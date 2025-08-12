# Telegram Media Downloader Bot

---

## Files:
- main.py
- requirements.txt
- Dockerfile

---

## Setup and Deployment on Render:

1. Create a GitHub repository and upload the above files.

2. Sign up or log in to https://dashboard.render.com/ and create a new Web Service.

   - Choose **Docker** (or select **Web Service** and set the build and start commands):
     - Build command: `pip install -r requirements.txt`
     - Start command: `gunicorn main:app --bind 0.0.0.0:$PORT`

   - Link your GitHub repository.

3. Add environment variables in Render settings:

   - `TELEGRAM_TOKEN` = Your Telegram bot token from BotFather
   - `WEBHOOK_URL` = The URL Render gives you for your service, e.g. `https://your-service.onrender.com`

---

# بوت تنزيل وسائط تيليجرام

---

## الملفات:
- main.py
- requirements.txt
- Dockerfile

---

## الإعداد والنشر على Render:

1. أنشئ مستودع على GitHub وارفع الملفات السابقة.

2. سجّل الدخول أو أنشئ حساب في https://dashboard.render.com/ وأنشئ خدمة ويب جديدة.

   - اختر **Docker** (أو اختر **Web Service** وأدخل أوامر البناء والبدء):
     - أمر البناء: `pip install -r requirements.txt`
     - أمر البدء: `gunicorn main:app --bind 0.0.0.0:$PORT`

   - اربط المستودع الخاص بك من GitHub.

3. أضف متغيرات البيئة في إعدادات الخدمة:

   - `TELEGRAM_TOKEN` = رمز بوت التيليجرام من BotFather  
   - `WEBHOOK_URL` = عنوان الخدمة التي يعطيك Render، مثل `https://your-service.onrender.com`

---