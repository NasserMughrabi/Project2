from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing_form", views.create_listing_form, name="create_listing_form"),
    path("categories", views.categories, name="categories"),
    path("<str:category_name>/category_listings", views.category_listings, name="category_listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<str:value>/listing_details", views.listing_details, name="listing_details")
]
