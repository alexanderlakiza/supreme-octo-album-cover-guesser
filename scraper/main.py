import json
import os
import random
import time
import urllib.request
from datetime import datetime

import deezer

client = deezer.Client(headers={'Accept-Language': 'en'})

all_genres = [
    'Jazz',
    'R&B',
    'Pop',
    'Rap/Hip Hop',
    'Alternative',
    'Rock',
    'Metal',
    'Electronic'
]

BASE_DIR = '../data/'

n_image = len(os.listdir(f"{BASE_DIR}images"))
current_genre_artists = []
target_dict = {}

with open(f'{BASE_DIR}targets.json', 'w') as json_file:
    json.dump(target_dict, json_file)

with open(f'{BASE_DIR}targets.json', 'r') as json_file:
    target_dict = json.load(json_file)


def show_cur_time(endpoint):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    return f"Scraping {endpoint} Time = {current_time}"


print(show_cur_time('Start'))

deezer_genres = client.list_genres()
for n_genre, genre in enumerate(all_genres):
    print(f"{genre=}")

    for d_genre in deezer_genres:
        if d_genre.name == genre:
            current_genre_id = d_genre.id

            current_genre_artists = client.get_genre(current_genre_id).get_artists()
            break

    for n_artist, artist in enumerate(current_genre_artists):
        print(f"{n_artist=}")
        artist_albums = artist.get_albums()
        if len(artist_albums) > 13:  # if len(albums) <= 15 then fetch all albums, otherwise fetch only 15
            fetched_artist_albums = random.sample(list(artist_albums), 13)
        else:
            fetched_artist_albums = artist_albums

        for album in fetched_artist_albums:

            if album.genres and album.genres[0].name == genre:
                current_filename = f"{BASE_DIR}images/{n_image}.jpg"
                urllib.request.urlretrieve(album.cover_big, current_filename)
                n_image += 1
                target_dict[current_filename] = n_genre

                time.sleep(0.4)

print(show_cur_time('Start'))

with open(f'{BASE_DIR}targets.json', 'w') as json_file:
    json.dump(target_dict, json_file)
