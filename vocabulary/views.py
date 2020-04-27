from django.http import HttpResponse
from random import choice
import csv
import io
import os
from django.shortcuts import render
from django.contrib import messages
from .models import Word, Question
from django.conf import settings
import numpy as np
from .forms import AnswerForm
from django.utils import timezone


def index(request):
    return render(request, 'vocabulary/vocabulary_index.html')


# one parameter named request
def vocabulary_upload(request):
    # declaring template
    template = "vocabulary/vocabulary_upload.html"
    data = Word.objects.all()
    # prompt is a context variable that can have different values depending on their context
    prompt = {
        'order': 'Order of the CSV should be hanzi, jyutping, english, file',
        'profiles': data
    }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        audio_files = [f.split('_')[0] for f in os.listdir(settings.MEDIA_ROOT)]
        if column[0] in audio_files:
            audio_file = column[0] + '_0.mp3'
        else:
            audio_file = None
        _, created = Word.objects.update_or_create(
            hanzi=column[0],
            jyutping=column[1],
            english=column[2],
            audio=audio_file
        )
    context = {}
    return render(request, template, context)


def test(request):
    if request.method == 'GET':
        n = 4
        words = []
        styles = []
        for n in np.random.randint(1, 800, n):
            words.append(Word.objects.get(pk=n))
            styles.append('btn-primary')

        question_word = choice(words)
        question, created = Question.objects.update_or_create(
            question=question_word,
            answer=None,
            opt1=words[0],
            opt2=words[1],
            opt3=words[2],
            opt4=words[3],
            date=timezone.now(),
            user='guest'
        )
        context = {'question': question_word, 'answers': list(zip(words, styles)), 'question_record': question,
                   'question_field': "hanzi", 'answer_field': "english"}
        return render(request, 'vocabulary/test.html', context)

    elif request.method == 'POST':
        form = AnswerForm(request.POST)
        print(form)
        question = Question.objects.get(pk=request.POST['question_id'])
        question.answer = Word.objects.get(pk=request.POST['answer_id'])
        question.save()

        styles = []
        words = [question.opt1, question.opt2, question.opt3, question.opt4]
        for word in words:
            if word.id == question.question.id:
                styles.append('btn-success')
            elif word.id == question.answer.id:
                styles.append('btn-danger')
            else:
                styles.append('btn-secondary')

        context = {'question': question.question, 'answers': list(zip(words, styles))}
        return render(request, 'vocabulary/result.html', context)

