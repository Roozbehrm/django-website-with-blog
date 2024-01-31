from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import LoginForm, RegisterForm

# Create your views here.

def login_view(request):
    if not request.user.is_authenticated:
        form = LoginForm()
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username= username, password= password)
                if user is not None:
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, 'logged in successfully')
                    return redirect('/')
            messages.add_message(request, messages.ERROR, 'Something went wrong')
        return render(request, 'accounts/login.html', {'form': form})
    else:
        return redirect('/')

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

def signup_view(request):
    if not request.user.is_authenticated:
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Signed up successfully')
                return redirect('/accounts/login')
            messages.add_message(request, messages.ERROR, 'Something went wrong')
        return render(request, 'accounts/signup.html', {'form' : form})
    else:
        return redirect('/')