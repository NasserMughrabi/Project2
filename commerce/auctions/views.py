from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *


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


# display all listing from all users to the current session
def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })

# display a list of categories from categoreis table/model as links
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Categorie.objects.all()
        })

def category_listings(request, category_name):
    return render(request, "auctions/category_listings.html", {
        "category_name": category_name,
        "category_listings": Listing.objects.filter(category=category_name)
    })

# display user's watchlist of listings
def watchlist(request):
    return render(request, "auctions/watchlist.html")

def create_listing_form(request):
    return render(request, "auctions/create_listing.html")


# create a listing and add it to some category and therefore to all listings 
def create_listing(request):
    title = request.POST.get("title")
    description = request.POST.get("description")
    bid = request.POST.get("bid")
    image = request.POST.get("image")
    category = request.POST.get("category")
    listing = Listing(id(Listing), title, description, bid, image, category)
    listing.save()
    
    return render(request, "auctions/listing_details.html", {
        "listing": listing
    })

def listing_details(request, listing):
    return render(request, "auctions/listing_details.html", {
        "listing": listing
    })
