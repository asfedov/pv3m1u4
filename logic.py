from random import randint
import requests

class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer, pokemon_number=None):

        self.pokemon_trainer = pokemon_trainer   

        self.pokemon_number = randint(1,1000) if not pokemon_number or pokemon_number < 0 or pokemon_number > 1000 else pokemon_number
        self.img = self.get_img()
        self.name = self.get_name()
        self.stats = self.get_stats()

        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data["sprites"]["other"]["official-artwork"]["front_default"])
        else:
            return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png"
    
    def get_stats(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            stats = {}
            for stat in data['stats']:
                stats[stat['stat']['name']] = stat['base_stat']
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
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"


    # Метод класса для получения информации
    def info(self):
        return f"Имя твоего покеомона: {self.name}"

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img



