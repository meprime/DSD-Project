from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from PopCorn.forms import *
from User.models import UserProfile


def register(request):
    if request.method == 'POST':
        print("method is post.")
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User()
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password'])
            user.email = form.cleaned_data['email']
            user.save()
            userprofile = UserProfile()
            userprofile.user = user
            userprofile.birthday = form.cleaned_data['birthday']
            userprofile.alias = form.cleaned_data['alias']
            userprofile.save()
            print("New user created.")
            return HttpResponseRedirect('/login/')
    else:
        form = RegistrationForm
    return render(request, "sign_up.html", {
        'form': form
        })
"""
def register(request):
    # form = Users(request.POST)
    if request.method == 'POST':
        print("method is post.")
        user_form = UserRegisterForm(request.POST, prefix="user_form")
        userprofile_form = UserProfileRegisterForm(request.POST, prefix="userProfile_form")
        if user_form.is_valid() and userprofile_form.is_valid():
            user = user_form.save()
            userprofile = userprofile_form.save(commit=False)
            userprofile.user = user
            userprofile.save()
            print("New user created.")
            return HttpResponseRedirect('/login/')
    else:
        user_form = UserRegisterForm(prefix="user_form")
        userprofile_form = UserProfileRegisterForm(prefix="userProfile_form")
    return render(request, "sign_up.html", {
        # 'form': form
        'user_form': user_form,
        'userprofile_form': userprofile_form
        })
"""


def sign_in(request):
    # form = Users(request.POST)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            print("say hi   ")
            login(request, user)
            return HttpResponseRedirect("/timeline/")
        else:
            login_form = LoginForm(request.POST)

    else:
        login_form = LoginForm

    return render(request, "sign_in.html", {
        'login_form': login_form
        })


def sign_out(request):
    logout(request)
    return HttpResponseRedirect("/login/")


def forgot_password(request):
    # form = Users(request.POST)
    msg = ''
    if request.method == 'POST':
        email = request.POST['email']
        users = User.objects.filter(email=email)
        if users:
            print("say hi")
            user = users[0]     #assuming email is unique
            pw = User.objects.make_random_password()
            user.set_password(pw)
            user.save()
            send_mail('PopCorn password reset', pw, 'password_reset@popcorn.com', [email])
            msg = 'We have sent you a password-reset email.'
        else:
            print("say bye")
            msg = 'Your email is not valid.'

    form = ForgotPasswordForm

    return render(request, "forgot_password.html", {
        'form': form,
        'operation_message': msg
        })


@login_required(login_url='/login/')
def profile(request, user_id):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    profiling_user = User.objects.filter(id=user_id)[0]
    profiling_user_profile = UserProfile.objects.get(user=profiling_user)
    if profiling_user:
        if profiling_user.username == user.username:
            if request.method == 'POST':
                pass
            else:
                update_form = ProfileUpdateForm

            return render(request, "profile_user.html", {

            })
        else:
            if user_profile.follows.filter(id=user_id):
                button = 'unfollow'
            else:
                button = 'follow'
            followees = profiling_user_profile.follows.count()
            #followers = UserProfile.objects.
            followers = 0
            return render(request, "profile.html", {
                'follow_button': button,
                'followers': followers,
                'followees': followees,
                'profiling_user_profile': profiling_user_profile
            })
    else:
        pass


def related_user(request):
    # form = Users(request.POST)
    return render(request, "related_users.html", {
        # 'form': form
        })


def search(request):
    # form = Users(request.POST)
    return render(request, "search_results.html", {
        # 'form': form
        })


