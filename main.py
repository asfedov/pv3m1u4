import telebot 
from config import token

from logic import Pokemon, check_pokemon

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет, для начала игры введи /go")

@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.id not in Pokemon.pokemons.keys():
        pokemon = Pokemon(message.from_user.id)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['cheat'])
def cheat(message):
    arguments = telebot.util.extract_arguments(message.text).split()
    pokemon = Pokemon(message.from_user.id, int(arguments[0]))
    bot.send_message(message.chat.id, pokemon.info())
    bot.send_photo(message.chat.id, pokemon.show_img())


@bot.message_handler(commands=['show'])
@check_pokemon(bot)
def show(message):
    pokemon = Pokemon.pokemons[message.from_user.id]
    bot.send_photo(message.chat.id, pokemon.show_img())
    bot.send_message(message.chat.id, pokemon.info())


@bot.message_handler(commands=['setstat'])
@check_pokemon(bot)
def set_stat(message):
    arguments = telebot.util.extract_arguments(message.text).split()
    pokemon = Pokemon.pokemons[message.from_user.id]
    is_changed = pokemon.set_stat(arguments[0], int(arguments[1]))
    bot.send_message(message.chat.id, f"Стат {arguments[0]} изменён на {arguments[1]}" if is_changed else f"Стат {arguments[0]} не найден у покемона {pokemon.name}")


@bot.message_handler(commands=['feed'])
@check_pokemon(bot)
def feed(message):
    pokemon = Pokemon.pokemons[message.from_user.id]
    is_levelup = pokemon.feed()
    bot.send_message(message.chat.id, f"Ты покормил своего покемона {pokemon.name}. {"Он достиг " + str(pokemon.level) + "уровня! Поздравляю!" if is_levelup else "" }\n{pokemon.level_info()}")


bot.infinity_polling(none_stop=True)

