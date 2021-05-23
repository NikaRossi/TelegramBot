import telebot
from settings import TG_TOKEN
from telebot import types
import database


bot = telebot.TeleBot(TG_TOKEN)

user_data = {}

class User:
    def __init__(self, first_name, ):
        self.first_name = first_name
        self.second_name = None
        self.phone = None

@bot.message_handler(commands=["start"])
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
        send_welcome(call.message)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Всего доброго!")
    elif call.data.split()[0] == "set_service":
        database.Database().set_service_for_user(call.from_user.id, call.data.split()[1])
        doctors = database.Database().get_all_doctors_for_service(call.data.split()[1])
        markup_inline = types.InlineKeyboardMarkup()
        for doctor in doctors:
            markup_inline.add(types.InlineKeyboardButton(text=doctor[1], callback_data=f'set_doctor {doctor[0]}'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите доктора', reply_markup=markup_inline)
    elif call.data.split()[0] == "set_doctor":
        database.Database().set_doctor_for_user(call.from_user.id, call.data.split()[1])
        data = database.Database().get_ticket(call.from_user.id)
        markup_inline = types.InlineKeyboardMarkup()
        markup_inline.add(types.InlineKeyboardButton(text="Адрес", callback_data='get address'))
        markup_inline.add(types.InlineKeyboardButton(text="Часы работы", callback_data='get work_time'))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Для клиента: {data["user"]}\nЗабронирована услуга: {data["service"]}\nВрач: {data["doctor"]}\nКабинет: {data["room"]}\nЦена: от {data["price"]} рублей\nМы вам перезвоним!', reply_markup=markup_inline)
    elif call.data.split()[0] == 'get':
        if call.data.split()[1] == 'address':
            bot.send_message(call.message.chat.id, "Санкт-Петербург, Вознесенский проспект, дом 46")
        elif call.data.split()[1] == 'work_time':
            bot.send_message(call.message.chat.id, "Пн-пт 9:00-20:00\nСб-вс 10:00-17:00")

def send_welcome(message):
    if database.Database().user_exist(message.chat.id):
        database.Database().clear_user_data(message.chat.id)
    else:
        database.Database().add_user(message.chat.id)
    mess = bot.send_message(message.chat.id, "Введите свое имя")
    bot.register_next_step_handler(mess, process_firstname_step)

def process_firstname_step(message):
    try:
        user_id = message.from_user.id
        database.Database().set_first_name_for_user(user_id, message.text)
        user_data[user_id] = User(message.text)
        mess = bot.send_message(message.chat.id, 'Введите свою фамилию')
        bot.register_next_step_handler(mess, process_secondname_step)
    except Exception as e:
        bot.reply_to(message, 'ошибка')

def process_secondname_step(message):
    try:
        user_id = message.from_user.id
        database.Database().set_second_name_for_user(user_id, message.text)
        user = user_data[user_id]
        user.second_name = message.text
        mess = bot.send_message(message.chat.id, 'Введите свой номер телефона')
        bot.register_next_step_handler(mess, process_phone_step)
    except Exception as e:
        bot.reply_to(message, 'ошибка')

def process_phone_step(message):
    try:
        user_id = message.from_user.id
        database.Database().set_phone_for_user(user_id, message.text)
        user = user_data[user_id]
        user.phone = message.text
        markup_inline = types.InlineKeyboardMarkup()
        services = database.Database().get_all_services()
        for service in services:
            markup_inline.add(types.InlineKeyboardButton(text=service[1], callback_data=f'set_service {service[0]}'))
        bot.send_message(message.chat.id, 'Выберите услугу, пожалуйста', reply_markup=markup_inline)
    except Exception as e:
        bot.reply_to(message, 'ошибка')





# для пошагового бота
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

if __name__ == "__main__":
    bot.polling(none_stop=True)