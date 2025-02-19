from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, resolve
from django.utils import timezone
from decimal import Decimal

from .models import Auction, User, Category, Bid, Watchlist, Comment


def index(request):
    category_id = request.GET.get("category")

    category = (
        Category.objects.filter(pk=category_id).first()
        if category_id is not None
        else None
    )

    if category is not None:
        auctions = Auction.objects.filter(is_active=True, category=category)
    else:
        auctions = Auction.objects.filter(is_active=True)

    return render(
        request, "auctions/index.html", {"auctions": auctions, "category": category}
    )


@login_required
def auctions_won(request):
    user = request.user
    auctions = Auction.objects.filter(winner=user)

    return render(request, "auctions/index.html", {"auctions": auctions})


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        next = request.POST.get("next")
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)

            if next is None:
                return HttpResponseRedirect(reverse("index"))

            try:
                resolve(next)
                return HttpResponseRedirect(next)
            except:
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
                request, "auctions/register.html", {"message": "Passwords must match."}
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


@login_required
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
    is_watched = (
        Watchlist.is_watched(auction=auction, user=request.user)
        if request.user is not None and request.user.is_authenticated
        else False
    )
    is_owner = auction.owner.pk == request.user.pk
    is_winner = (
        auction.winner.pk == request.user.pk if auction.winner is not None else False
    )
    comments = Comment.objects.filter(auction=auction, is_removed=False).order_by(
        "-date"
    )

    return render(
        request,
        "auctions/details.html",
        {
            "auction": auction,
            "highest_bid": highest_bid,
            "is_watched": is_watched,
            "is_owner": is_owner,
            "is_winner": is_winner,
            "comments": comments,
        },
    )


@login_required
def place_bid(request, id):
    auction = Auction.objects.filter(id=id).first()

    if auction is None:
        return HttpResponseRedirect(reverse("not_found"))

    highest_bid = Bid.get_highest_bid(auction=auction)
    is_owner = auction.owner.pk == request.user.pk

    if request.method == "POST":
        target_bid_value = Decimal(request.POST.get("bid"))

        if highest_bid is not None and target_bid_value <= highest_bid.value:
            return render(
                request,
                "auctions/details.html",
                {
                    "auction": auction,
                    "highest_bid": highest_bid,
                    "is_owner": is_owner,
                    "place_bid_error": f"Your offer must be bigger than the latest bid: {highest_bid.value}",
                },
            )

        if highest_bid is None and target_bid_value <= auction.minimum_bid_value:
            return render(
                request,
                "auctions/details.html",
                {
                    "auction": auction,
                    "highest_bid": highest_bid,
                    "is_owner": is_owner,
                    "place_bid_error": f"Your offer must be bigger than the minimum bid value: {auction.minimum_bid_value}",
                },
            )

        bid = Bid(
            auction=auction,
            user=request.user,
            value=target_bid_value,
            date=timezone.now(),
            is_active=True,
        )

        bid.save()

        return HttpResponseRedirect(reverse("listing_entry", args=[id]))

    return render(
        request,
        "auctions/details.html",
        {"auction": auction, "highest_bid": highest_bid},
    )


def not_found(request):
    return render(request, "auctions/404.html")


@login_required
def watchlist(request):
    watchlist_entries = Watchlist.objects.filter(user=request.user)

    return render(request, "auctions/watchlist.html", {"entries": watchlist_entries})


@login_required
def toggle_watchlist(request, auction_id):
    if request.method == "POST":
        auction = Auction.objects.filter(id=auction_id).first()

        if auction is None:
            return HttpResponseRedirect(reverse("not_found"))

        watched_entry = Watchlist.objects.filter(
            user=request.user, auction=auction
        ).first()

        if watched_entry is not None:
            watched_entry.delete()
        else:
            watchlist_entry = Watchlist(
                user=request.user, auction=auction, date=timezone.now()
            )
            watchlist_entry.save()

        return HttpResponseRedirect(reverse("listing_entry", args=[auction_id]))

    return HttpResponseRedirect(reverse("not_found"))


@login_required
def close_auction(request, id):
    if request.method == "POST":
        auction = Auction.objects.filter(id=id).first()

        if auction is None:
            return HttpResponseRedirect(reverse("not_found"))

        highest_bid = Bid.get_highest_bid(auction=auction)

        if highest_bid is not None:
            auction.winner = highest_bid.user

        auction.is_active = False
        auction.save()

        return HttpResponseRedirect(reverse("listing_entry", args=[id]))


@login_required
def comment(request, id):
    if request.method == "POST":
        auction = Auction.objects.filter(id=id).first()

        if auction is None:
            return HttpResponseRedirect(reverse("not_found"))

        text = request.POST.get("comment")

        comment = Comment(
            comment=text, user=request.user, auction=auction, date=timezone.now()
        )

        comment.save()

    return HttpResponseRedirect(reverse("listing_entry", args=[id]))


def categories(request):
    categories = Category.objects.all()

    return render(request, "auctions/categories.html", {"categories": categories})
