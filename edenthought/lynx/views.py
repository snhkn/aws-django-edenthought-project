from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm
from . models import Profile

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):

    return render(request, 'lynx/index.html')

def register(request):

    form  = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            current_user = form.save(commit=False)
            form.save()
            profile = Profile.objects.create(user=current_user)
            return redirect("my-login")

    context = {'form': form}
    return render(request, 'lynx/register.html', context=context)

def my_login(request):

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")

    context = {'form': form}
    return render(request, 'lynx/my-login.html', context=context)

def user_logout(request):

    auth.logout(request)
    return redirect("")

@login_required(login_url='my-login')
def dashboard(request):

    return render(request, 'lynx/dashboard.html')

@login_required(login_url='my-login')
def profile_management(request):

    return render(request, 'lynx/profile-management.html')