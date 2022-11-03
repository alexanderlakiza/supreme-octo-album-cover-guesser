import random
import deezer
import time
import json
import urllib.request

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

genre_artist = {
    'Jazz': 'Louis Armstrong'
}

BASE_DIR = '../data/'

# for i, genre in all_genres[2:3]:

# print(client.get_genre('Jazz').get_artists())
main_info = {}

current_genre = 'Jazz'
n_image = 0

deezer_genres = client.list_genres()
for genre in deezer_genres:
    if genre.name == current_genre:
        current_genre_id = genre.id

        current_genre_artists = client.get_genre(current_genre_id).get_artists()

        break

for artist in current_genre_artists[:2]:
    artist_albums = artist.get_albums()

    for album in artist_albums:
        print(album.genres)
        if album.genres and album.genres[0].name == current_genre:
            urllib.request.urlretrieve(album.cover_big, f"{BASE_DIR}images/{n_image}.jpg")
            n_image += 1
            print(n_image)
            time.sleep(0.3)
