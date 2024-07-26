from django.shortcuts import render,redirect, get_object_or_404
from .models import*
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Create your views here.

@login_required(login_url = "/login/")

def tweets(request):
    
    if request.method == "POST":

        data = request.POST
        name = request.user.username
        tweet_image = request.FILES.get('tweet_image')
        content = data.get('content')
        
        Tweet.objects.create(
            tweet_image =tweet_image,
            name = name ,
            content = content,
            user = request.user
            )


        return redirect('/tweets/')
    
    queryset = Tweet.objects.all()

    search_query = request.GET.get('search', '')

    if search_query:
        queryset= queryset.filter(name_icontains = search_query)

    context = {'tweets': queryset , 'username' : request.user.username,
               'search_query' : search_query}

    
    return render(request , 'tweets.html' , context)

@login_required(login_url = "/login/")
def update_tweet(request,id):
    
    queryset = Tweet.objects.get(id=id)


    if request.method == "POST":

        data = request.POST
        tweet_image = request.FILES.get('tweet_image')
        # name = data.get('name')
        content = data.get('content')
        # queryset.name = name
        queryset.content = content

        if tweet_image:
            queryset.tweet_image = tweet_image

        queryset.save()
        return redirect('/tweets/')

    context = {'tweet' :queryset}

    return render(request , 'update_tweet.html' , context)

@login_required(login_url = "/login/")
def delete_tweet(request , id):
    queryset = Tweet.objects.get(id=id)

    queryset.delete()
    return redirect('/tweets/')


def login_page(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request , 'Invalid Username' )
            return redirect('/login/')
    
        user = authenticate(username = username ,password= password)

        if user is None:
            messages.error(request , 'Invalid Password' )
            return redirect('/login/')
    
        else:
            login(request , user)
            return redirect('/tweets/')



    return render(request , 'login.html')


def logout_page(request):
    logout(request)
    return redirect('/login/')


def register(request):

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        my_email = request.POST.get('my_email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(request, 'Username already taken')
            return redirect('/register/')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            
        )

        user.set_password(password)
        user.save()

        messages.info(request , 'Account created successfuly' )

        return redirect('/register/')

    return render(request , 'register.html')