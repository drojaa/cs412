from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
# Create your views here.


import random
import time

#list containing all quotes
quotes = ["I don't belong to anyone else but myself. I have to make my own decisions. Happiness is defined by me.", "We don’t all need to look the same. Beauty is in the eye of the beholder, you decide what’s beautiful in the world. Not the other way around.", "Dream big, work hard, and surround yourself with good people", 'Never let your dream die in the midst of doing the things you have to do to get what you need to invest in yourself. This is the hardest part, but you are worth it', 'You have to understand that when things go wrong in your life, it doesn’t mean you need to quit. It means you need to get stronger and change your plan.']

#list containing all images
images = ["keke1.png", "keke2.png", "keke3.jpg", "keke4.jpg.webp", "keke5.jpg.webp"]

#list containing tuples with both quotes and images
quotes_map_images = [
    ("I don't belong to anyone else but myself. I have to make my own decisions. Happiness is defined by me.", 'keke1.png'),
    ('We don’t all need to look the same. Beauty is in the eye of the beholder, you decide what’s beautiful in the world. Not the other way around.', 'keke2.png'),
    ('Dream big, work hard, and surround yourself with good people', 'keke3.jpg'),
    ('Never let your dream die in the midst of doing the things you have to do to get what you need to invest in yourself. This is the hardest part, but you are worth it', 'keke4.jpg.webp'),
    ('You have to understand that when things go wrong in your life, it doesn’t mean you need to quit. It means you need to get stronger and change your plan.', 'keke5.jpg.webp')
]

#function for homepage and single quotes
def quote(request):
  
    template_name = "quotes/quote.html"
    context = {
        "single_quote": random.choice(quotes),
        "single_image": random.choice(images),
        "time": time.ctime(), 
    }
    return render(request, template_name, context)
    
#function for page showing all quotes and all images
def show_all(request):

    template_name = "quotes/show_all.html"
    context = {
        "quotes" : quotes,
        "images" : images,
        "quotes_map_images" : quotes_map_images,
        "time": time.ctime(), 
    }
    return render(request, template_name, context)
#function for about page
def about(request):

    template_name = "quotes/about.html"
    context = {
          "time": time.ctime(), 
    }
    return render(request, template_name, context)


