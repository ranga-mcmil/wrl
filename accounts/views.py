from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm
from .forms import LoginForm
from .models import StudentProfile
from PIL import Image
from django.contrib import messages





def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.type = form.cleaned_data['type']
            new_user.save()
            if new_user.type == 'STUDENT':
                StudentProfile.objects.create(user=new_user)
            login(request, new_user)
            messages.success(request, "Account created successfully")
            return redirect('assessments:dashboard')

    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated ' \
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})