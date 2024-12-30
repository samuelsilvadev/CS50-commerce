from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import Auction, User, Category, Bid


def index(request):
    auctions = Auction.objects.filter(is_active=True)

    return render(request, "auctions/index.html", {"auctions": auctions})


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {
                    "message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def new_listing(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        image_url = request.POST.get("image_url")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        minimum_bid_value = request.POST.get("minimum_bid_value")
        category_ids = request.POST.getlist("category")
        is_active = request.POST.get("is_active") == "on"

        auction = Auction(
            title=title,
            description=description,
            image_url=image_url,
            start_date=start_date,
            end_date=end_date,
            minimum_bid_value=minimum_bid_value,
            owner=request.user,
            is_active=is_active,
        )

        auction.save()

        categories = Category.objects.filter(id__in=category_ids)
        auction.category.set(categories)

        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/new.html", {"categories": Category.objects.all()})


def listing_entry(request, id):
    auction = Auction.objects.filter(id=id).first()

    if auction is None:
        return HttpResponseRedirect(reverse("not_found"))

    highest_bid = Bid.get_highest_bid(auction=auction)

    return render(request, "auctions/details.html", {"auction": auction, "highest_bid": highest_bid})


def place_bid(request, id):
    auction = Auction.objects.filter(id=id).first()

    if auction is None:
        return HttpResponseRedirect(reverse("not_found"))

    if request.method == "POST":
        target_bid_value = request.POST.get("bid")

        bid = Bid(
            auction=auction,
            user=request.user,
            value=target_bid_value,
            date=timezone.now(),
            is_active=True
        )

        bid.save()

        return HttpResponseRedirect(reverse("listing_entry", args=[id]))

    highest_bid = Bid.get_highest_bid(auction=auction)

    return render(request, "auctions/details.html", {"auction": auction, "highest_bid": highest_bid})


def not_found(request):
    return render(request, "auctions/404.html")
