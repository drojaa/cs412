from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
# Create your views here.

import time
import random

def home(request):
    '''
    Define a view to handle the 'home' request.
    '''
    current_time = time.ctime()

    response_text = f'''
    <html>
    <h1>Hello, boo!</h1>
    </html>
    '''
    
    return HttpResponse(response_text)

def home_page(request):

    template_name = "hw/home.html"
    context = {
        "time": time.ctime(),
        "letter1": chr(random.randint(1,100)),
        "letter2": chr(random.randint(1,100))
    }
    return render(request, template_name, context)

def about(request):
    template_name="hw/about.html"
    context = {
        "time": time.ctime(),
        "letter1": chr(random.randint(1,100)),
        "letter2": chr(random.randint(1,100)),
    }
    return render(request, template_name, context)
