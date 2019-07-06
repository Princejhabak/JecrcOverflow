from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'posts'

urlpatterns = [
    url(r'^$', views.my_question_list, name='question_list'),

    # url(r'^my/$', views.my_question_list, name='my_question_list'),
    # url(r'^(?P<pk>\d+)/$', views.QuestionDetailView.as_view(), name='question_detail'),

    url(r'^(?P<pk>\d+)/$', views.question_detail, name='question_detail'),
    url(r'^create/$', views.add_question, name='question_create'),
    url(r'^(?P<pk>\d+)/comment/$', views.add_comment, name='comment_create'),
    # url(r'^(?P<pk>\d+)/delete/answer/(?P<pk1>\d+)/$', views.AnswerDeleteView.as_view(), name='delete_answer'),

]
