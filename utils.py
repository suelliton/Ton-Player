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
    
    # Obtém a duração em segundos
    duration_in_seconds = audio.info.length
    
    # Converte para minutos e segundos
    minutes = int(duration_in_seconds // 60)
    seconds = int(duration_in_seconds % 60)
    
    # Formata como MM:SS
    duration_formatted = f"{minutes}:{seconds:02d}"
    print(f"Duração: {duration_formatted}")
    
    return duration_formatted

def find_control_by_key(page, key_name):
    """
    Busca recursivamente um controle com a key especificada na página.
    
    :param page: A página ou controle base para a busca.
    :param key_name: O nome da key a ser buscada.
    :return: O controle encontrado ou None se não for encontrado.
    """
    # Função interna recursiva
    def search_controls(controls):
        for control in controls:
            if control.key == key_name:
                return control
            # Verifica controles filhos recursivamente
            if hasattr(control, "controls"):
                found = search_controls(control.controls)
                if found:
                    return found
        return None

    # Começa a busca a partir dos controles da página
    return search_controls(page.controls)

def find_control_by_key_in_control(control, key_name):
    """
    Busca recursivamente um controle com a key especificada dentro de um controle dado.
    
    :param control: O controle base para a busca.
    :param key_name: O nome da key a ser buscada.
    :return: O controle encontrado ou None se não for encontrado.
    """
    # Função interna recursiva
    def search_controls(controls):
        for child in controls:
            if child.key == key_name:
                return child
            # Verifica controles filhos recursivamente
            if hasattr(child, "controls"):
                found = search_controls(child.controls)
                if found:
                    return found
        return None

    # Começa a busca nos controles filhos do controle base
    return search_controls(control.controls if hasattr(control, "controls") else [])
