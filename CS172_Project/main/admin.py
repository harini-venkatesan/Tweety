from django.contrib import admin
from .models import Tweets
# Register your models here.

# Registering Tweets to show on admin site
# to input data for testing
admin.site.register(Tweets)