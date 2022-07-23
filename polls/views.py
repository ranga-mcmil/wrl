from multiprocessing import context
from multiprocessing.connection import answer_challenge
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RemarkForm, StudentNameForm, StudentRemarkForm
from .models import Question, Choice, Remark, Survey, StudentName, StudentRemark 
from accounts.models import User  
from django.contrib import messages


def index(request):
    if request.user.type == 'WORK_SUPERVISOR':
        latest_question_list = Question.objects.all()
        surveys = Survey.objects.all()
        userIn = False
        users = []
        for survey in surveys:
            users.append(survey.user.username)

        if request.user.username in users:
            userIn = True
        context = {'latest_question_list': latest_question_list, 'userIn': userIn}
        return render(request, 'polls/index.html', context)
    elif request.user.type == 'SUPERVISOR':
        surveys = Survey.objects.all()
        users = []
        supervising = []
        for survey in surveys:
            if survey.user in users:
                pass
            else:
                user = User.objects.get(id=1) 
                a = request.user.supervising.all()
                for u in a:
                    print('-----------------------------------------------------------------', u)
                    supervising.append(u)
                # users.append(user)

        print(users)
        
        context = {
            'users': users,
            'supervising': supervising
        }
        return render(request, 'polls/index.html', context)
    else:
        print('Money')


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question_number = Question.objects.all().count()
    try:
        selected_choice = question.choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        Survey.objects.create(question=question, answer=selected_choice.choice_text, user=request.user)
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        if question.id == question_number:
            return redirect('polls:add_remark')
        else:
            return HttpResponseRedirect(reverse('polls:detail', args=(question.id + 1,)))
            

def results(request, id):
    survey = Survey.objects.filter(user=id)
    remarks = Remark.objects.filter(user=id)
    student_name = StudentName.objects.filter(user=id)

    context = {
        'survey': survey,
        'remarks': remarks,
        'student_name': student_name
    }
    
    return render(request, 'polls/results.html', context)



def add_remark(request):
    if request.method == 'POST':
        form = RemarkForm(data=request.POST)
        if form.is_valid():
            new_remark = form.save(commit=False)
            new_remark.user = get_object_or_404(User, id=request.user.id)
            new_remark.save()
            messages.success(request, "Saved successfully")
            return HttpResponseRedirect(reverse('polls:results', args=[request.user.id]))
            # return redirect()
        messages.error(request, 'Something happened')
    else:
        form = RemarkForm()
    context = {
        'form': form
    }
    return render(request, 'polls/add_remark.html', context)



def add_student_name(request):
    question = Question.objects.all().first()
    if request.method == 'POST':
        form = StudentNameForm(data=request.POST)
        if form.is_valid():
            new_name = form.save(commit=False)
            new_name.user = get_object_or_404(User, id=request.user.id)
            new_name.save()
            return HttpResponseRedirect(reverse('polls:detail', args=[question.id]))
    else:
        form = StudentNameForm()
    context = {
        'form': form
    }
    return render(request, 'polls/add_student_name.html', context)


def remarks(request):
    if request.user.type == 'WORK_SUPERVISOR' or request.user.type == 'SUPERVISOR':
        remarks = StudentRemark.objects.all()

        context = {
            'remarks': remarks
        }
        
        return render(request, 'polls/remarks.html', context)
    
    elif request.user.type == 'STUDENT':
        if request.method == 'POST':
            form = StudentRemarkForm(data=request.POST)
            if form.is_valid():
                new_remark = form.save(commit=False)
                new_remark.user = get_object_or_404(User, id=request.user.id)
                new_remark.save()
                messages.success(request, "Saved successfully")
                return HttpResponseRedirect(reverse('assessments:dashboard'))
                # return redirect()
            messages.error(request, 'Something happened')
        else:
            form = StudentRemarkForm()
        context = {
            'form': form
        }
        return render(request, 'polls/remarks.html', context)

