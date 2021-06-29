from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post, Follow


def index(request):
    viewer = User.objects.get(id = request.user.id)
    posts = Post.objects.all()
    paginator = Paginator(posts, 10) # Show 10 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        'page_obj': page_obj,
        "viewer": viewer
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            Follow.objects.create(person_of_interest= user)
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def new_post(request):
    viewer = User.objects.get(id = request.user.id)
    posts = Post.objects.all()
    paginator = Paginator(posts, 10) # Show 10 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == "POST":
        description = request.POST["description"]
        creator = User.objects.get(id = request.user.id)
        post = Post.objects.create(poster=creator, description=description)
        
        return render(request, "network/index.html", {
            'page_obj': page_obj,
            "viewer":viewer
        })
    else: 
        return render(request, "network/index.html", {
            'page_obj': page_obj,
            "viewer":viewer
        })

def profile(request, user_id):
    user = User.objects.get(pk = user_id)
    viewer = User.objects.get(id = request.user.id)
    posts = Post.objects.filter(poster = user)
    paginator = Paginator(posts, 10) # Show 10 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    follow = Follow.objects.get(person_of_interest= user)
    followers = 0
    following = 0
    print(user)
    print(viewer)
    print(follow.followers.all())
    for i in follow.followers.all():
        followers += 1
    for i in follow.following.all():
        following += 1
    if viewer not in follow.followers.all():
        boolean = True
    else:
        boolean = False
    return render(request, "network/profile.html", {
        "user": user,
        "viewer": viewer,
        'page_obj': page_obj,
        "followers": followers,
        "following": following,
        "boolean": boolean
    })

def follow(request, user_id):
    user = User.objects.get(pk = user_id)
    viewer = User.objects.get(id = request.user.id)
    #creating object to add to POI followers
    follow = Follow.objects.get(person_of_interest= user)
    #creating object to add to viewer's following
    follow1 = Follow.objects.get(person_of_interest = viewer)
    if viewer not in follow.followers.all():
        follow.followers.add(viewer)
        follow1.following.add(user)
    else:
        follow.followers.remove(viewer)
        follow1.following.remove(user)
    follow.save()
    follow1.save()
    posts = Post.objects.filter(poster = user)
    paginator = Paginator(posts, 10) # Show 10 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    followers = follow.followers.count()
    following = follow.following.count()

    if viewer not in follow.followers.all():
        boolean = True
    else:
        boolean = False
    print(boolean)
    return render(request, "network/profile.html", {
        "user": user,
        "viewer": viewer,
        'page_obj': page_obj,
        "followers": followers,
        "following": following,
        "boolean": boolean
    })

def following_page(request):
    viewer = User.objects.get(id = request.user.id)
    follow = Follow.objects.get(person_of_interest= viewer)
    list = follow.following.all()
    posts = Post.objects.filter(poster__in = list)
    paginator = Paginator(posts, 10) # Show 10 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following_page.html", {
        'page_obj': page_obj,
        "viewer":viewer
    })

def edit_post(request, post_id):
    post= Post.objects.get(id= post_id)
    viewer = User.objects.get(id = request.user.id)
    if request.method == "POST":
        description = request.POST["new_description"]
        post.description = description
        post.save()
        posts = Post.objects.all()
        paginator = Paginator(posts, 10) # Show 10 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            'page_obj': page_obj,
            "viewer":viewer
        })
    else:
        return render(request, "network/edit_post.html", {
        'post': post
    })
    
def like(request, post_id):
    post = Post.objects.get(id= post_id)
    viewer = User.objects.get(id = request.user.id)
    if viewer in post.liked_post.all():
        post.liked_post.remove(viewer)
        post.likes = post.liked_post.count()
    else:
        post.liked_post.add(viewer)
        post.likes = post.liked_post.count()
    post.save()
    posts = Post.objects.all()
    paginator = Paginator(posts, 10) # Show 10 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        'page_obj': page_obj,
        "viewer":viewer
    })