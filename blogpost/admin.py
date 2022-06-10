from django.contrib import admin
from blogpost.models import BlogPost, PostComment


admin.site.register([BlogPost, PostComment])
# Register your models here.
