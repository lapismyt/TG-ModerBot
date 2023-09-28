import telebot
from datetime import datetime, timedelta

with open("token.txt") as f:
    bot_token = f.read().strip()

bot = telebot.TeleBot(bot_token)

# Команда для получения ID пользователя
@bot.message_handler(commands=['getid'])
def get_id(message):
    if not is_admin(message): return None
    user_id = message.reply_to_message.from_user.id
    bot.reply_to(message, f"ID: {user_id}")

# Команда для выгнания пользователя
@bot.message_handler(commands=['kick'])
def kick_user(message):
    if not is_admin(message): return None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bot.kick_chat_member(message.chat.id, user_id)
        bot.reply_to(message, "Пользователь успешно выгнан!")
    else:
        bot.reply_to(message, "Ответьте на сообщение пользователя, которого хотите выгнать.")

# Команда для бана пользователя
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if not is_admin(message): return None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        duration = message.text.split()[1] if len(message.text.split()) > 1 else None
        
        if duration:
            duration = parse_duration(duration)
            until_date = datetime.now() + duration
            bot.kick_chat_member(message.chat.id, user_id, until_date=until_date)
            bot.reply_to(message, f"Пользователь забанен до {until_date}.")
        else:
            bot.kick_chat_member(message.chat.id, user_id)
            bot.reply_to(message, "Пользователь забанен навсегда!")
    else:
        bot.reply_to(message, "Ответьте на сообщение пользователя, которого хотите забанить.")

# Команда для разбана пользователя
@bot.message_handler(commands=['unban'])
def unban_user(message):
    if not is_admin(message): return None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bot.unban_chat_member(message.chat.id, user_id)
        bot.reply_to(message, "Пользователь разбанен!")
    else:
        bot.reply_to(message, "Ответьте на сообщение пользователя, которого хотите разбанить.")

# Команда для замьюта пользователя
@bot.message_handler(commands=['mute'])
def mute_user(message):
    if not is_admin(message): return None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        duration = message.text.split()[1] if len(message.text.split()) > 1 else None
        
        if duration:
            duration = parse_duration(duration)
            until_date = datetime.now() + duration
            bot.restrict_chat_member(message.chat.id, user_id, until_date=until_date)
            bot.reply_to(message, f"Пользователь замьючен до {until_date}.")
        else:
            bot.restrict_chat_member(message.chat.id, user_id)
            bot.reply_to(message, "Пользователь замьючен навсегда!")
    else:
        bot.reply_to(message, "Ответьте на сообщение пользователя, которого хотите замьютить.")

# Команда для размьюта пользователя
@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if not is_admin(message): return None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
        bot.reply_to(message, "Пользователь размьючен!")
    else:
        bot.reply_to(message, "Ответьте на сообщение пользователя, которого хотите размьютить.")

# Парсинг длительности времени
def parse_duration(duration_string):
    duration = None
    
    if duration_string[-1] == "h":
        duration = timedelta(hours=int(duration_string[:-1]))
    elif duration_string[-1] == "m":
        duration = timedelta(minutes=int(duration_string[:-1]))
    elif duration_string[-1] == "d":
        duration = timedelta(days=int(duration_string[:-1]))
    
    return duration

# Проверяем, является ли пользователь админом
def is_admin(message):
    # получаем список ID админов
    with open("admins.txt") as f:
        admins = f.read().splitlines()
    if message.chat.type == 'private':
        # в личных сообщениях нет админов
        return False
    elif message.sender_chat != None:
        # для каналов проверяем ID канала
        return str(message.sender_chat.id) in admins
    else:
        # для групп и супергрупп проверяем ID пользователя
        return str(message.from_user.id) in admins

bot.infinity_polling()
