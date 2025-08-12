import os
import tempfile
import shutil
import traceback
from flask import Flask, request, Response
import telebot
from telebot import types
import subprocess

TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN environment variable is required")

# URL الكامل اللي يدخله Telegram كـ webhook، مثلاً:
# https://your-service.onrender.com/<TOKEN>
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # ضعها في إعدادات Render

bot = telebot.TeleBot(TOKEN, threaded=True)
app = Flask(__name__)

# -------- health-check endpoint (لـ Render health checks) --------
@app.route("/", methods=["GET"])
def health():
    return "OK", 200

# -------- Telegram webhook receiver --------
@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    try:
        json_str = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
    except Exception:
        print("Failed to process update:")
        traceback.print_exc()
    return Response(status=200)

# -------- helper: run yt-dlp to download media --------
def download_with_ytdlp(url: str, out_dir: str, only_audio: bool=False):
    """
    Uses yt-dlp to download the best video (or audio) into out_dir.
    Returns path to downloaded file.
    """
    # safe filename template
    out_template = os.path.join(out_dir, "%(title).100s.%(ext)s")
    cmd = [
        "yt-dlp",
        "-f", "best",
        "-o", out_template,
    ]

    if only_audio:
        # extract audio as mp3
        cmd = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "-o", out_template,
            url
        ]
    else:
        cmd = cmd + [url]

    # run command
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"yt-dlp failed: {proc.stderr[:1000]}")

    # find the file in out_dir (most recently modified)
    files = [os.path.join(out_dir, f) for f in os.listdir(out_dir)]
    if not files:
        raise RuntimeError("No file was downloaded by yt-dlp")
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return files[0]

# -------- message handlers --------
@bot.message_handler(commands=["start", "help"])
def cmd_start(message):
    bot.send_message(message.chat.id,
                     "مرحباً! أرسل لي رابط فيديو (TikTok / Instagram / Pinterest) وسأحاول تحميله. "
                     "لـ TikTok سأعطيك خيار تحميل الفيديو أو الصوت فقط.")

def detect_platform(url: str):
    u = url.lower()
    if "tiktok.com" in u or "vt.tiktok.com" in u:
        return "tiktok"
    if "instagram.com" in u or "instagr.am" in u:
        return "instagram"
    if "pinterest." in u:
        return "pinterest"
    return "unknown"

@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_all(message):
    text = message.text.strip()
    chat_id = message.chat.id

    # quick URL check
    if not (text.startswith("http://") or text.startswith("https://")):
        bot.reply_to(message, "أرسل رابط صحيح يبدأ بـ http:// أو https://")
        return

    platform = detect_platform(text)
    if platform == "unknown":
        bot.reply_to(message, "هذه المنصة غير مدعومة حالياً. ادعم TikTok وInstagram وPinterest.")
        return

    # For TikTok, offer buttons for video or audio
    if platform == "tiktok":
        kb = types.InlineKeyboardMarkup()
        kb.row(
            types.InlineKeyboardButton("🔊 صوت (MP3)", callback_data=f"tiktok_audio|{text}"),
            types.InlineKeyboardButton("🎬 فيديو", callback_data=f"tiktok_video|{text}")
        )
        bot.send_message(chat_id, "اختر ما تريد تحميله:", reply_markup=kb)
        return

    # For Instagram/Pinterest: start downloading video (video only)
    msg = bot.send_message(chat_id, "جاري تجهيز التحميل... قد يستغرق بعض الوقت.")
    try:
        tmpdir = tempfile.mkdtemp(prefix="down_")
        downloaded = download_with_ytdlp(text, tmpdir, only_audio=False)
        filesize = os.path.getsize(downloaded)
        # Telegram has upload limits; we warn if big
        if filesize > 50 * 1024 * 1024:
            bot.edit_message_text("الملف كبير جدًا (أكبر من 50MB). لن أرسله مباشرة. أرسله لك كرابط أو حاول تقليل الجودة.", chat_id, msg.message_id)
            # Could implement upload to external storage here
        else:
            bot.send_chat_action(chat_id, "upload_video")
            with open(downloaded, "rb") as f:
                bot.send_video(chat_id, f)
            bot.edit_message_text("تم الإرسال ✅", chat_id, msg.message_id)
    except Exception as e:
        print("Error:", e)
        bot.edit_message_text(f"فشل التحميل: {e}", chat_id, msg.message_id)
    finally:
        try:
            shutil.rmtree(tmpdir)
        except Exception:
            pass

# -------- callback query handler for inline buttons --------
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data  # format: tiktok_audio|URL or tiktok_video|URL
    try:
        kind, url = data.split("|", 1)
    except Exception:
        bot.answer_callback_query(call.id, "خطأ بالبيانات.")
        return

    chat_id = call.message.chat.id
    msg = bot.send_message(chat_id, "جاري التحميل... انتظر قليلاً.")
    try:
        tmpdir = tempfile.mkdtemp(prefix="down_")
        if kind == "tiktok_audio":
            downloaded = download_with_ytdlp(url, tmpdir, only_audio=True)
            filesize = os.path.getsize(downloaded)
            if filesize > 50 * 1024 * 1024:
                bot.edit_message_text("ملف الصوت كبير جدًا ليرسله عبر تلغرام.", chat_id, msg.message_id)
            else:
                bot.send_chat_action(chat_id, "upload_audio")
                with open(downloaded, "rb") as f:
                    bot.send_audio(chat_id, f)
                bot.edit_message_text("تم إرسال الصوت ✅", chat_id, msg.message_id)
        else:  # tiktok_video
            downloaded = download_with_ytdlp(url, tmpdir, only_audio=False)
            filesize = os.path.getsize(downloaded)
            if filesize > 50 * 1024 * 1024:
                bot.edit_message_text("ملف الفيديو أكبر من الحد المسموح لإرساله عبر البوت (قد تحتاج رفعه لخدمة تخزين خارجية).", chat_id, msg.message_id)
            else:
                bot.send_chat_action(chat_id, "upload_video")
                with open(downloaded, "rb") as f:
                    bot.send_video(chat_id, f)
                bot.edit_message_text("تم إرسال الفيديو ✅", chat_id, msg.message_id)
    except Exception as e:
        print("Callback error:", e)
        traceback.print_exc()
        bot.edit_message_text(f"فشل التحميل: {e}", chat_id, msg.message_id)
    finally:
        try:
            shutil.rmtree(tmpdir)
        except Exception:
            pass

# -------- helper to set webhook when starting (optional) --------
def set_webhook():
    if not WEBHOOK_URL:
        print("WEBHOOK_URL not set; skipping set_webhook")
        return
    url = f"{WEBHOOK_URL.rstrip('/')}/{TOKEN}"
    res = bot.set_webhook(url)
    print("set_webhook result:", res)

# -------- app entrypoint --------
if __name__ == "__main__":
    # local run for testing
    set_webhook()
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)