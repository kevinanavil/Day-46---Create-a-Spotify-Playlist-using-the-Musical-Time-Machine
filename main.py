import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

#find songs in that date
#date = input("What date you want to go back (YYYY-MM-DD): ")
date = "2001-10-11"
URL = "https://www.billboard.com/charts/hot-100/" + date
response = requests.get(URL)
billboard = response.text
soup = BeautifulSoup(billboard, "html.parser")
titles = soup.find_all(name="li", class_="o-chart-results-list__item // lrv-u-flex-grow-1 lrv-u-flex lrv-u-flex-direction-column lrv-u-justify-content-center lrv-u-border-b-1 u-border-b-0@mobile-max lrv-u-border-color-grey-light lrv-u-padding-l-050 lrv-u-padding-l-1@mobile-max")
file_path = "C:\\Users\\kev51\\Documents\\VSCode\\Web Development Projects\\Day 46 - Create a Spotify Playlist using the Musical Time Machine\\musics.txt"
songs_names = []

with open(file_path, "w", encoding="utf-8") as file:
    li_tags = soup.find_all(name="li", class_="o-chart-results-list__item")

    for li in li_tags:
        h3_tag = li.find("h3", class_="c-title")

        if h3_tag:
            title = h3_tag.get_text(strip=True)
            file.write(f"{title}\n")
            songs_names.append(title)
    print(songs_names)


#Spotify auth
SPOTIPY_REDIRECT_URI = "http://example.com"
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

#Spotify Authentication
spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = spotify.current_user()["id"]
print(user_id)

#Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in songs_names:
    result = spotify.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist = spotify.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

#Adding songs found into the new playlist
spotify.playlist_add_items(playlist_id=playlist["id"], items=song_uris)



       