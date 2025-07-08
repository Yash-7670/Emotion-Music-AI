import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import geocoder

load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                           client_secret=client_secret))

def get_user_location_name():
    try:
        g = geocoder.ip('me')
        country = g.country
        return country if country else "IN"  # fallback to India
    except Exception:
        return "IN"

def get_spotify_songs(emotion, country="IN"):
    songs = []
    try:
        query = f"{emotion} music"
        results = sp.search(q=query, type='track', limit=4, market=country)
        for item in results['tracks']['items']:
            song = {
                "title": item['name'],
                "artist": item['artists'][0]['name'],
                "url": item['external_urls']['spotify'],
                "album_cover": item['album']['images'][0]['url'],
                "preview_url": item['preview_url']
            }
            songs.append(song)
    except Exception as e:
        print(f"❌ Spotify API error: {e}")
    return songs
