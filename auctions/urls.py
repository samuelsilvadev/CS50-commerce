from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/new", views.new_listing, name="new_listing"),
    path("listing/details/<int:id>", views.listing_entry, name="listing_entry")
]
