from django.urls import path


from . import views

app_name = 'vocabulary'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.vocabulary_upload, name="upload"),
    path('test', views.test, name='test'),
    path('test/<str:question_field>/<str:answer_field>/<int:total_no_questions>/<int:current_question>',
         views.test, name='test'),
    path('result/<str:question_field>/<str:answer_field>/<int:total_no_questions>/<int:current_question>',
         views.test, name='result'),
    path('final_result/<int:total_no_questions>', views.final_result, name='final_result'),
    path('newtest', views.newtest, name='newtest'),
    path('createtest', views.createtest, name='createtest')
]
