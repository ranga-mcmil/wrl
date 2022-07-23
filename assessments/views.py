from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Log, Message
from .forms import LogForm, CommentForm, AddStudentForm, AddWRLSupervisorForm, UpdateProgForm
from accounts.models import User, Contact, StudentProfile
from django.http import JsonResponse
import json
from django.core import serializers
from actions.utils import create_action
from django.contrib import messages
from actions.models import Action
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
@login_required
def dashboard(request):
    if request.user.type == 'STUDENT':
        documents = Log.objects.filter(author=request.user)

        context = {
            'documents': documents
        }

        return render(request, 'assessments/student/dashboard.html', context)
    elif request.user.type == 'SUPERVISOR':
        documents = Log.objects.filter(approved_for_academic=True)
        students = request.user.supervising.all()

        context = {
            'documents': documents,
            'students': students
        }

        return render(request, 'assessments/supervisor/dashboard.html', context)
    elif request.user.type == 'WORK_SUPERVISOR':
        documents = Log.objects.all()
        students = request.user.supervising.all()

        context = {
            'documents': documents,
            'students': students
        }

        return render(request, 'assessments/work_supervisor/dashboard.html', context)
    else:
        documents = Log.objects.filter(author=request.user)
        students = request.user.supervising.all()

        context = {
            'documents': documents,
            'students': students
        }

        return render(request, 'assessments/work_supervisor/dashboard.html', context)

@login_required
def update_prog(request):
    if request.method == 'POST':
        form = UpdateProgForm(request.POST)

        if form.is_valid():
            profile = StudentProfile.objects.get(user=request.user)
            profile.programme = form.get_info()
            profile.save()
            messages.success(request, "Programme updated")
            return redirect('assessments:dashboard')
    else:
        form = UpdateProgForm()

    context = {
        'form': form
    }

    return render(request, 'assessments/student/update_prog.html', context)


@login_required
def new(request):
    if request.method == 'POST':
        form = LogForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_log = form.save(commit=False)
            new_log.author = get_object_or_404(User, id=request.user.id)
            new_log.save()
            create_action(request.user, 'uploaded a', new_log)
            messages.success(request, "Uploaded successfully")
            return redirect('assessments:dashboard')
        messages.error(request, 'File type not valid')
    else:
        form = LogForm()
    context = {
        'form': form
    }

    return render(request, 'assessments/student/new_log.html', context)


@login_required
def detail(request, id):

    log = Log.objects.get(id=id)
    userr = log.author
    comments = log.comments.all()
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.log = log
            new_comment.author = get_object_or_404(User, id=request.user.id)
            new_comment.save()
            messages.success(request, "Comment sent")
            create_action(request.user, 'commented on your submission', new_comment)
            return redirect(request.META['HTTP_REFERER'])
        messages.error(request, 'Error while sending comment')
    else:
        form = CommentForm()
    context = {
        'form': form,
        'comments': comments,
        'log': log,
        'userr': userr
    }

    return render(request, 'assessments/student/detail.html', context)



@login_required
def notifications(request):
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    verb = 'uploaded a'
    if request.user.type == 'SUPERVISOR':
        supervising_ids = request.user.supervising.values_list('id',
                                                           flat=True)
        if supervising_ids:
            # If user is following others, retrieve only their actions
            actions = actions.filter(user_id__in=supervising_ids)
            print('---------------------------', actions)
    elif request.user.type == 'WORK_SUPERVISOR':
        supervising_ids = request.user.supervising.values_list('id',
                                                           flat=True)
        if supervising_ids:
            # If user is following others, retrieve only their actions
            actions = actions.filter(user_id__in=supervising_ids)
            print('---------------------------', actions)
    else:
        supervising_ids = request.user.supervised_by.values_list('id',
                                                               flat=True)
        if supervising_ids:
            # If user is following others, retrieve only their actions
            actions = actions.filter(user_id__in=supervising_ids)
            print('---------------------------', actions)

    context = {
        'actions': actions,
        'verb': verb
    }

    if request.user.type == 'STUDENT':
        return render(request, 'assessments/student/notifications.html', context)
    elif request.user.type == 'WORK_SUPERVISOR':
        return render(request, 'assessments/work_supervisor/notifications.html', context)
    else:
        return render(request, 'assessments/supervisor/notifications.html', context)



