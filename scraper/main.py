import json
import numpy as np
import os
import PIL
import random
import requests
import time
import urllib.request
from datetime import datetime
from PIL import Image

import deezer

client = deezer.Client(headers={'Accept-Language': 'en'})

all_genres = {
    'Jazz': 0,
    'R&B': 1,
    'Pop': 2,
    'Rap/Hip Hop': 3,
    'Alternative': 4,
    'Rock': 5,
    'Metal': 6,
    'Electro': 7
}

BASE_DIR = '../data/'

n_image = len(os.listdir(f"{BASE_DIR}images"))
current_genre_artists = []
target_dict = {}

with open(f'{BASE_DIR}targets.json', 'w') as json_file:
    json.dump(target_dict, json_file)


def show_cur_time(endpoint):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    return f"Scraping {endpoint} Time = {current_time}"


print(show_cur_time('Start'))

deezer_genres = client.list_genres()
for genre in (all_genres.keys()):
    print(f"{genre=}")

    n_genre = all_genres[genre]
    genre_dict = {}

    for d_genre in deezer_genres:
        if d_genre.name == genre:
            current_genre_id = d_genre.id

            current_genre_artists = client.get_genre(current_genre_id).get_artists()
            break

    for n_artist, artist in enumerate(current_genre_artists):
        print(f"{n_artist=}")
        artist_albums = artist.get_albums()
        if len(artist_albums) > 18:  # if len(albums) <= 18 then fetch all albums, otherwise fetch only 18
            fetched_artist_albums = random.sample(list(artist_albums), 18)
        else:
            fetched_artist_albums = artist_albums

        albums_arrays = []

        for album in fetched_artist_albums:
            if album.genres and album.genres[0].name == genre:

                try:
                    album_im = Image.open(requests.get(album.cover_big, stream=True).raw)

                    for album_array in albums_arrays:
                        if (np.array(album_im) == album_array).all():
                            break
                    else:
                        current_filename = f"{BASE_DIR}images/{n_image}.jpg"

                        with open(f'{BASE_DIR}targets.json', 'r') as json_file:
                            target_dict = json.load(json_file)

                        try:
                            urllib.request.urlretrieve(album.cover_big, current_filename)
                            target_dict[current_filename] = n_genre
                            n_image += 1

                            cur_album_image = Image.open(current_filename)
                            albums_arrays.append(np.array(cur_album_image))

                            with open(f'{BASE_DIR}targets.json', 'w') as json_file:
                                json.dump(target_dict, json_file)

                        except TypeError:
                            pass

                    time.sleep(0.4)
                except:
                    pass

print(show_cur_time('Finish'))
