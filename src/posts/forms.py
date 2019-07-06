from django import forms

from .models import Question, Answer,Comment


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'details')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
