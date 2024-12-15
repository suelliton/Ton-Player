import requests

def get_deezer_metadata(song_name, artist_name=None):
    query = f"https://api.deezer.com/search?q=track:\"{song_name}\""
    if artist_name:
        query += f" artist:\"{artist_name}\""
    
    response = requests.get(query)
    data = response.json()

    if 'data' in data and len(data['data']) > 0:
        track = data['data'][0]
        return {
            'name': track['title'],
            'artist': track['artist']['name'],
            'album': track['album']['title'],
            'image': track['album']['cover']
        }
    return None

# Exemplo de uso
metadata = get_deezer_metadata('Shape of You', 'Ed Sheeran')
print(metadata)
