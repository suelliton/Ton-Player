import requests
import base64

CLIENT_ID = '2ec55646db0248a6b36927d60e0be092'
CLIENT_SECRET = 'a62692951af14557832caebd28df63c5'

def get_spotify_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    return response.json().get("access_token")

def search_song_metadata(song_name, artist_name=None):
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}
    query = f"track:{song_name}"
    if artist_name:
        query += f" artist:{artist_name}"
    
    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"
    response = requests.get(url, headers=headers)
    data = response.json()

    if data.get('tracks', {}).get('items'):
        track = data['tracks']['items'][0]
        return {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'image': track['album']['images'][0]['url'] if track['album']['images'] else None
        }
    return None

# Exemplo de uso
metadata = search_song_metadata('I Give You My Heart','IU')
print(metadata)
