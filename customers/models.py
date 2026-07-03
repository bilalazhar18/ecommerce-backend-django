from django.db import models
# Create your models here.
class Customer(models.Model):
    MEMBER_SHIP_BRONZE = 'B'
    MEMBER_SHIP_SILVER = 'S'
    MEMBER_SHIP_GOLD = 'G'
    MEMBER_SHIP_CHOICES = [
        (MEMBER_SHIP_BRONZE, 'Bronze'),
        (MEMBER_SHIP_SILVER, 'Silver'),
        (MEMBER_SHIP_GOLD, 'Gold')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email   = models.EmailField(unique=True)
    phone   = models.CharField(max_length=20)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBER_SHIP_CHOICES, default=MEMBER_SHIP_BRONZE)
    


class Address(models.Model):
    street = models.CharField(max_length=255)
    city   = models.CharField(max_length=255)
    #presenting one to one relationship with customer
    #customer = models.OneToOneField(Customer, on_delete=models.CASCADE,primary_key=True)
    #presenting one to many relationship with customer
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
