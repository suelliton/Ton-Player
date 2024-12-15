from mutagen.mp3 import MP3

def sanitize_metadata(metadata):
    if metadata['artist'] == None:
        metadata['artist'] = 'Unknown'
    
    if metadata['album'] == None:
        metadata['album'] = 'Unknown'
    
    if metadata['genre'] == None:
        metadata['genre'] = 'Unknown'
    
    if 'coverart_path' not in metadata:
        metadata['coverart_path'] = 'assets/default-music.png'
    return metadata

def get_audio_duration(file_path):
    if file_path.endswith(".mp3"):
        audio = MP3(file_path)   
    else:
        raise ValueError("Formato de arquivo não suportado.")
    print(f"Duração: {audio.info.length/60:.2f} segundos")        
    return round(audio.info.length/60,2)



