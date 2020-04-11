from django import forms


class AnswerForm(forms.Form):
    answer = forms.CharField(label='your answer', max_length=100)

