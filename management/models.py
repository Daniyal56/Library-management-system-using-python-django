from django.db import models

# Create your models here.

class Book(models.Model):
    """
    Book class - to describe book in the system.
    """
    serial = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    cost = models.IntegerField()
    procurement = models.DateField(null=True, blank=True)

    def __str__(self):
        return ('Book: ' + self.name)  #object description in string

class Movies(models.Model):
    """
    Movies class - to describe movie in the system.
    """
    serial = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    cost = models.IntegerField()
    procurement = models.DateField(null=True, blank=True)

    def __str__(self):
        return ('Movie: ' + self.name+ '('+self.author +')')



class Memberships(models.Model):
    """
    Membershipsclass - to describe Memberships in the ERP.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    aadhar = models.CharField(max_length=200)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=200)
    fine = models.IntegerField()
    if_having_book = models.CharField(max_length=200)
    if_having_movie = models.CharField(max_length=200)
    if_issue_date = models.DateField(null=True, blank=True)
    if_return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return ('Member Name: ' + self.name )


