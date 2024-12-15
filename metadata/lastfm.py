import requests
#senha lastfm = Suelliton110886!
# Application name	ton player
# API key	a0d954d7c06d6b829317b56ced96a1f5
# Shared secret	ba05fe60ef1e88bd540502bcca5c840c
# Registered to	suelliton
API_KEY = 'a0d954d7c06d6b829317b56ced96a1f5'
BASE_URL = 'http://ws.audioscrobbler.com/2.0/'

def get_song_metadata(song_name, artist_name=None):
    params = {
        'method': 'track.search',
        'track': song_name,
        'api_key': API_KEY,
        'format': 'json'
    }
    if artist_name:
        params['artist'] = artist_name
    
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if 'results' in data and 'trackmatches' in data['results']:
        tracks = data['results']['trackmatches']['track']
        if tracks:
            track = tracks[0]  # Pega a primeira correspondência
            return {
                'name': track['name'],
                'artist': track['artist'],
                'album': track.get('album', 'N/A'),
                'image': track['image'][-1]['#text'] if track.get('image') else None
            }
    return None

# Exemplo de uso
metadata = get_song_metadata('Shape of You', 'Ed Sheeran')
print(metadata)
