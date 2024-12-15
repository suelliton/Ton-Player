from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TPE1, TIT2, TALB, TCON, error
from threading import Thread
from models import Music
import os
import requests
import time

def read_mp3_metadata(file_path):
    try:
        # Carrega o arquivo MP3 com suporte ao ID3
        audio = MP3(file_path, ID3=EasyID3)

        # Obtém os valores dos metadados (se existirem)
        metadata = {
            "title": audio.get("title", [None])[0],
            "artist": audio.get("artist", [None])[0],
            "album": audio.get("album", [None])[0],
            "genre": audio.get("genre", [None])[0],
            "tracknumber": audio.get("tracknumber", [None])[0],
            "date": audio.get("date", [None])[0],
        }

        # Retorna os metadados
        return metadata
    except Exception as e:
        print(f"Erro ao ler os metadados: {e}")
        return None

def read_metadata(path='/home/sueliton/Músicas/teste/All My Dreams - Roxi Drive.mp3'):
    metadata = read_mp3_metadata(path)

    if metadata:
        print("Metadados do arquivo:")
        for key, value in metadata.items():
            print(f"{key.capitalize()}: {value}")

# read_metadata()



def extract_mp3_metadata(mp3_file_path, output_folder="coverart"):
    try:
        # Verifica se o arquivo existe
        if not os.path.exists(mp3_file_path):
            raise FileNotFoundError(f"O arquivo {mp3_file_path} não existe.")

        # Carrega o arquivo MP3
        audio = MP3(mp3_file_path, ID3=ID3)

        # Cria a pasta de saída, se não existir
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Inicializa o dicionário de metadados
        metadata = {
            "title": None,
            "artist": None,
            "album": None,
            "genre": None,
            "coverart_path": None
        }

        # Extrai os metadados básicos
        metadata["title"] = audio.tags.get(TIT2.__name__, None)
        metadata["artist"] = audio.tags.get(TPE1.__name__, None)
        metadata["album"] = audio.tags.get(TALB.__name__, None)
        metadata["genre"] = audio.tags.get(TCON.__name__, None)

        # Remove os objetos de metadados para extrair apenas valores
        metadata = {key: (value.text[0] if value else None) for key, value in metadata.items() if key != "coverart_path"}

        # Procura a arte da capa (APIC)
        for tag in audio.tags.values():
            if isinstance(tag, APIC):
                # Define o nome do arquivo da arte da capa
                coverart_filename = os.path.join(
                    output_folder,
                    f"{os.path.splitext(os.path.basename(mp3_file_path))[0]}_cover.jpg"
                )

                # Salva a imagem localmente
                with open(coverart_filename, "wb") as img_file:
                    img_file.write(tag.data)

                # Adiciona o caminho ao dicionário de metadados
                metadata["coverart_path"] = coverart_filename
                break

        return metadata

    except Exception as e:
        print(f"Erro ao extrair os metadados: {e}")
        return None


def add_coverart_to_mp3_file(mp3_path, image_path):
    print(f'Adding coverart to mp3 file{mp3_path}')
    try:
        # Carrega o arquivo MP3 e verifica as tags
        audio = MP3(mp3_path, ID3=ID3)

        # Adiciona a tag ID3 se não existir
        if audio.tags is None:
            audio.add_tags()

        # Lê a imagem da capa
        with open(image_path, 'rb') as img_file:
            image_data = img_file.read()

        # Adiciona a imagem como uma tag APIC (Attached Picture)
        audio.tags.add(
            APIC(
                encoding=3,          # UTF-8
                mime='image/jpeg',   # MIME type da imagem (use 'image/png' se for PNG)
                type=3,              # 3 = capa frontal (front cover)
                desc='Cover',        # Descrição da imagem
                data=image_data      # Dados binários da imagem
            )
        )

        # Salva o arquivo com a capa
        audio.save()
        print(f"Capa adicionada ao arquivo {mp3_path}")

    except error as e:
        print(f"Erro ao adicionar a capa: {e}")


def download_image(url, save_path, filename):
    print(f'Downloading image from {url}')
    print(f'Saving image in {save_path}')
    try:
        # Faz a requisição GET para baixar a imagem
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Verifica se houve algum erro na requisição
        
        # Cria o diretório se não existir
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        # Define o caminho completo para salvar a imagem
        full_path = os.path.join(save_path, filename)
        
        # Salva o conteúdo da imagem em um arquivo
        with open(full_path, "wb") as file:
            for chunk in response.iter_content(1024):  # Baixa em pedaços para eficiência
                file.write(chunk)
        
        print(f"Imagem salva em: {full_path}")
        return full_path

    except Exception as e:
        print(f"Erro ao baixar a imagem: {e}")
        return None

def write_mp3_metadata(music):   
    
    try:
        # Carrega o arquivo MP3 com suporte ao ID3
        if music.coverart.startswith('https'):
            download_image(music.coverart, 'coverart',f'{music.title}')
            # time.sleep(1)            
            add_coverart_to_mp3_file(music.path, f'coverart/{music.title}')
            # add_coverart_to_mp3_file(music.path, f'coverart/lee.jpg')
        else:
            add_coverart_to_mp3_file(music.path, music.coverart)

        #esta parte serve para os demais metadados com EasyID3
        audio = MP3(music.path, ID3=EasyID3)
        # Atualiza os campos necessários
        if music.title:
            audio['title'] = music.title
        if music.artist:
            audio['artist'] = music.artist
        if music.album:
            audio['album'] = music.album
        if music.genre:
            audio['genre'] = music.genre
        
        # Salva as alterações no arquivo
        audio.save()       
        
        # Formata o novo nome do arquivo
        title = music.title or audio.get('title', [None])[0]
        artist = music.artist or audio.get('artist', [None])[0]

        if title and artist:
            # Gera o novo nome no formato "nome da música - artista.mp3"
            new_file_name = f"{title} - {artist}.mp3"

            # Garante que o nome não tenha caracteres inválidos para o sistema de arquivos
            new_file_name = ''.join(c for c in new_file_name if c not in r'\/:*?"<>|')
            
            # Define o novo caminho para o arquivo
            new_file_path = os.path.join(os.path.dirname(music.path), new_file_name)

            # Renomeia o arquivo
            os.rename(music.path, new_file_path)
            print(f"Arquivo renomeado para: {new_file_path}")
            music.path = new_file_path
            music.save()
        else:
            print("Não foi possível renomear o arquivo: Título ou artista ausente.")
    except Exception as e:
        print(f"Erro ao atualizar os metadados: {e}")


def task_update_mp3_files_playlist(playlist):
    print('Running thread')
    musics = Music.select().where(Music.playlist==playlist)
    for music in musics:
        write_mp3_metadata(music)


def update_mp3_files_playlist(playlist):
    print('Updating mp3 files metadata from hard disc')
    thread = Thread(target=task_update_mp3_files_playlist, args=(playlist,))
    thread.start()


