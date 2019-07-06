from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField  #for adding upload from our own server in CKEDITOR
from django.core.exceptions import ValidationError
# from ckeditor.fields import RichTextField  #does not contain upload option for us in Images

User = get_user_model()


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    details = RichTextUploadingField(config_name='special')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    # def get_absolute_url(self):
    #     return reverse('posts:question_detail', kwargs={'pk': self.pk})

    def clean(self, *args, **kwargs):
        text = self.text
    
        question_list = Question.objects.filter(user=User.objects.first())
        for question in question_list:
            if question.text == text:
                raise ValidationError("Question already exists")
        return super(Question, self).clean(*args, **kwargs)


    class Meta:
        ordering = ['-created_date']
        unique_together = ['user', 'text']


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = RichTextUploadingField(config_name='special')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        unique_together = ['question', 'user']


class Comment(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        unique_together = ['text', 'user']


# class Upvote(models.Model):
#     answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     vote = models.BooleanField(default=False)
