from django.contrib import admin

from .models import Word, Question

admin.site.register(Word)
admin.site.register(Question)