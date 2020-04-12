from django.db import models


class Word(models.Model):
    hanzi = models.CharField(max_length=10)
    jyutping = models.CharField(max_length=20)
    english = models.CharField(max_length=20)
    audio = models.FileField(upload_to='.')

    def __str__(self):
        return self.english


class Question(models.Model):
    answer = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='answer_word', null=True)
    question = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='question_word')
    opt1 = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='opt1')
    opt2 = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='opt2')
    opt3 = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='opt3')
    opt4 = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='opt4')
    user = models.CharField(max_length=20)
    date = models.DateTimeField()

    def __str__(self):
        return self.question
