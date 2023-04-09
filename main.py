import telebot
import time
import json
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.remove_bg import ApiRemoveBg
from src.register_api import verifyApiRemove, registerApiRemove

TOKEN = 'TOKEN'
bot = telebot.TeleBot(token=TOKEN, parse_mode='HTML')

@bot.message_handler(commands=['start'])
def message_handle_start(message):
    if len(message.text.split()) == 2:
        api_key = message.text.split()[1]
        registerApiRemove(str(message.chat.id), api_key)

        bot.send_message(message.chat.id, 'La API Key es válida. Puedes enviar la foto que deseas remover!')

    elif (not verifyApiRemove(str(message.chat.id))):
        msg = bot.send_message(message.chat.id, '¡Hola! Bienvenido a RemoveBg-bot. Este bot utiliza la API RemoveBg para eliminar el fondo de las fotos. Para utilizar el bot, necesitas proporcionar una API Key válida de RemoveBg. \n\n <code>/start [tu_api_key]</code>',
                               reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text='Get Api Key', url='https://www.remove.bg/r/ZcHBdWKSfKLRRbaMf2Kc1N5E')]]))

    else:
        bot.send_message(message.chat.id, f'Bienvenido a RemoveBg-bot {message.from_user.first_name}. Puedes enviar la foto que deseas remover!')

@bot.message_handler(content_types=['photo'])
def message_handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file_url(file_id)
    
    msg = bot.send_message(message.chat.id, '🖼 Descargando la fotografía')
    time.sleep(5)

    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=msg.message_id,
        text='🖼 Importando la fotografía en la API de RemoveBg'
    )
    with open('src/config.json', 'r') as archivo:
        api_remove_bg = json.load(archivo)[f'{message.chat.id}']['X-Api-Key']
        remove_bg = ApiRemoveBg(api_remove_bg)

        remove_bg.publish(file_info)

    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=msg.message_id,
        text='🖼 Enviado!'
    )
    photo = open('src/photo/remove-bg.png', 'rb')
    bot.send_photo(message.chat.id, photo)

if __name__ == '__main__':
    bot.infinity_polling()