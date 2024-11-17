import random

def extract_city(text, cities_list):
    words = text.split()
    cities = [city for city in words if city.lower() in (c.lower() for c in cities_list)]
    if len(cities) == 1:
        return cities[0]
    return None

def is_valid_city(city, last_letter):
    return city[0].lower() == last_letter.lower()

def is_used_city(city, used_cities):
    return city in used_cities

def get_last_letter(city):
    for char in reversed(city):
        if char not in 'ьъы':
            return char
    return ''

def bot_respond(last_letter, cities_list, used_cities, level):
    delta = random.random()
    result = delta < 0.3 if level == 'Легкий' else (delta < 0.2 if level == 'Средний' else delta < 0.1)
    if not result:
        possible_cities = [city['name'] for city in cities_list if city['name'][0].lower() == last_letter.lower() and city['name'] not in used_cities and city['country_id'] == '3159']
        if len(possible_cities) > 0:
            return random.choice(possible_cities)
        possible_cities = [city['name'] for city in cities_list if city['name'][0].lower() == last_letter.lower() and city['name'] not in used_cities]
        return random.choice(possible_cities) if possible_cities else None
    return None

def bot_first_respond(cities_list):
    possible_cities = [city['name'] for city in cities_list if city['country_id'] == '3159']
    return random.choice(possible_cities) if possible_cities else None

def who_first_start():
    return random.choice(['Бот', 'Пользователь'])
