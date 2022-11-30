from django.shortcuts import render, HttpResponseRedirect
from Login_System.forms import CreateNewUser, EditProfile
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from Login_System.models import UserProfile, Follow
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from Post_System.forms import PostForm
from django.contrib import messages

from django.contrib.auth.models import User


# Create your views here.

def signup(request):
    form = CreateNewUser()
    registered = False
    if request.method == 'POST':
        form = CreateNewUser(data=request.POST)
        if form.is_valid():
            user = form.save()
            registered = True
            user_profile = UserProfile(user=user)
            user_profile.save()
            messages.success(request, "Account Created Successfully!")
            return HttpResponseRedirect(reverse('Login_System:login'))
    return render(request, 'Login_System/signup.html', context={'title':'Sign up . Social', 'form':form})

# def signup(request):
#     form = CreateNewUser()
#     registered = False
#     if request.method == 'POST':
#         form = CreateNewUser(data=request.POST)
#         if form.is_valid():
#             user = form.save()
#             registered = True
#             # user_profile = UserProfile(user=user)
#             # user_profile.save()
#             # return HttpResponseRedirect(reverse('Login_System:login'))
#             pass
#     return render(request, 'signup.html', context={'title':'Sign up . Social', 'form':form})

def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('Post_System:home'))

    return render(request, 'Login_System/login.html', context={'title':'Login . Social','form':form})

@login_required
def edit_profile(request):
    current_user = UserProfile.objects.get(user=request.user)
    form = EditProfile(instance=current_user)
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            form = EditProfile(instance=current_user)
            return HttpResponseRedirect(reverse('Login_System:profile'))
    return render(request, 'Login_System/profile.html', context={'form':form, 'title':'Edit Profile . Social'})

@login_required
def logout_user(request):
    logout(request)
    messages.warning(request, "You are logged out!!")
    return HttpResponseRedirect(reverse('Login_System:login'))


@login_required
def profile(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'Login_System/user.html', context={'title':'User', 'form': form})

@login_required
def user(request, username):
    user_other = User.objects.get(username=username)
    already_followed = Follow.objects.filter(follower=request.user, following=user_other)
    if user_other == request.user:
        return HttpResponseRedirect(reverse('Login_System:profile'))
    return render(request, 'Login_System/user_other.html', context={'user_other':user_other, 'already_followed':already_followed})

@login_required
def follow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user, following=following_user)
    if not already_followed:
        followed_user = Follow(follower=follower_user, following=following_user)
        followed_user.save()
    return HttpResponseRedirect(reverse('Login_System:user', kwargs={'username':username}))

@login_required
def unfollow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user, following=following_user)
    already_followed.delete()
    return HttpResponseRedirect(reverse('Login_System:user', kwargs={'username':username}))
