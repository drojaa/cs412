from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
import time 

#view function for main page
def main(request):

    template_name = "restaurant/main.html"
    context = {
          "time": time.ctime(), 
    }
    return render(request, template_name, context)
#view function for order page
def order(request):

    template_name = "restaurant/order.html"
    context = {
          "time": time.ctime(), 
    }
    return render(request, template_name, context)
#view function for confirmation page
def confirmation(request):

    template_name = "quotes/about.html"
    context = {
          "time": time.ctime(), 
    }
    return render(request, template_name, context)



