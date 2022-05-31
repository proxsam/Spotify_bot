import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = "2000-01-01"
CLIENT_ID = "9a6359dc7c9c4793849258ee44e44584"
CLIENT_SECRET = "fb7c56f702614fdaa0d301cb7a734020"
REDIRECT_URI = "http://example.com"

response = requests.get("https://www.billboard.com/charts/hot-100/2000-08-12/")
billboard_page = response.text

soup = BeautifulSoup(billboard_page, "html.parser")
data = soup.select("li h3")

songs = [song.text.strip("\n") for song in data[:100]]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        show_dialog=True,
        cache_path="token.txt"
    )
)
USER_ID = sp.current_user()['id']

song_uri_list = []
for song in songs:
    song_search = sp.search(q=f"{song} year{2000}", type="track", limit=1)
    try:
        song_search_uri = song_search['tracks']['items'][0]['uri']
        song_uri_list.append(song_search_uri)
    except IndexError:
        print(f"Cant find the song {song} skipped")

playlist = sp.user_playlist_create(user=USER_ID, name=f"{date} Billboard 100", public=False)

sp.user_playlist_add_tracks(user=USER_ID, playlist_id=playlist["id"], tracks=song_uri_list)
