from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# Categories table
class Categorie(models.Model):
    # columns
    category = models.CharField(primary_key=True, max_length=64)

# Listings table
class Listing(models.Model):
    # columns
    listing_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    price = models.IntegerField()
    image_URL = models.URLField(blank=True)
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="listing")

# class watchlist(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist", primary_key=True)
#     listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist(s)", primary_key=True)

# Bids table
class Bid(models.Model):
    # columns
    bid_id = models.AutoField(primary_key=True)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    price = models.IntegerField()

# Comments table
class Comment(models.Model):
    # columns
    comment_id = models.AutoField(primary_key=True)
    listing_id  = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=250)


