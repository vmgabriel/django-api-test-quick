"""
Model Data of Bills
"""

# Libraries
from django.db import models
from django.contrib.auth.models import AbstractUser

SCORES = (
        ('G', 'Good'),
        ('R', 'Regular'),
        ('B', 'Bad'),
    )


class Client(AbstractUser):
    """Client Class Model"""
    identification = models.CharField(max_length=30, unique=True, null=False)
    email = models.EmailField(unique=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        """Meta Class for Define Observations Client of Model"""
        db_table = 'client'
        ordering = ['identification']


class Product(models.Model):
    """Product Class Model"""
    name = models.CharField(max_length=70, null=False)
    description = models.CharField(max_length=150, null=True)
    prize_one = models.IntegerField()
    quantity = models.IntegerField()
    provider_name = models.CharField(max_length=80, null=True)
    score = models.CharField(max_length=1, choices=SCORES)

    class Meta:
        """Meta Class for Define Observations product of Model"""
        db_table = 'product'
        ordering = ['name']


class Bill(models.Model):
    """Bill Class Model"""
    company_name = models.CharField(max_length=100, null=False)
    nit = models.CharField(max_length=40, null=False)
    code = models.CharField(max_length=40, null=False)
    client_id = models.ForeignKey(
        Client,
        db_column='client_id',
        on_delete=models.CASCADE
    )
    products = models.ManyToManyField(Product, null=True, blank=True),

    class Meta:
        """Meta Class for Define Observations Bill of Model"""
        db_table = 'bill'
        ordering = ['code']


class File(models.Model):
    """File Class Definition"""
    title = models.CharField(max_length=100, null=False)
    file_data = models.FileField(blank=True, null=True)
    description = models.CharField(max_length=255)

    class Meta:
        """Meta Definition"""
        db_table = 'file'
        ordering = ['title']

    def __str__(self):
        """To Str"""
        return self.title
