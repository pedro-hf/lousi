from django.urls import path


from . import views

app_name = 'vocabulary'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.vocabulary_upload, name="upload"),
    path('test', views.test, name='test'),
    path('result', views.test, name='result')
]
