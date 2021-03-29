from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from settings import TG_TOKEN
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup

def start(bot, update):
    print('Кто-то отправил команду /start')
    bot.message.reply_text('Здравствуйте, {}! Я бот стоматологической клиники "Бриллиант"!'
                           ' \nВы можете ознакомиться с нашим местоположением и часами работы, '
                           'а также заполнить анкету и записаться на приём.'
                           .format(bot.message.chat.first_name), reply_markup=get_keyboard())

def parrot(bot, update):
    print(bot.message.text)
    bot.message.reply_text(bot.message.text)

def close_keyboard(bot, update):
    bot.message.reply_text('Ok', reply_markup=ReplyKeyboardRemove())

def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup([['/adress', '/work_time'], ['/anketa']], resize_keyboard=True)
    return my_keyboard

def adress(bot, update):
    bot.message.reply_text('Адрес: Россия, Санкт-Петербург, Вознесенский проспект, д. 46')

def time(bot, update):
    bot.message.reply_text('Время работы: пн-пт, 9:00 - 18:00')

def anketa(bot, update):
    bot.message.reply_text('Услуга записи пока недоступна')

def main():
    my_bot = Updater(TG_TOKEN, use_context=True)
    my_bot.dispatcher.add_handler(CommandHandler('start', start))
    my_bot.dispatcher.add_handler(CommandHandler('close', close_keyboard))
    my_bot.dispatcher.add_handler(CommandHandler('adress', adress))
    my_bot.dispatcher.add_handler(CommandHandler('work_time', time))
    my_bot.dispatcher.add_handler(CommandHandler('anketa', anketa))
    # my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))
    my_bot.start_polling()
    my_bot.idle()

main()
