import telebot
from settings import TG_TOKEN
from telebot import types

bot = telebot.TeleBot(TG_TOKEN)

user_data = {}

class User:
    def __init__(self, first_name, ):
        self.first_name = first_name
        self.second_name = None
        self.age = None

@bot.message_handler(commands="start")
def get_info(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text= "Да", callback_data= "yes")
    item_no = types.InlineKeyboardButton(text= "Нет", callback_data= "no")
    markup_inline.add(item_yes, item_no)
    bot.send_message(message.chat.id, "Здравствуйте! Я бот стоматологической клиники 'Бриллиант'! "
                                      "\nЖелаете ли Вы записаться к нам на прием?", reply_markup=markup_inline)

@bot.callback_query_handler(func = lambda call: True)
def answer(call):
    if call.data == "yes":
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_one = types.InlineKeyboardButton("Заполнить анкету")
        markup_reply.add(item_one)
        mes = bot.send_message(call.message.chat.id, "Нажмите на кнопку ('Заполнить анкету')",
                               reply_markup=markup_reply)
        bot.register_next_step_handler(mes, send_welcome)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Всего доброго!")

def send_welcome(message):
    mess = bot.send_message(message.chat.id, "Введите свое имя")
    bot.register_next_step_handler(mess, process_firstname_step)

def process_firstname_step(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = User(message.text)
        mess = bot.send_message(message.chat.id, 'Введите свою фамилию')
        bot.register_next_step_handler(mess, process_secondname_step)
    except Exception as e:
        bot.reply_to(message, 'ошибка')

def process_secondname_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.second_name = message.text
        mess = bot.send_message(message.chat.id, 'Введите свой возраст')
        bot.register_next_step_handler(mess, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'ошибка')

def process_age_step(message):
    try:
        user_id = message.from_user.id
        user = user_data[user_id]
        user.age = message.text
        bot.send_message(message.chat.id, "Вы успешно зарегестрированы!")
    except Exception as e:
        bot.reply_to(message, 'ошибка')

# для пошагового бота
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

if __name__ == "__main__":
    bot.polling(none_stop=True)
