from django.db import models


import os
import uuid
from django.db import models
from pydub import AudioSegment

def convert_to_mp3(input_file):
    output_file = os.path.splitext(input_file)[0] + '.mp3'
    audio = AudioSegment.from_wav(input_file)
    audio.export(output_file, format='mp3')
    return output_file

class User(models.Model):
    name = models.CharField(max_length=255)
    token = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name

class AudioRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wav_file = models.FileField(upload_to='audio')
    mp3_file = models.FileField(upload_to='audio', null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def save(self, *args, **kwargs):
        if self.wav_file:
            self.mp3_file = convert_to_mp3(self.wav_file.path)
        super().save(*args, **kwargs)
