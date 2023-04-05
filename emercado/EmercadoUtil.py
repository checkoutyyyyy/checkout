from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from .EmercadoDB import *
from .models import *
import json
from django.shortcuts import redirect,HttpResponseRedirect
from django.http import JsonResponse
from django.conf import settings

from django.http import HttpResponse
from random import randint
import base64
import os
from smtplib import SMTPException
from django.core.mail import EmailMessage


def handle_uploaded_file(file):
    with open('Post_Media/' + file.name,'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

def upload_product_image(file,id1,id2):
    new_name = id1 + "." + id2 + ".jpg"
    new_path = os.path.join('Post_Media/', new_name)
    with open(new_path,'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

def upload_storepic_image(file,id1,id2):
    new_name = id1 + "." + id2 + ".jpg"
    new_path = os.path.join('Post_Media/', new_name)
    with open(new_path,'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

def upload_profilepic_image(file,id1,id2):
    new_name = str(id1) + "." + str(id2) + ".jpg"
    new_path = os.path.join('Post_Media/', new_name)
    with open(new_path,'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

def upload_profilepicture_image(file,id1,id2):
    new_name = str(id1) + "." + str(id2) + ".jpg"
    new_path = os.path.join('Post_Media/', new_name)
    with open(new_path,'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

def upload_discount_file(file,id1,id2):
    new_name = "discount_file_" + str(id1) + "." + str(id2) + ".jpg"
    new_path = os.path.join('Post_Media/', new_name)
    with open(new_path,'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

def StringTolist(string,separator):
  
    retval = []
    string_len = len(string)
    i = 0
    j = i + 1
    charval = ""

    while i < string_len:
        if string[i] == separator:
            retval.append(charval)
            i = i + 1
            charval = ""
        else:
            charval += string[i]
            i = i + 1

    return retval        

def set_browse_img(request):
    context = {}

    if request.method == "POST":
        image = Product_Images()
        this_value = json.loads(request.POST['value']) 
        print(this_value)
        this_id = request.POST["product_id"]
        if Products.objects.filter(pk = this_id).exists():
            product = Products.objects.get(pk = this_id)
            # image.file_name = this_value
            # image.product_id = product
            # image.save()
            # handle_uploaded_file(this_value)
            context["success"] = 1

    return HttpResponse(json.dumps(context), "application/json")

def send_email(request):
    subject = "Test"
    recipient_list = ["cjbautistadev03@gmail.com", ]
    email = EmailMessage(subject, "test", "cjbautistauchiha@gmail.com", recipient_list )


    try:
        print(email)
        email.send()
        print("email sent")
    except SMTPException as e:          # It will catch other errors related to SMTP.
        print('There was an error sending an email.')
        print(e)

    return HttpResponseRedirect("/")    