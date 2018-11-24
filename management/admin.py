from django.contrib import admin
from .models import Book, Movies, Memberships
# Register your models here.

admin.site.register(Book)
admin.site.register(Movies)
admin.site.register(Memberships)