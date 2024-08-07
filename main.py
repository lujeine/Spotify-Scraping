import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify Authentication
SPOTIFY_CLIENT_ID = 'XXX'
SPOTIFY_CLIENT_SECRET = 'XXX'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private,playlist-modify-public",
                                               show_dialog=True,
                                               cache_path="token.txt"))

user_id = sp.current_user()["id"]

# Scraping Billboard 100
date = input("Enter a date in YYYY-MM-DD format: ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
soup = BeautifulSoup(response.text, "html.parser")
songs = soup.select("li ul li h3")

songs_titles = []
for song in songs:
    songs_titles.append(song.getText().strip())

# Search songs in Spotify
song_uris = []
year = date.split("-")[0]
for song in songs_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Create a new private playlist
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

# Add songs to the playlist
sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)
print(f"Added {len(song_uris)} songs to the playlist.")
