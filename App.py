import telebot
from Config import keys, TOKEN
from extensions import APIException, Converter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = '''Привет! Этот бот поможет вам в конвертации валют! Для начала необходимо – отправить мне название необходимой валюты!'''
    bot.send_message(message.chat.id,text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
   text = 'Доступные виды:'
   for key in keys.keys():
       text = '\n'.join((text,key, ))
   bot.send_message(message.chat.id,text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
      try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Ошибка! Слишком много параметров для расчета!')
        quote, base, amount = values
        total_base = Converter.get_price(quote, base, amount)
      except APIException as e:
          bot.send_message(message.chat.id, f'Ошибка! Неверный ввод: {e}')
      except Exception as e:
          bot.send_message(message.chat.id, f'Ошибка! Не удается обработать команду: {e}')
      else:
        number = total_base * float(amount)
        number = round(number, 4)
        text = f'Цена {amount} {quote} в {base} равняется {number}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
