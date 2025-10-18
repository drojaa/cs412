from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail

# Create your views here.
import time
import random
#function to make form appear
def show_form(request):
    '''Show the web page with the form.'''

    template_name = "formdata/show_form.html"
    return render(request, template_name)
#function called when pressing submit button
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
        #maps selected menu items to price, and add it to total cost
        total_cost += sum(menu_prices.get(item, 0) for item in menuItem)
        #if user selects today special, then it will add the special's price to total
        if todaySpecial:
            special_prices = {
                "Dark Chocolate Covered Strawberries": 10.00,
            }
            total_cost += special_prices.get(todaySpecial, 0)
        #coverts to dollar format 
        total_cost = "{:.2f}".format(total_cost)

        curr_time = time.time()
        #converts min to seconds, return betwwen 30min - 1hr
        random_min = random.randint(1800, 3600)
        # add random value to current time 
        readyTime_seconds = curr_time + random_min
        # assign readyTime
        readyTime = time.ctime(readyTime_seconds)
        context = {
            'customerName' : customerName,
            'menuItem' : menuItem,
            'todaySpecial' : todaySpecial,
            'totalCost': total_cost,
            "readyTime": readyTime, 
            "time": time.ctime()
        }
  
        message = (
    f"Hi {request.POST['customerName']},\n\n"
    f"Thank you so much for placing your order with Saweetie Treats! 💖\n"
    f"We’re thrilled to start preparing your goodies — they’re going to be as sweet as you are.\n\n"
    f"Here’s a quick summary of your order:\n"
    f"- Customer Name: {request.POST['customerName']}\n"
    f"- Email: {request.POST['customerEmail']}\n"
    f"- Phone: {request.POST['customerPhone']}\n"
    f"- Menu Item(s): {', '.join(menuItem)}\n"
    f"- Today’s Special: {todaySpecial if todaySpecial else 'None'}\n\n"
    f"We’ll send another update when your treats are ready to pick up.\n"
    f"If you have any changes or special requests, just reply to this email — we’re happy to help!\n\n"
    f"Wishing you a beautiful (and delicious) day! 🍓✨\n\n"
    f"- The Saweetie Treats Team\n\n"
    f"Order Time: {time.ctime()}\n"
)
        send_mail(
    subject="New Saweetie Treat Order",
    message=message,
    from_email="derinellrojas@gmail.com",
    recipient_list=[request.POST['customerEmail']]
    )





    return render(request, template_name, context=context)