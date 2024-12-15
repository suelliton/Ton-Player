import peewee
from pathlib import Path
import json
from datetime import datetime
db = peewee.SqliteDatabase('database/database.db')
#como rodar: flet --ignore database.db main.py -r
#dessa forma o arquivo database.db não será ouvido pelo flet e não ocasionará em hot reload desnecessários nem travamentos


class BaseModel(peewee.Model):
    class Meta:
        database = db

class Playlist(BaseModel):
    id = peewee.AutoField()
    name = peewee.CharField(default='My Musics')
    coverart = peewee.CharField(default='/assets/default-playlist.jpg')
    created = peewee.DateTimeField(default=datetime.now())
    updated = peewee.DateTimeField(default=datetime.now())

    def save(self, *args, **kwargs):
        if self.id is not None:
            self.updated = datetime.now()
        return super().save(*args, **kwargs)
    
class Music(BaseModel):
    id = peewee.AutoField()
    playlist = peewee.ForeignKeyField(Playlist, backref='musics') 
    title = peewee.CharField(default='My music of life')
    artist = peewee.CharField(default='Unknown')
    album = peewee.CharField(default='Unknown')
    genre = peewee.CharField(default='Unknown')
    duration = peewee.CharField(default='0.00')
    coverart = peewee.CharField(default='default-music.png')
    path = peewee.CharField(default='No path')
    has_metadata = peewee.BooleanField(default=False)
    created = peewee.DateTimeField(default=datetime.now())
    updated = peewee.DateTimeField(default=datetime.now())

    def save(self, *args, **kwargs):
        if self.id is not None:
            self.updated = datetime.now()
        return super().save(*args, **kwargs)


def create_db_and_tables():
    if not Path(r'database.db').is_file():
        peewee.SqliteDatabase('database.db')
        print('Database created...')
    try:
        Playlist.create_table()
        Music.create_table()
        print('Playlist table created...')
    except peewee.OperationalError:
        print('Table error')