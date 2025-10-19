from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


from . import mail as mailer
from django.conf import settings


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
from django.conf import settings
from restaurant import mailer  # Ensure mailer.py exists in restaurant app

def confirmation(request):

    template_name = "restaurant/confirmation.html"
    context = {
        "time": time.ctime(), 
    }
    try:
        mailer.send_order_email(
            subject="Order confirmation",
            message=f"Your order was placed at {time.ctime()}",
            recipient_list=[getattr(settings, "DEFAULT_CONTACT_EMAIL", "customer@example.com")],
        )
    except Exception as e:
        # Print to stdout so Vercel runtime logs contain the error
        print("Email send failed:", e)

    return render(request, template_name, context)



