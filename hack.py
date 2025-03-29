import json
import numpy as np
import requests
from time import sleep
import random

host = "http://172.18.4.158:8000"
post_url = f"{host}/submit-word"
get_url = f"{host}/get-word"
status_url = f"{host}/status"

NUM_ROUNDS = 5

# Iau cuvintele din fisier
with open("words.json", "r") as file:
    words_data = json.load(file)

# Transform dictionarul intr-o lista de tuple (id, text, cost)
words_list = [(int(k), v["text"], v["cost"]) for k, v in words_data.items()]

battle_map = {
    "Feather" : "Wind",
    "Coal" : "Water",
    "Pebble" : "Explosion",
    "Leaf" : "Flame",
    "Paper" : "Flame",
    "Rock" : "Paper",
    "Water" : "Tsunami",
    "Twig" : "Flame",
    "Sword" : "Shield",
    "Shield" : "War",
    "Gun" : "Explosion",
    "Flame" : "Water",
    "Rope" : "Sword",
    "Disease" : "Cure",
    "Cure" : "War",
    "Bacteria": "Cure",
    "Shadow" : "Light",
    "Light" : "Moon",
    "Virus" : "Vaccine",
    "Sound" : "Peace",
    "Time" : "Gravity",
    "Fate" : "Karma",
    "Earthquake" : "Tectonic Shift",
    "Storm" : "Tsunami",
    "Vaccine" : "Fate",
    "Logic" : "Time",
    "Gravity" : "Time",
    "Robots" : "Human Spirit",
    "Stone" : "Explosion",
    "Echo" : "Explosion",
    "Thunder" : "Antimatter",
    "Karma" : "Fate",
    "Wind" : "Supernova",
    "Ice" : "Flame",
    "Sandstorm" : "Earthquake",
    "Laser" : "Explosion",
    "Magma" : "Volcano",
    "Peace" : "War",
    "Explosion" : "Nuclear Bomb",
    "War" : "Peace",
    "Enlightenment" : "Rebirth",
    "Nuclear Bomb" : "Supernova",
    "Volcano" :  "Apocalyptic Meteor",
    "Whale" : "Earth",
    "Earth" : "Apocalyptic Meteor",
    "Moon" : "Supernova",
    "Star" : "Supernova",
    "Tsunami" : "Sandstorm",
    "Supernova" : "Neutron Star",
    "Antimatter" : "Feather",
    "Plague" : "Cure",
    "Rebirth" : "Human Spirit",
    "Tectonic Shift" : "Earth’s Core",
    "Gamma-Ray Burst" : "Neutron Star",
    "Human Spirit" : "Robots",
    "Apocalyptic Meteor" : "Neutron Star",
    "Earth’s Core" : "Moon",
    "Neutron Star" : "Light",
    "Supermassive Black Hole" : "Feather",
    "Entropy" : "Pebble",
}

# Transform un cuvant intr-un vector de frecventa a literelor
def word_to_vector(word):
    vector = np.zeros(26)
    for char in word.lower():
        if 'a' <= char <= 'z':  # Ignor caracterele non-alfabetice
            vector[ord(char) - ord('a')] += 1
    return vector

# Calculez similaritatea cosine intre doi vectori
def cosine_similarity(vec1, vec2):
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0  # Evită împărțirea la zero
    return np.dot(vec1, vec2) / (norm1 * norm2)

# Gasesc cel mai apropiat cuvant din words_list
def find_most_similar(word):
    sys_vector = word_to_vector(word)
    max_similarity = -1
    best_match = None

    for _, candidate_word, _ in words_list:
        candidate_vector = word_to_vector(candidate_word)
        similarity = cosine_similarity(sys_vector, candidate_vector)
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = candidate_word

    return best_match

def what_beats(word):
    most_similar_word = find_most_similar(word)
    if most_similar_word in battle_map:
        return battle_map[most_similar_word]
    return random.choice(words_list)[1]  # Daca nu am in battle_map, aleg random

def play_game(player_id):
    for round_id in range(1, NUM_ROUNDS+1):
        round_num = -1
        while round_num != round_id:
            response = requests.get(get_url)
            sys_word = response.json()['word']
            round_num = response.json()['round']
            print(f"🔄 Round {round_num}: System played {sys_word}")
            sleep(1)

        if round_id > 1:
            status = requests.get(status_url)
            print(status.json())

        chosen_word = what_beats(sys_word)
        print(f"✅ Round {round_id}: I played {chosen_word}")

        chosen_word_id = next((k for k, v in words_data.items() if v["text"] == chosen_word), None)
        if chosen_word_id is None:
            print("❌ Error: Word not found in words_data.")
            return

        data = {"player_id": player_id, "word_id": int(chosen_word_id), "round_id": round_id}
        response = requests.post(post_url, json=data)
        print(response.json())

play_game(player_id="AO4CUVWeGn")
