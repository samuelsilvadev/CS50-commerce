from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/new", views.new_listing, name="new_listing"),
    path("listing/details/<int:id>", views.listing_entry, name="listing_entry"),
    path("listing/details/bid/<int:id>", views.place_bid, name="place_bid"),
    path(
        "listing/details/close-auction/<int:id>",
        views.close_auction,
        name="close_auction",
    ),
    path("404", views.not_found, name="not_found"),
    path("watchlist", views.watchlist, name="watchlist"),
    path(
        "toggle_watchlist/<int:auction_id>",
        views.toggle_watchlist,
        name="toggle_watchlist",
    ),
]
