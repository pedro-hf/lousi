from django import forms


class AnswerForm(forms.Form):
    question_id = forms.IntegerField()
    answer_id = forms.IntegerField()
    answer = forms.CharField(label='your answer was', max_length=100)

    def __repr__(self):
        return self.question_id, self.answer_id, self.answer

    def is_correct(self):
        if self.solution_id == self.answer:
            return 'Correct!'
        else:
            return 'Oops!'
