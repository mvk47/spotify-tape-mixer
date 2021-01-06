import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
client_id = #your client id
client_secret = #your client secret
user_date = input("Please input the date on which you want to create "
                  "your playlist in YYYY-MM-DD format")
url = "https://www.billboard.com/charts/hot-100/"+user_date
# print(url)
response = requests.get(url=url)
songs_data = response.text
soup = BeautifulSoup(songs_data, 'html.parser')

# print(soup.prettify())
# class="chart-element__information__song text--truncate color--primary"
songs_list = []
element = soup.find_all(name="span",class_="chart-element__information__song text--truncate color--primary")
for i in range(0, 100):
    songs_list.append(element[i].text)
print(songs_list)


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                                 client_id=client_id, client_secret=client_secret,
                                 redirect_uri="http://example.com",
                                 scope="playlist-modify-private",
                                 cache_path="token.txt",
                                 show_dialog=True
                                 ))
user_id = sp.current_user()["id"]
song_uris = []
for song in songs_list:
    result = sp.search(q=f"track:{song} ", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
playlist = sp.user_playlist_create(user=user_id, name=f"{user_date} Billboard 100", public=False)
# print(playlist)

sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist["id"], tracks=song_uris)