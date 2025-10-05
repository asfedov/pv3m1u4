import telebot 
from config import token

from logic import Pokemon

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет, для начала игры введи /go")

@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        pokemon = Pokemon(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['cheat'])
def cheat(message):
    arguments = telebot.util.extract_arguments(message.text).split()
    pokemon = Pokemon(message.from_user.username, int(arguments[0]))
    bot.send_message(message.chat.id, pokemon.info())
    bot.send_photo(message.chat.id, pokemon.show_img())


@bot.message_handler(commands=['show'])
def show(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
        bot.send_message(message.chat.id, f"Статы покемона: {pokemon.stats}")
    else:
        bot.reply_to(message, "Ты ещё не создал себе покемона, введи /go")

@bot.message_handler(commands=['setstat'])
def set_stat(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        arguments = telebot.util.extract_arguments(message.text).split()
        pokemon = Pokemon.pokemons[message.from_user.username]
        is_changed = pokemon.set_stat(arguments[0], int(arguments[1]))
        bot.send_message(message.chat.id, f"Стат {arguments[0]} изменён на {arguments[1]}" if is_changed else f"Стат {arguments[0]} не найден у покемона {pokemon.name}")
    else:
        bot.reply_to(message, "Ты ещё не создал себе покемона, введи /go")


bot.infinity_polling(none_stop=True)

