Telegram Media Downloader Bot
-----------------------------

ملفات:
- main.py
- requirements.txt
- Dockerfile

الاعداد والنشر (على Render):

1. أنشئ مستودع على GitHub وارفع الملفات.
2. سجل في https://dashboard.render.com/ وأنشئ Web Service جديد:
   - اختر Docker (أو استخدام "Web Service" مع Build command: pip install -r requirements.txt و Start command: gunicorn main:app --bind 0.0.0.0:$PORT)
   - اربط المستودع.
3. اضف متغيرات البيئة في إعدادات الخدمة:
   - TELEGRAM_TOKEN = (توكن بوت تيليجرام من BotFather)
   - WEBHOOK_URL = https://your-service.onrender.com   (اكتب عنوان الخدمة التي يعطيك Render)
4. بعد النشر: ضع webhook عبر زيارة:
   - https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook?url=https://your-service.onrender.com/<TELEGRAM_TOKEN>
   (أو دع الكود ينفذ set_webhook تلقائيًا إن ضبطت WEBHOOK_URL)

تنبيهات:
- ملفات أكبر من ~50MB قد لا تُرسل مباشرة عبر بوت تليجرام. في هذه الحالة تحتاج رفع الملف إلى خدمة تخزين (S3, Google Drive...) ثم إرسال الرابط للمستخدم.
- yt-dlp يتحسن ويدعم عدد كبير من المواقع لكن قد يتطلب تحديث مستقبلاً.