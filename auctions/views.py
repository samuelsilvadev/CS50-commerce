from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import  HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Auction, User, Category



def index(request):
    return render(request, "auctions/index.html")


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def new_listing(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image_url = request.POST.get('image_url')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        minimum_bid_value = request.POST.get('minimum_bid_value')
        category_ids = request.POST.getlist('category')

        auction = Auction(
            title=title,
            description=description,
            image_url=image_url,
            start_date=start_date,
            end_date=end_date,
            minimum_bid_value=minimum_bid_value,
            owner=request.user,
        )

        auction.save()

        categories = Category.objects.filter(id__in=category_ids)
        auction.category.set(categories)

        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/new.html", {
        "catogories": Category.objects.all()
    })
