import telebot
import requests
import time

# ضع التوكن الخاص بك هنا من BotFather
API_TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = telebot.TeleBot(API_TOKEN)

# دالة لتوليد إيميل عشوائي
def generate_email():
    response = requests.get("https://api.1secmail.com/v1/?action=genRandomMailbox")
    return response.json()[0]

# دالة لفحص الرسائل الواصلة
def check_messages(email):
    login, domain = email.split('@')
    url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
    return requests.get(url).json()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! اضغط على /newmail للحصول على إيميل وهمي جديد.")

@bot.message_handler(commands=['newmail'])
def new_mail(message):
    email = generate_email()
    bot.reply_to(message, f"إيميلك الوهمي الجديد هو:\n`{email}`\n\nانتظر هنا، سأرسل لك أي رسالة تصلك فوراً!", parse_mode="Markdown")
    
    # حلقة بسيطة لفحص البريد لمدة 5 دقائق (كمثال)
    stop_time = time.time() + 300 
    while time.time() < stop_time:
        msgs = check_messages(email)
        if msgs:
            for msg in msgs:
                msg_id = msg['id']
                login, domain = email.split('@')
                content_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={msg_id}"
                content = requests.get(content_url).json()
                full_msg = f"📩 **رسالة جديدة!**\nمن: {content['from']}\nالموضوع: {content['subject']}\n\nالمحتوى:\n{content['textBody']}"
                bot.send_message(message.chat.id, full_msg, parse_mode="Markdown")
            break # يتوقف بعد استقبال أول رسالة لتبسيط الكود
        time.sleep(5)

bot.polling()