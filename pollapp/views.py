from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
#get-read, post-create, put-change or update, delete-delete = api - application programming interface
from django.template import loader
from django.urls import reverse
from django.views import generic

from pollapp.models import Question, Choice


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'pollapp/index.html', context)
#
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'pollapp/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'pollapp/results.html', {'question': question})

class IndexView(generic.ListView):
    template_name = 'pollapp/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'pollapp/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'pollapp/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'pollapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

    return HttpResponseRedirect(reverse('pollapp:results', args=(question.id,)))
