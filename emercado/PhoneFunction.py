from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from .EmercadoDB import *
from .EmercadoUtil import *
from .models import *
from django.db.models import Q  # New
from .models import Store_Info
import json
from django.shortcuts import redirect,HttpResponseRedirect
from django.http import JsonResponse
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
import random
from datetime import datetime, timedelta
import string
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from random import randint
import base64
from .tokens import generate_token
import pytz
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django import template
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives, send_mail, BadHeaderError, EmailMessage

def LoginPage_PhoneNumber(request):
    context = {}
    return render(request, 'phonenumber/login_phonenum.html', context)

    
def VerificationPage_CodeNumber(request):
    context = {}
    return render(request, 'phonenumber/login_verify_code.html', context)

def Login_Forgot_Number(request):
    context = {
        "error_msg":"",
        "success_msg":""
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Consumer.objects.get(email=email)
        except Consumer.DoesNotExist:
            context["error_msg"] = "This email is not registered."
            return render(request, "phonenumber/login_forgot_number.html", {"ReqParams": ReqParams, "context": context})

        reset_link_expiration_date = datetime.now() + timedelta(hours=3)

        token = get_random_string(length=32) # generate a random token
        user.reset_number_token = token
        user.reset_number_token_expiry = reset_link_expiration_date
        user.save()

        # Send a password reset email to the user
        reset_number_url = f"{request.scheme}://{request.get_host()}/login_forgot_number_reset/{token}/"
        first_name = user.first_name
        subject = 'Checkout Reset Number Email'
        message = render_to_string('password/forgotnumber_email.html', {'reset_number_url': reset_number_url, 'first_name': first_name})
        from_email = 'outlook_90311B5164E86D4B@outlook.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, html_message=message)

        context["success_msg"] = "An email has been sent to your email address with instructions on how to reset your number."
        return render(request, "phonenumber/login_forgot_number_sent.html", {"ReqParams": ReqParams, "context": context})
    return render(request, 'phonenumber/login_forgot_number.html', {"ReqParams":ReqParams, "context":context})


def Login_Forgot_Number_Sent(request):

    return render(request,"login_forgot_number_sent.html")

def Login_Forgot_Number_Reset(request, token):
    context = {
        "error_msg":"",
        "success_msg":""
    }
    try:
        user = Consumer.objects.get(reset_number_token=token)
    except Consumer.DoesNotExist:
        context["error_msg"] = "Invalid or expired reset link."
        return render(request, "phonenumber/login_forgot_number.html", {"ReqParams": ReqParams, "context": context})

    now = datetime.now()
    now_local = pytz.utc.localize(now)

    if user.reset_number_token_expiry > now_local:
            context["error_msg"] = "The number reset link has expired."
            return render(request, "phonenumber/login_forgot_number.html", {"ReqParams": ReqParams, "context": context})

    if request.method == 'POST':
        phone_number = request.POST.get('phonenumber')
        if phone_number.startswith('09') and len(phone_number) == 11 and phone_number.isdigit(): 
            user.phone_number1 = phone_number
            user.reset_number_token = None
            user.reset_number_token_expiry = None
            user.save()
            context["success_msg"] = "Your number has been reset successfully."
            return render(request, "phonenumber/login_forgot_number_code.html", {"ReqParams": ReqParams, "context": context})
        else:
            context["error_msg"] = "Invalid number"
            return redirect(f'/login_forgot_number_reset/{token}/', {"ReqParams": ReqParams, "context": context})
            # return render(request, "login_forgot_number_reset.html", {"ReqParams": ReqParams, "context": context})
    return render(request, 'phonenumber/login_forgot_number_reset.html', context)

def Login_Forgot_Number_Done(request):

    return render(request,"phonenumber/login_forgot_number_done.html")

def Login_Forgot_Number_Code(request):

    return render(request,"phonenumber/login_forgot_number_code.html")