from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
import time
import random

def show_form(request):
    '''Show the web page with the form.'''

    template_name = "formdata/show_form.html"
    return render(request, template_name)

def submit(request):
    '''Process the form submission'''
    template_name = "formdata/confirmation.html"
    menu_prices = {
        "Red Velvet Cake Pops": 3.00,
        "Chocolate Truffle Cake Pops": 3.00,
        "Churro Spice Cake Pops": 3.00,
        "Salted Caramel Swirl": 12.00,
        "Coconut Cloud Cupcakes": 5.00,
        "Lemon Raspberry Cheese Danish": 3.00,
    }
    total_cost = 0
    if request.POST:
        customerName = request.POST["customerName"]
        menuItem = request.POST.getlist("menuItem")
        todaySpecial = request.POST.get("todaySpecial", "")

        total_cost += sum(menu_prices.get(item, 0) for item in menuItem)
        if todaySpecial:
            special_prices = {
                "Dark Chocolate Covered Strawberries": 10.00,
            }
            total_cost += special_prices.get(todaySpecial, 0)
        total_cost = "{:.2f}".format(total_cost)
        curr_time = time.time()
        random_min = random.randint(1800, 3600)
        readyTime_seconds = curr_time + random_min
        readyTime = time.ctime(readyTime_seconds)
        context = {
            'customerName' : customerName,
            'menuItem' : menuItem,
            'todaySpecial' : todaySpecial,
            'totalCost': total_cost,
            "readyTime": readyTime, 
            "time": time.ctime()
        }

    return render(request, template_name, context=context)