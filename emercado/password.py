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
from django.conf import settings
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
import smtplib
from django.core.mail import get_connection


# Consumer
def Forgot_Password(request):
    context = {
        "error_msg":"",
        "success_msg":""
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Consumer.objects.get(email=email)
        except Consumer.DoesNotExist:
            return render(request, "password/password_consumer/password_reset.html", {"ReqParams": ReqParams, "context": context})

        reset_link_expiration = datetime.now() + timedelta(hours=3)

        token = get_random_string(length=32) # generate a random token
        user.reset_password_token = token
        user.reset_password_token_expiry = reset_link_expiration
        user.save()

        # Send a password reset email to the user
        reset_url = f"{request.scheme}://{request.get_host()}/password_reset_confirm/{token}/"
        first_name = user.first_name
        subject = 'Checkout Reset Password Email'
        message = render_to_string('password/forgotpassword_email.html', {'reset_url': reset_url, 'first_name':first_name})
        from_email = 'outlook_90311B5164E86D4B@outlook.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, html_message=message)

        context["success_msg"] = "An email has been sent to your email address with instructions on how to reset your password."
        return render(request, "password/password_consumer/password_reset_sent.html", {"ReqParams": ReqParams, "context": context})

    return render(request, 'password/password_consumer/password_reset.html', {"ReqParams":ReqParams, "context":context})
   

def Forgot_Password_Sent(request):

   return render(request,'password/password_consumer/password_reset_sent.html',{"ReqParams":ReqParams})

def Forgot_Password_Confirm(request, token):
    context = {
        "error_msg":"",
        "success_msg":""
    }
    try:
        user = Consumer.objects.get(reset_password_token=token)
    except Consumer.DoesNotExist:
        context["error_msg"] = "Invalid or expired reset link."
        return render(request, "password/password_consumer/password_reset.html", {"ReqParams": ReqParams, "context": context})
    
    now = datetime.now()
    now_local = pytz.utc.localize(now)

    if user.reset_password_token_expiry > now_local:
            context["error_msg"] = "The password reset link has expired."
            return render(request, "password/password_consumer/password_reset.html", {"ReqParams": ReqParams, "context": context})

    if request.method == 'POST':
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        if password == confirm_password:
            print("password: " + str(password))
            print("confirm_password: " + str(confirm_password))
            # Reset the user's password and clear the reset token
            passwords = password
            passAscii = passwords.encode("ascii")
            passBytes = base64.b64encode(passAscii)
            user.password = passBytes
            user.reset_password_token = None
            user.reset_password_token_expiry = None
            user.save()
            context["success_msg"] = "Your password has been reset successfully."
            return render(request, "password/password_consumer/password_reset_complete.html", {"ReqParams": ReqParams, "context": context})
        else:
            messages.error(request, "Passwords do not match.")
            return redirect(f'/password_reset_confirm/{token}/')

    return render(request, 'password/password_consumer/password_reset_form.html', {'token': token, "context":context})

def Forgot_Password_Complete(request):

   return render(request,'password/password_consumer/password_reset_complete.html',{"ReqParams":ReqParams})



# Merchant
def Merchant_Forgot_Password(request):
    context = {
        "error_msg":"",
        "success_msg":""
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Store_Info.objects.get(email_address=email)
        except Store_Info.DoesNotExist:
            context["error_msg"] = "This email is not registered."
            return render(request, "password/password_store/password_reset.html", {"ReqParams": ReqParams, "context": context})

        reset_link_expiration = datetime.now() + timedelta(hours=3)

        token = get_random_string(length=32) # generate a random token
        user.reset_password_token = token
        user.reset_password_token_expiry = reset_link_expiration
        user.save()

        # Send a password reset email to the user
        reset_url = f"{request.scheme}://{request.get_host()}/merchant/password_reset_confirm/{token}/"
        first_name = user.first_name
        subject = 'Checkout Merchant Reset Password Email'
        message = render_to_string('password/merchant_forgotpassword_email.html', {'reset_url': reset_url, 'first_name':first_name})
        from_email = 'outlook_90311B5164E86D4B@outlook.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, html_message=message)

        context["success_msg"] = "An email has been sent to your email address with instructions on how to reset your password."
        return render(request, "password/password_store/password_reset_sent.html", {"ReqParams": ReqParams, "context": context})

    return render(request, 'password/password_store/password_reset.html', {"ReqParams":ReqParams, "context":context})
   

def Merchant_Forgot_Password_Sent(request):

   return render(request,'password/password_store/password_reset_sent.html',{"ReqParams":ReqParams})

def Merchant_Forgot_Password_Confirm(request, token):
    context = {
        "error_msg":"",
        "success_msg":""
    }
    try:
        user = Store_Info.objects.get(reset_password_token=token)
    except Store_Info.DoesNotExist:
        context["error_msg"] = "Invalid or expired reset link."
        return render(request, "password/password_store/password_reset.html", {"ReqParams": ReqParams, "context": context})
    
    now = datetime.now()
    now_local = pytz.utc.localize(now)

    if user.reset_password_token_expiry > now_local:
            context["error_msg"] = "The password reset link has expired."
            return render(request, "password/password_store/password_reset.html", {"ReqParams": ReqParams, "context": context})

    if request.method == 'POST':
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        if password == confirm_password:
            print("password: " + str(password))
            print("confirm_password: " + str(confirm_password))
            # Reset the user's password and clear the reset token
            passwords = password
            passAscii = passwords.encode("ascii")
            passBytes = base64.b64encode(passAscii)
            user.password = passBytes
            user.reset_password_token = None
            user.reset_password_token_expiry = None
            user.save()
            context["success_msg"] = "Your password has been reset successfully."
            return render(request, "password/password_store/password_reset_complete.html", {"ReqParams": ReqParams, "context": context})
        else:
            messages.error(request, "Passwords do not match.")
            return redirect(f'/merchant/password_reset_confirm/{token}/')

    return render(request, 'password/password_store/password_reset_form.html', {'token': token, "context":context})

def Merchant_Forgot_Password_Complete(request):

   return render(request,'password/password_store/password_reset_complete.html',{"ReqParams":ReqParams})
