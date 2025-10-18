from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
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

    message = Mail(
        from_email='derinellrojas@gmail.com',  # or your verified sender
        to_emails=[request.POST.get('customerEmail')],
        subject='Your Saweetie Treat Order Confirmation 🍓',
        html_content="""
        <div style="font-family: Arial, sans-serif; color:#333;">
            <h2>Hi {name},</h2>
            <p>Thank you for placing your order with <strong>Saweetie Treats</strong> 💖</p>
            <p>We’re getting your goodies ready! Here’s a quick summary:</p>
            <ul>
                <li><strong>Name:</strong> {name}</li>
                <li><strong>Email:</strong> {email}</li>
                <li><strong>Menu Item(s):</strong> {menu}</li>
                <li><strong>Today’s Special:</strong> {special}</li>
            </ul>
            <p>We’ll send another update when your treats are ready to pick up.</p>
            <p>Wishing you a sweet day! 🍰✨<br>
            <em>The Saweetie Treats Team</em></p>
        </div>
        """.format(
            name=request.POST.get("customerName", "Customer"),
            email=request.POST.get("customerEmail", ""),
            menu=", ".join(request.POST.getlist("menuItem")),
            special=request.POST.get("todaySpecial", "None"),
        ),
    )

    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        print("Status:", response.status_code)
        print("Body:", response.body)
        print("Headers:", response.headers)
    except Exception as e:
        print("SendGrid error:", str(e))




    return render(request, template_name, context=context)