@login_required
def add_student(request):
    if request.method == 'POST':
        form = AddStudentForm(request.POST)

        if form.is_valid():
            user_to_add = User.objects.get(username=form.get_info())
            user = request.user.supervising.all()
            if user_to_add in user:
                messages.info(request, "You are already supervising this student")
                return redirect('assessments:dashboard')

            else:
                new_contact = Contact.objects.create(user_from=request.user, user_to=User.objects.get(username=form.get_info()))
                new_contact.save()
                messages.success(request, "Student added")
                return redirect('assessments:dashboard')
    else:
        form = AddStudentForm()

    context = {
        'form': form
    }

    return render(request, 'assessments/supervisor/add_student.html', context)


@login_required
def add_wrl_supervisor(request):
    if request.method == 'POST':
        form = AddWRLSupervisorForm(request.POST)

        if form.is_valid():
            user_to_add = User.objects.get(username=form.get_info())
            user = request.user.supervised_by.all()
            supervisor = request.user.supervised_by.first()
            if user_to_add in user:
                messages.info(request, "You are already added this supervisor")
                return redirect('assessments:dashboard')

            else:
                new_contact = Contact.objects.create(user_from=User.objects.get(username=form.get_info()),
                                                     user_to=request.user)
                new_contact2 = Contact.objects.create(user_from=supervisor,
                                                     user_to=user_to_add)
                new_contact3 = Contact.objects.create(user_from=user_to_add,
                                                      user_to=supervisor)
                new_contact.save()
                new_contact2.save()
                new_contact3.save()
                messages.success(request, "Work Supervisor added")
                return redirect('assessments:dashboard')
    else:
        form = AddWRLSupervisorForm()

    context = {
        'form': form
    }

    return render(request, 'assessments/student/add_wrl_supervisor.html', context)




@login_required
def student_detail(request, id):
    student = User.objects.get(id=id)
    logs = Log.objects.filter(author=student)
    supervisors = student.supervised_by.all()

    context = {
        'logs': logs,
        'supervisors': supervisors,
        'student': student
    }


    return render(request, 'assessments/student/student_detail.html', context)



@login_required
def get_messages(request):
    data = json.loads(request.body)
    user_id = data['user_id']


    if user_id:
        try:
            user = User.objects.get(id=user_id)
            messages = []
            messages_from = eval(serializers.serialize("json", Message.objects.filter(message_from=user, message_to=request.user),
                                                  fields=("body", "created", "message_from", "message_to")))
            messages_to = eval(serializers.serialize("json", Message.objects.filter(message_to=user, message_from=request.user),
                                                fields=("body", "created", "message_from", "message_to")))

            for message in messages_from:
                messages.append(message['fields'])
            for message in messages_to:
                messages.append(message['fields'])

            sortedMessages = sorted(messages, key=lambda d: d['created'])
            print(sortedMessages)
            data = [{'name': user.get_full_name()}, sortedMessages, {'id': user.id}]

            return JsonResponse(data, safe=False)

        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'error'})



@login_required
def send_message(request):
    data = json.loads(request.body)
    print(data)
    message_from = data['message_from']
    message_to = data['message_to']
    body = data['message']


    if body:
        try:
            user = User.objects.get(id=message_to)
            user_from = User.objects.get(id=message_from)
            user_to = User.objects.get(id=message_to)
            Message.objects.create(message_from=user_from, message_to=user_to, body=body)
            messages = []
            messages_from = eval(serializers.serialize("json", Message.objects.filter(message_from=user, message_to=request.user),
                                                  fields=("body", "created", "message_from", "message_to")))
            messages_to = eval(serializers.serialize("json", Message.objects.filter(message_to=user, message_from=request.user),
                                                fields=("body", "created", "message_from", "message_to")))

            for message in messages_from:
                messages.append(message['fields'])
            for message in messages_to:
                messages.append(message['fields'])

            print(messages)
            sortedMessages = sorted(messages, key=lambda d: d['created'])
            print(sortedMessages)
            data = [{'name': user.get_full_name()}, sortedMessages]

            return JsonResponse(data, safe=False)

        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'error'})



@login_required
def approve(request, id):
    # questionnare = Questionnaire.objects.get(id=id)
    log = Log.objects.get(id=id)
    log.approved_for_academic = True
    log.save()
    # create_action(request.user, 'posted a ', log)
    messages.success(request, "Document Approved")
    return redirect('assessments:dashboard')
    

