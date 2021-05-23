from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User
# Create your views here.

@login_required
def welcome(request):
    return render(request, "welcome.html")

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            usrnm = request.POST.get("uname")
            passwd = request.POST.get("pswd")
            user_obj = authenticate(username=usrnm, password=passwd)
            if user_obj:
                login(request, user_obj)
                return redirect('welcome')
            else:
                return HttpResponse("Invalid Credentials. Please try Again...")
        return render(request, 'login.html')
    else:
        return redirect('welcome')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

class UserSignupForm(UserCreationForm):

    password2 = forms.CharField(
        label="Re-Enter Password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

def signup(request):
    if request.method == "POST":
        form =  UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile is Successfully Created.. Please Login')
            return redirect('login')
        else:
            return render(request, 'signup.html', {'form': form})
    form = UserSignupForm()
    return render(request, "signup.html", {"form": form})


@login_required
def change_password(request):
    if request.method=="POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user= form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your Password has been Updated!!!")
            return redirect('cpassold')
        else:
            return render(request, 'change_password.html', {'form': form})

    change_form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': change_form})


@login_required
def changepassword(request):
    if request.method=="POST":
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user= form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your Password has been Updated!!!")
            return redirect('cpass')
        else:
            return render(request, 'changepassword.html', {'form': form})

    changeform = SetPasswordForm(request.user)
    return render(request, 'changepassword.html', {'form': changeform})
