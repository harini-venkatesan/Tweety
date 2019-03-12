from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Tweets
from django.db.models import Q

# Create your views here.
def homepage(request):
    return render(request = request, template_name = "main/home.html")

def search(request):
    template = 'main/search.html'
    results = ''
    if 'q' in request.GET:
        query = request.GET['q']
        results = Tweets.objects.filter(tweet_text__icontains=query)
    context = {'results': results}
    return render(request, template, context)
    #return render(request =request, template_name="main/search.html" )