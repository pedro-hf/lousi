from django.db.models import Count, Case, When, IntegerField, F, Avg, FloatField, Value
from django.db.models.functions import Cast
from random import choice
import csv
import io
import os
from django.shortcuts import render, redirect
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


def _get_questions(mode='random'):
    n = 4
    words = []
    if mode == 'random':
        for n in np.random.randint(1, 800, n):
            words.append(Word.objects.get(pk=n))
        return words
    elif mode == 'revision':
        words = Word.objects.annotate(score=Avg(Case(When(question_word=F('answer_word'), then=Value(1)),
                                                     default=Value(0), output_field=FloatField())))\
                                .order_by('score')[:4]
        return words


def test(request, question_field, answer_field, total_no_questions, current_question):
    if request.method == 'GET':
        if current_question > total_no_questions:
            return redirect(request.build_absolute_uri('/vocabulary/final_result/{}'.format(total_no_questions)))
        else:
            words = _get_questions(mode='revision')
            styles = ['btn-primary'] * len(words)
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
                       'question_field': question_field, 'answer_field': answer_field, 'current_question': current_question,
                       'total_no_questions': total_no_questions}
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

        context = {'question': question.question, 'answers': list(zip(words, styles)), 'question_field': question_field,
                   'answer_field': answer_field, 'next_question': current_question + 1,
                   'total_no_questions': total_no_questions}
        return render(request, 'vocabulary/result.html', context)


def final_result(request, total_no_questions):
    n = total_no_questions
    latest_questions = Question.objects.order_by('-id')[:n]
    correct = 0
    for question in latest_questions:
        if question.answer == question.question:
            correct += 1
    if correct / n >= 0.8:
        comment = '好勁'
    else:
        comment = 'oops...唔好'
    context = {'total_no_questions': n, 'correct': correct, 'comment': comment}
    return render(request, 'vocabulary/final_result.html', context)


def newtest(request):
    return render(request, 'vocabulary/newtest.html')


def createtest(request):
    answer = request.GET['answer_field']
    question = request.GET['question_field']
    total_no_questions = request.GET['no_q']
    return redirect('test/{}/{}/{}/{}'.format(question, answer, total_no_questions, 0))
