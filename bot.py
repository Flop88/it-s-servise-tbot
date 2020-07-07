import config
import telebot
from telebot import types  # кнопки
from string import Template

bot = telebot.TeleBot(config.token)

user_dict = {}


# class User:
#     def __init__(self, city):
#         self.city = city
#         # fullname, phone, device, brand, model, problem
#         keys = ['fullname', 'phone', 'device',
#                 'brand', 'model', 'problem']
#
#         for key in keys:
#             self.key = None
class User:
    def __init__(self, fullname):
        self.fullname = fullname
        self.phone = None
        self.device = None
        self.brand = None
        self.model = None
        self.problem = None


# если /help, /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('/about')
    itembtn2 = types.KeyboardButton('/reg')
    itembtn3 = types.KeyboardButton('/start')
    markup.add(itembtn1, itembtn2, itembtn3)

    bot.send_message(message.chat.id, "Здравствуйте "
                     + message.from_user.first_name
                     + ", Я бот сервисного центра *IT-S | Service*, чтобы вы хотели узнать? "
                     + "\n /about - О нашей компании "
                     + "\n /reg - Оставить заявку "
                     + "\n /start - Начать сначала ", reply_markup=markup)


# /about
@bot.message_handler(commands=['about'])
def send_about(message):
    bot.send_message(message.chat.id, "Наш сервисный центр занимается компонентным ремонтом материнских плат и"
                     + " за долгое время хорошо зарекомендовал себя на рынке услуг по ремонту техники. "
                     + "Фирма работает с 2016 года")


# /reg
@bot.message_handler(commands=["reg"])
def user_reg(message):
    # удалить старую клавиатуру
    markup = types.ReplyKeyboardRemove(selective=False)

    msg = bot.reply_to(message, """\
    Здраствуйте, Я бот сервисного центра *IT-S | Service*
    Сейчас мы с Вами составим заявку на ремонт и наши менеджеры свяжутся с Вами в ближайшее время :)
    Введите ваше имя и фамилию?
    """)

    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        # Присваиваем Имя и фамилию
        chat_id = message.chat.id
        name = message.text
        user = User(name)

        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'Введите телефон для связи')
        bot.register_next_step_handler(msg, process_device_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')



def process_device_step(message):
    try:
        # Присваиваем номер телефона
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.phone = message.text

        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        itembtn1 = types.KeyboardButton('Телефон')
        itembtn2 = types.KeyboardButton('Планшет')
        itembtn3 = types.KeyboardButton('Компьютер')
        itembtn4 = types.KeyboardButton('Ноутбук')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

        msg = bot.send_message(message.chat.id, 'Что у Вас сломалось?(Можно написать текстом :) )', reply_markup=markup)
        bot.register_next_step_handler(msg, process_brand_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def process_brand_step(message):
    try:
        # Присваиваем девайс
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.device = message.text

        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        itembtn1 = types.KeyboardButton('Apple')
        itembtn2 = types.KeyboardButton('Samsung')
        itembtn3 = types.KeyboardButton('Huawei/Honor')
        itembtn4 = types.KeyboardButton('Xiaomi')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

        msg = bot.send_message(message.chat.id, 'Кто производитель?(Можно написать текстом :) )', reply_markup=markup)
        bot.register_next_step_handler(msg, process_model_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')


def process_model_step(message):
    try:
        # Присваиваем бренд
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.brand = message.text

        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(chat_id, 'Модель устройства(Можно написать текстом :) )')
        bot.register_next_step_handler(msg, process_problem_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')



def process_problem_step(message):
    try:
        # Присваиваем модель
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.model = message.text

        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        itembtn1 = types.KeyboardButton('Не включается')
        itembtn2 = types.KeyboardButton('Не заряжается')
        itembtn3 = types.KeyboardButton('Разбит')
        itembtn4 = types.KeyboardButton('Залит')
        itembtn5 = types.KeyboardButton('Глючит')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)

        msg = bot.send_message(message.chat.id, 'Что случилось?(Можно написать текстом :) )', reply_markup=markup)
        bot.register_next_step_handler(msg, process_finish_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')



def process_finish_step(message):
    try:
        # Присваиваем проблему
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.problem = message.text

        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        # ваша заявка "Имя пользователя"
        bot.send_message(chat_id, getRegData(user, 'Ваша заявка', message.from_user.first_name), parse_mode="Markdown")
        # отправить в группу
        bot.send_message(config.chat_id, getRegData(user, 'Заявка от бота', bot.get_me().username),
                         parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, 'ooops!!')


# формирует вид заявки регистрации
# нельзя делать перенос строки Template
# в send_message должно стоять parse_mode="Markdown"
def getRegData(user, title, name):
    t = Template(
        '$title *$name* \n Имя Фамилия: *$fullname* \n Телефон: *$phone* \n Что сломалось: *$device* \n Кто производитель: *$brand* \n Модель: *$model* \n Что случилось: *$problem* ')

    return t.substitute({
        'title': title,
        'name': name,
        'fullname': user.fullname,
        'phone': user.phone,
        'device': user.device,
        'brand': user.brand,
        'model': user.model,
        'problem': user.problem,
    })


# произвольный текст
@bot.message_handler(content_types=["text"])
def send_help(message):
    bot.send_message(message.chat.id, 'О нас - /about\nОставить заявку - /reg\nГлавная - /start')


# произвольное фото
@bot.message_handler(content_types=["photo"])
def send_help_text(message):
    bot.send_message(message.chat.id, 'Напишите текст')


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)