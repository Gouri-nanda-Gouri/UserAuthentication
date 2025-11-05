from django.db import models
import pyotp

class User(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(unique=True)
    user_password = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=50, blank=True, null=True)   # Add this
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tbl_user"   # This sets the table name in SQLite


class Seller(models.Model):
    seller_name = models.CharField(max_length=100)
    seller_email = models.EmailField(unique=True)
    seller_password = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=50, blank=True, null=True)   # Add this
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tbl_seller"
