from code import interact
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField, IntegerField


class User(AbstractUser):
    pass

# Listings table
class Listing(models.Model):
    # columns
    listing_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    price = models.IntegerField()
    image_URL = models.URLField(blank=True)

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
