from django.db import models

# 반드시 makemigrations, migrate 진행, inspectdb 통한 db 정보 읽어오고 작성
class Albums(models.Model):
    album_id = models.CharField(primary_key=True, max_length=50)
    album_name = models.CharField(max_length=150, blank=True, null=True)      
    album_artist = models.CharField(max_length=50, blank=True, null=True)     
    album_genre = models.CharField(max_length=50, blank=True, null=True)      
    album_image = models.CharField(max_length=150, blank=True, null=True)     
    album_release_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'albums'


class Alternative(models.Model):
    track_id = models.CharField(primary_key=True, max_length=50)
    acousticness = models.FloatField(blank=True, null=True)
    danceability = models.FloatField(blank=True, null=True)
    energy = models.FloatField(blank=True, null=True)
    loudness = models.FloatField(blank=True, null=True)
    speechiness = models.FloatField(blank=True, null=True)
    tempo = models.FloatField(blank=True, null=True)
    valence = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alternative'


class AudioFeatures(models.Model):
    track = models.OneToOneField('Tracks', models.DO_NOTHING, primary_key=True)
    acousticness = models.FloatField(blank=True, null=True)
    danceability = models.FloatField(blank=True, null=True)
    energy = models.FloatField(blank=True, null=True)
    loudness = models.FloatField(blank=True, null=True)
    speechiness = models.FloatField(blank=True, null=True)
    tempo = models.FloatField(blank=True, null=True)
    valence = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audio_features'

        
class Electro(models.Model):
    track_id = models.CharField(primary_key=True, max_length=50)
    acousticness = models.FloatField(blank=True, null=True)
    danceability = models.FloatField(blank=True, null=True)
    energy = models.FloatField(blank=True, null=True)
    loudness = models.FloatField(blank=True, null=True)
    speechiness = models.FloatField(blank=True, null=True)
    tempo = models.FloatField(blank=True, null=True)
    valence = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'electro'


class Hiphop(models.Model):
    track_id = models.CharField(primary_key=True, max_length=50)
    acousticness = models.FloatField(blank=True, null=True)
    danceability = models.FloatField(blank=True, null=True)
    energy = models.FloatField(blank=True, null=True)
    loudness = models.FloatField(blank=True, null=True)
    speechiness = models.FloatField(blank=True, null=True)
    tempo = models.FloatField(blank=True, null=True)
    valence = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hiphop'


class Indiepop(models.Model):
    track_id = models.CharField(primary_key=True, max_length=50)
    acousticness = models.FloatField(blank=True, null=True)
    danceability = models.FloatField(blank=True, null=True)
    energy = models.FloatField(blank=True, null=True)
    loudness = models.FloatField(blank=True, null=True)
    speechiness = models.FloatField(blank=True, null=True)
    tempo = models.FloatField(blank=True, null=True)
    valence = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'indiepop'


class Jazz(models.Model):
    track_id = models.CharField(primary_key=True, max_length=50)
    acousticness = models.FloatField(blank=True, null=True)
    danceability = models.FloatField(blank=True, null=True)
    energy = models.FloatField(blank=True, null=True)
    loudness = models.FloatField(blank=True, null=True)
    speechiness = models.FloatField(blank=True, null=True)
    tempo = models.FloatField(blank=True, null=True)
    valence = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jazz'


class Jpop(models.Model):
    track_id = models.CharField(primary_key=True, max_length=50)
    acousticness = models.FloatField(blank=True, null=True)
    danceability = models.FloatField(blank=True, null=True)
    energy = models.FloatField(blank=True, null=True)
    loudness = models.FloatField(blank=True, null=True)
    speechiness = models.FloatField(blank=True, null=True)
    tempo = models.FloatField(blank=True, null=True)
    valence = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jpop'


class Kpop(models.Model):
    track_id = models.CharField(primary_key=True, max_length=50)
    acousticness = models.FloatField(blank=True, null=True)
    danceability = models.FloatField(blank=True, null=True)
    energy = models.FloatField(blank=True, null=True)
    loudness = models.FloatField(blank=True, null=True)
    speechiness = models.FloatField(blank=True, null=True)
    tempo = models.FloatField(blank=True, null=True)
    valence = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kpop'


class Latin(models.Model):
    track_id = models.CharField(primary_key=True, max_length=50)
    acousticness = models.FloatField(blank=True, null=True)
    danceability = models.FloatField(blank=True, null=True)
    energy = models.FloatField(blank=True, null=True)
    loudness = models.FloatField(blank=True, null=True)
    speechiness = models.FloatField(blank=True, null=True)
    tempo = models.FloatField(blank=True, null=True)
    valence = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'latin'


class Rnb(models.Model):
    track_id = models.CharField(primary_key=True, max_length=50)
    acousticness = models.FloatField(blank=True, null=True)
    danceability = models.FloatField(blank=True, null=True)
    energy = models.FloatField(blank=True, null=True)
    loudness = models.FloatField(blank=True, null=True)
    speechiness = models.FloatField(blank=True, null=True)
    tempo = models.FloatField(blank=True, null=True)
    valence = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rnb'


class Rock(models.Model):
    track_id = models.CharField(primary_key=True, max_length=50)
    acousticness = models.FloatField(blank=True, null=True)
    danceability = models.FloatField(blank=True, null=True)
    energy = models.FloatField(blank=True, null=True)
    loudness = models.FloatField(blank=True, null=True)
    speechiness = models.FloatField(blank=True, null=True)
    tempo = models.FloatField(blank=True, null=True)
    valence = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rock'


class Tracks(models.Model):
    track_id = models.CharField(primary_key=True, max_length=50)
    track_name = models.CharField(max_length=150, blank=True, null=True)      
    track_preview = models.CharField(max_length=150, blank=True, null=True)   
    album = models.ForeignKey(Albums, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tracks'

