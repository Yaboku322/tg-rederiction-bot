import telebot
import os
from dotenv import load_dotenv
load_dotenv()
from andro_cfw import CFWSession
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


session = CFWSession.load()
telebot.apihelper.API_URL = session.telebot_api_url()
telebot.apihelper.FILE_URL = session.telebot_file_url()


TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я твой первый бот. Напиши мне что-нибудь.")

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "Мои команды:\n/start - запуск бота\n/help - эта справка")

#Cancel - сброс режима
@bot.message_handler(commands=['cancel'])
def cancel_reply(message):
    global WAITING_FOR_REPLY_TO
    if message.from_user.id == ADMIN_ID:
        WAITING_FOR_REPLY_TO = None
        bot.reply_to(message, "Режим ответа отменен.")
    else:
        bot.reply_to(message, "Эта команда только для владельца.")




ADMIN_ID = int(os.getenv("ADMIN_ID"))

WAITING_FOR_REPLY_TO = None

# very important

@bot.message_handler(content_types=['text'])
def echo(message):
    global WAITING_FOR_REPLY_TO

    if WAITING_FOR_REPLY_TO is not None and message.from_user.id == ADMIN_ID:
        try:
            bot.send_message(WAITING_FOR_REPLY_TO, f"Ответ от владельца:\n\n{message.text}")
        except Exception:
            bot.reply_to(message, "ERROR: пользователь заблокировал бота.")
        finally:
            WAITING_FOR_REPLY_TO = None
        return


    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "Это твое сообщение.")
        return

    text_for_admin = f"by @{message.from_user.username}: {message.text}"
    markup = InlineKeyboardMarkup()

    btn_reply = InlineKeyboardButton(text="Ответить", callback_data=f"reply_{message.from_user.id}")
    btn_reject = InlineKeyboardButton(text="Отклонить", callback_data=f"reject_{message.from_user.id}")
    markup.add(btn_reply, btn_reject)

    bot.send_message(ADMIN_ID, text_for_admin, reply_markup=markup)
    bot.reply_to(message, "Сообщение доставлено владельцу.")


@bot.callback_query_handler(func=lambda call: True)
def handle_admin_action(call):
    # legit check
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Ты не владелец!")
        return

    # call_data выглядит как reply_12345 or reject_12345
    # разделяем строку по нижнему подчеркиванию
    parts = call.data.split("_")
    action = parts[0]       # reply or reject
    user_id = int(parts[1]) # USER ID, который написал сообщение

    #BUTTONS
        # Принять
    if action == "reply":
        global WAITING_FOR_REPLY_TO
        WAITING_FOR_REPLY_TO = user_id
        bot.answer_callback_query(call.id, "Напишите ответ в чат.")
        bot.send_message(ADMIN_ID, f"Режим ответа. Напишите текст:")
        bot.edit_message_text("Вы нажали ответить.", call.message.chat.id, call.message.message_id, reply_markup=None)

        # Отказ
    elif action == "reject":
        bot.send_message(user_id, "Владелец отказался от аудиенции с вами.")
        bot.answer_callback_query(call.id, "Отклонено")
        bot.edit_message_text("Вы нажали Отклонить.", call.message.chat.id, call.message.message_id, reply_markup=None)


print("Bot active...")
bot.infinity_polling(timeout=10, long_polling_timeout=5)