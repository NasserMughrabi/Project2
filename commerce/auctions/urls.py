from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("<str:category_name>/category_listings", views.category_listings, name="category_listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("<int:listing_id>/remove_from_watchlist", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("<int:listing_id>/add_comment", views.add_comment, name="add_comment"),
    path("<int:listing_id>/add_bid", views.add_bid, name="add_bid"),
    path("<int:listing_id>/close_auction", views.close_auction, name="close_auction"),
    path("create_listing_form", views.create_listing_form, name="create_listing_form"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<int:listing_id>/listing_details", views.listing_details, name="listing_details")
]
