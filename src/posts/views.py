from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from .forms import QuestionForm, AnswerForm, CommentForm
from django.utils import timezone
from django.db.models import Q
from django.urls import reverse_lazy
from django.db import IntegrityError

from .models import Question, Answer, Comment


class QuestionListView(ListView):
    model = Question

    def get_queryset(self):

        request = self.request
        query = request.GET.get('q')
        if query is not None:
            lookups = Q(text__icontains=query)  # | Q(details__icontains=query)
            return Question.objects.filter(lookups).distinct()
        else:
            return Question.objects.all()


# class QuestionDetailView(DetailView):
#     model = Question
#     print(Question.objects.get(id=1))
#     template_name = 'posts/question_detail.html'


def question_detail(request, pk):
    question = Question.objects.get(pk=pk)
    answers = Answer.objects.filter(question=question)

    comments = Comment.objects.all()
    x = 0

    if request.method == "POST":

        answer_form = AnswerForm(request.POST)

        if answer_form.is_valid():
            answer = answer_form.save(commit=False)

            answer.question = question
            answer.user = request.user
            answer.text = answer_form.cleaned_data['text']
            answer.date = timezone.now()
            answer.save()

            return redirect('posts:question_detail', pk=pk)

    else:
        answer_form = AnswerForm()

    return render(request, 'posts/question_detail.html',
                  {'question': question, 'answers': answers, 'answer_form': answer_form, 'comments': comments, 'x': x})


def my_question_list(request):
    query = request.GET.get('q')
    if query is not None:
        question_list = Question.objects.filter(user=request.user, text__icontains=query)
    else:
        question_list = Question.objects.filter(user=request.user)

    return render(request, 'posts/question_list.html', {'question_list': question_list})


# class QuestionCreateView(CreateView):
#     fields = ['text', 'details']
#     model = Question
#     template_name = 'posts/question_form.html'


def add_question(request):
    # question = get_object_or_404(Question)

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)

            question.user = request.user
            question.text = form.cleaned_data['text']
            question.details = form.cleaned_data['details']
            question.created_date = timezone.now()
            question.save()

            # return redirect('question_detail', pk=post.pk)
            return redirect('posts:question_list')
    else:
        form = QuestionForm()
    return render(request, 'posts/question_form.html', {'form': form})


def add_comment(request, pk):
    answer = Answer.objects.get(pk=pk)
    # print(answer.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)

            comment.answer = answer
            comment.user = request.user
            comment.text = form.cleaned_data['text']
            comment.date = timezone.now()
            comment.save()

            # return redirect('posts:question_list')
            return redirect('posts:question_detail', pk=answer.question.id)

    else:
        form = CommentForm()
    return render(request, 'posts/comment_form.html', {'form': form})


# class AnswerDeleteView(DeleteView):
#     model = Answer
#     success_url = reverse_lazy('home')
