from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. I'am the exercise index!")
