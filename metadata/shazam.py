import asyncio
from shazamio import Shazam
from models import Music
from threading import Thread



async def recognize_song(file_path):
    # Cria uma instância do Shazam
    shazam = Shazam()

    # Carrega o arquivo de áudio
    out = await shazam.recognize(file_path)
    # print(out.keys())
    # print(out['track']['images']['coverart'])
    # print('Track keys',out['track'].keys())
    # print('Track',out['track'])
    # Extrai metadados do resultado
    title = None
    artist = None
    album = None
    genre = None
    coverart = None

    if 'title' in out:
        title = out['title']
    elif 'track' in out:
        title = out['track']['title']

    if 'artist' in out:
        artist = out['artist']

    if 'album' in out:
        album = out['album']
    else:
        try:
            album = out['track']['sections'][0]['metadata'][0]['text']
        except:
            print('Erro ao extrair album')

    if 'track' in out:
        if 'genres' in out['track']:
            try:
                genre = out['track']['genres']['primary']
            except:
                print('Erro ao extrair genre')
        if 'subtitle' in out['track']:
            artist = out['track']['subtitle']
        
        if 'images' in out['track']:
            if 'coverart' in out['track']['images']:
                coverart = out['track']['images']['coverart']


    song_metadata = {
        'title': title ,
        'artist': artist,
        'album': album,
        'genre': genre,
        'coverart': coverart
        # 'track': out['track'] if 'track' in out else None
        # 'release_date': out['track']['releaseDate'],
        # 'duration': out['track']['duration']
    }
    
    return song_metadata


def update_metadata_music(app, music):
    # Exemplo de uso
    file_path = music.path #'/media/sueliton/CCC0F10AC0F0FC10/Users/Bruno/Music/Korean mix/Crash Landing On You - IU OST - I Will Give You My Heart [ENG SUB]-ZKCFDExYUcs.mp3'
    metadata = asyncio.run(recognize_song(file_path))
    print('-------------------------------------')
    print('metadata',metadata)
    print('-------------------------------------')

    music.title = metadata['title'] if metadata['title'] else music.title 
    music.artist = metadata['artist'] if metadata['artist'] else 'Unknown' 
    music.album = metadata['album'] if metadata['album'] else 'Unknown' 
    music.genre = metadata['genre'] if metadata['genre'] else 'Unknown' 
    music.coverart = metadata['coverart'] if metadata['coverart'] else 'default-music.png'# music.coverart 

    # if 'title' in metadata:
    #     print('updatind title to',metadata['title'])
    #     music.title = metadata['title']
    # if 'artist' in metadata:
    #     print('updatind artist to',metadata['artist'])
    #     music.artist = metadata['artist']
    # if 'album' in metadata:
    #     print('updatind album to',metadata['album'])
    #     music.album = metadata['album']
    # if 'genre' in metadata:
    #     print('updatind album to',metadata['album'])
    #     music.genre = metadata['genre']
    # if 'track' in metadata:
    #     if 'images' in metadata['track']:
    #         if 'coverart' in metadata['track']['images']:
    #             print('updatind coverart to',metadata['track']['images']['coverart'])
    #             music.coverart = metadata['track']['images']['coverart']

    music.has_metadata = True
    music.save()
    app.listen_view.update_list_musics_ui()

    return music
    # print(metadata.keys)
    # print('Timestamp',metadata['timestamp'])
    # print('Track',metadata['track'])
    # print('Tagid',metadata['tagid'])

def add_playlist_coverart(playlist, coverart, app):  
    playlist.coverart = coverart
    playlist.save()
    app.left_view.update_playlists_ui()
    
def task_update_metadata_playlist(playlist, app):
    print('Running thread')
    musics = Music.select().where(Music.playlist == playlist, Music.has_metadata == False)
    for i, music in enumerate(musics):
        music = update_metadata_music(app, music)
        if i == 0 and 'default-playlist' in playlist.coverart:
            add_playlist_coverart(playlist, music.coverart, app)
        print(music.title)

def update_metadata_playlist(app, playlist):
    print(f'Updating metadata of playlist {playlist.name}')
    thread = Thread(target=task_update_metadata_playlist, args=(playlist,app,))
    thread.start()