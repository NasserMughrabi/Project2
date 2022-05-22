from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django import forms
from django.db.models import Max



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


def create_listing_form(request):
    return render(request, "auctions/create_listing.html")


# create a listing and add it to some category and therefore to all listings 
def create_listing(request):
    title = request.POST.get("title")
    description = request.POST.get("description")
    bid = request.POST.get("bid")
    image = request.POST.get("image")
    category = request.POST.get("category")
    listing = Listing(id(Listing), title, description, bid, image, category, request.user.username)
    listing.save()
    
    return render(request, "auctions/listing_details.html", {
        "listing": listing
    })


class newTaskForm(forms.Form):
    listing_item = forms.CharField(label="")

def listing_details(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bids = Bid.objects.filter(listing_id=listing_id)
    comments = Comment.objects.filter(listing_id=listing_id)
    if Bid.objects.filter(listing_id=listing_id).count() > 0:
        highest = Bid.objects.filter(listing_id=listing_id).aggregate(Max('price'))['price__max']
        highest_bidder = Bid.objects.filter(listing_id=listing_id, price=highest).first().username
    else:
        highest = listing.price
        highest_bidder = listing.username


    if listing.username == request.user.username:
        username_is_owner = True
    else :
        username_is_owner = False
    
    return render(request, "auctions/listing_details.html", {
        "listing": listing,
        "owner": username_is_owner,
        "form": newTaskForm(),
        "bids": bids,
        "highest_bidder": highest_bidder,
        "highest_bid": highest,
        "comments": comments
    })


# display user's watchlist of listings
def watchlist(request):
    listings = Watchlist.objects.filter(username = request.user.username)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


def add_to_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    # add listing to the watchlist model/table using correct username
    username = request.user.username
    watchlist = Watchlist(listing_id, username)
    watchlist.save()
    return render(request, "auctions/watchlist.html", {
        "listings": Watchlist.objects.filter(username=username)
    })

def remove_from_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    # add listing to the watchlist model/table using correct username
    username = request.user.username
    if Watchlist.objects.filter(listing=listing_id, username=username).exists():
        Watchlist.objects.filter(listing=listing_id, username=username).delete()
        return render(request, "auctions/watchlist.html", {
            "listings": Watchlist.objects.filter(username=username)
        })
    else:
        return render(request, "auctions/watchlist.html", {
            "listings": Watchlist.objects.filter(username=username)
        })

# def bid(request):
#     if request.method == "post":
#         bid = request.POST.get("bid")
#     return render(request, "auctions/listing_details.html", {
#         "listing": bid,
#     })

def add_comment(request, listing_id):
    if request.method == "POST":
        comment_input = request.POST["comment"]
    
    comment = Comment(id(Comment), listing_id, comment_input)
    comment.save()

    listing = Listing.objects.get(pk=listing_id)
    bids = Bid.objects.filter(listing_id=listing_id)
    comments = Comment.objects.filter(listing_id=listing_id)

    if Bid.objects.filter(listing_id=listing_id).count() > 0:
        highest = Bid.objects.filter(listing_id=listing_id).aggregate(Max('price'))['price__max']
        highest_bidder = Bid.objects.filter(listing_id=listing_id, price=highest).first().username
    else:
        highest = listing.price
        highest_bidder = listing.username
    
    return render(request, "auctions/listing_details.html", {
        "listing": listing,
        "bids": bids,
        "highest_bid": highest,
        "highest_bidder": highest_bidder,
        "comments": comments
    })

def add_bid(request, listing_id):
    if request.method == "POST":
        bid_input = request.POST["bid"]

    listing = Listing.objects.get(pk=listing_id)
    if Bid.objects.filter(listing_id=listing_id).count() > 0:
        highest = Bid.objects.filter(listing_id=listing_id).aggregate(Max('price'))['price__max']
    else:
        highest = listing.price

    if int(bid_input) < listing.price or int(bid_input) < highest:
        return HttpResponse("Invalid input. Your bid must be higher than both the Starting bid and the Highest bid!")
    
    bid = Bid(id(Bid), listing_id, bid_input, request.user.username)
    bid.save()

    if Bid.objects.filter(listing_id=listing_id).count() > 0:
        highest = Bid.objects.filter(listing_id=listing_id).aggregate(Max('price'))['price__max']
        highest_bidder = Bid.objects.filter(listing_id=listing_id, price=highest).first().username
    else:
        highest = listing.price
        highest_bidder = listing.username

    bids = Bid.objects.filter(listing_id=listing_id)
    comments = Comment.objects.filter(listing_id=listing_id)
    
    return render(request, "auctions/listing_details.html", {
        "listing": listing,
        "bids": bids,
        "highest_bid": highest,
        "highest_bidder": highest_bidder,
        "comments": comments
    })

def close_auction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    Listing.objects.filter(listing_id=listing_id).update(closed=True)
    bids = Bid.objects.filter(listing_id=listing_id)
    comments = Comment.objects.filter(listing_id=listing_id)

    if Bid.objects.filter(listing_id=listing_id).count() > 0:
        highest = Bid.objects.filter(listing_id=listing_id).aggregate(Max('price'))['price__max']
        highest_bidder = Bid.objects.filter(listing_id=listing_id, price=highest).first().username
    else:
        highest = listing.price
        highest_bidder = listing.username
    
    return render(request, "auctions/listing_details.html", {
        "listing": listing,
        "form": newTaskForm(),
        "bids": bids,
        "highest_bidder": highest_bidder,
        "highest_bid": highest,
        "comments": comments
    })