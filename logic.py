from random import randint
import requests

class Pokemon:
    pokemons = {}

    level_up_xp = [0, 10, 33, 80, 156, 270, 428, 640, 911, 1250, 1663, 2160, 2746, 3430, 4225, 5139, 6192, 7390, 8749, 10285]

    scale_factor = 1.4
    shiny_scale_factor = 1.5

    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer, pokemon_number=None):

        self.pokemon_trainer = pokemon_trainer   

        self.is_shiny = self.check_shiny()

        self.pokemon_number = randint(1,1000) if not pokemon_number or pokemon_number < 0 or pokemon_number > 1000 else pokemon_number
        self.img = self.get_img()
        self.name = self.get_name()
        self.stats = self.get_stats()

        self.level = 0
        self.xp = 0

        Pokemon.pokemons[pokemon_trainer] = self

    def check_shiny(self):
        return True if randint(1,10) <= 4 else False

    def feed(self):
        self.xp += 5 + randint(1,5)
        if self.xp >= Pokemon.level_up_xp[self.level+1]:
            self.level_up()
            return True
        return False
    
    def level_info(self):
        return f"Уровень: {self.level}, XP: {self.xp}/{Pokemon.level_up_xp[self.level + 1]}"
    
    def level_up(self):
        self.xp -= Pokemon.level_up_xp[self.level+1]
        self.level += 1

        for stat in self.stats.keys():
            self.scale_stat(stat, Pokemon.shiny_scale_factor if self.is_shiny else Pokemon.scale_factor)

    def scale_stat(self, stat_name, factor):
        self.stats[stat_name] = int(self.stats[stat_name] * factor)


    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data["sprites"]["other"]["official-artwork"]["front_default" if not self.is_shiny else "front_shiny"])
        else:
            return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png"
    
    def get_stats(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            stats = {}
            for stat in data['stats']:
                stats[stat['stat']['name']] = stat['base_stat'] * ( Pokemon.shiny_scale_factor if self.is_shiny else 1)
            return stats
        else:
            return {}
        
    def set_stat(self, stat_name, value):
        if stat_name in self.stats:
            self.stats[stat_name] = value
            return True
        else:
            print(f"Стат {stat_name} не найден у покемона {self.name}")
            return False

    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (("Shiny " if self.is_shiny else "") + data['forms'][0]['name'])
        else:
            return "Pikachu"


    # Метод класса для получения информации
    def info(self):
        return f"""Имя твоего покемона: {self.name}
    Статы покемона: {self.stats}
    {self.level_info()}"""

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img



def check_pokemon(bot):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if args[0].from_user.id not in Pokemon.pokemons.keys():
                bot.reply_to(args[0], "Ты ещё не создал себе покемона, введи /go")
                return
            
            func(*args, **kwargs)
        return wrapper
    return decorator


