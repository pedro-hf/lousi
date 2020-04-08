from django.db import models

class Word(models.Model):
    hanzi = models.CharField(max_length=10)
    jyutping = models.CharField(max_length=20)
    english = models.CharField(max_length=20)
    audio = models.FileField(upload_to='.')

    def __str__(self):
        return self.english
