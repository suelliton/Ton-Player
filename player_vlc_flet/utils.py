from mutagen.mp3 import MP3

def get_audio_duration(file_path):
    if file_path.endswith(".mp3"):
        audio = MP3(file_path)
    else:
        raise ValueError("Formato de arquivo não suportado.")    
    # Get duration in seconds
    duration_in_seconds = audio.info.length    
    # Convert to minutes and seconds
    minutes = int(duration_in_seconds // 60)
    seconds = int(duration_in_seconds % 60)    
    # Format like MM:SS
    duration_formatted = f"{minutes}:{seconds:02d}"
    print(f"Duration: {duration_formatted}")  
    return duration_formatted

def transform_millisseconds_to_mm_ss(millisseconds):
    # transform duration millisseconds in seconds
    duration_in_seconds = millisseconds/1000            
    # Convert to minutes and seconds
    minutes = int(duration_in_seconds // 60)
    seconds = int(duration_in_seconds % 60)            
    # Format like MM:SS
    duration_formatted = f"{minutes}:{seconds:02d}"
    print(f"Duration: {duration_formatted}")
    return duration_formatted
