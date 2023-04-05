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
from django.shortcuts import redirect, HttpResponseRedirect
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
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
scheduler.start() #start the scheduler

def ID_FORMAT(id,idtype):
    retval = idtype
    id_len = 12
    lastid = str(id)
    lastid_len = len(lastid)
    len_zeros = id_len - lastid_len
    while len_zeros != 0:
        retval += "0"
        len_zeros -= 1
    retval += lastid

    return retval

def generate_store_id():
    n = 15
    does_exists = 1
    retval = ""
    while does_exists == 1:
        obj = ''.join(random.choice(string.digits) for num in range(n))
        if Store_Info.objects.filter(pk=obj).exists():
            does_exists = 1
        else:
            retval = obj
            does_exists = 0

    return retval

def generate_random():
    n = 10
    obj = ''.join(random.choice(string.digits) for num in range(n))
    return obj


def Merchant_Register(request):

    if request.method == "POST":
        store = Store_Info()
        store.email_address = request.POST.get(ReqParams.email_address)
        store.first_name = request.POST.get(ReqParams.firstname)
        store.last_name = request.POST.get(ReqParams.lastname)
        store.store_address1 = request.POST.get("address1")
        # store.store_address2 = request.POST.get("address2")
        store.store_name = request.POST.get(ReqParams.business_name)
        store.phone_number = request.POST.get("phone")
        store.store_category = "Food and Drinks"
        this_random = generate_random()
        if 'profile_picture' in request.FILES:
            upload_profilepicture_image(request.FILES.get(
                "profile_picture"), store.store_id, this_random)
            store.profile_picture = str(
                store.store_id) + "." + str(this_random) + ".jpg"

        this_random = generate_random()
        if 'profile_pic' in request.FILES:
            upload_profilepic_image(request.FILES.get(
                "profile_pic"), store.store_id, this_random)
            store.profile_pic = str(
                store.store_id) + "." + str(this_random) + ".jpg"
            
        store.store_link = settings.URL_SITE_DOMAIN + \
            "/store/" + str(store.store_id)
        store.save()
        #token = get_random_string(length=8)  # generate a random token
        token = store.first_name
        # convertion into base64
        password = token  # default password as for now
        passAscii = password.encode("ascii")
        passBytes = base64.b64encode(passAscii)
        store.password = passBytes
        user_name = store.first_name + str(store.store_id)
        store.user_name = user_name
        store.status = 1
        store.save()
        store.store_link = settings.URL_SITE_DOMAIN + \
            "/store/" + str(store.store_id)
        store.save()
        store.id_format = ID_FORMAT(store.store_id,"MER")
        store.save()

        reset_url = f"{request.scheme}://{request.get_host()}/"
        first_name = store.first_name
        subject = 'Checkout Registered Successfully'
        message = render_to_string('password/register_merchant_email.html', {'reset_url': reset_url, 'first_name':first_name})
        from_email = 'outlook_90311B5164E86D4B@outlook.com'
        recipient_list = [store.email_address]
        send_mail(subject, message, from_email,recipient_list, html_message=message)
        
        # Send a password reset email to the user
        # reset_url = f"{request.scheme}://{request.get_host()}/merchant/login/{token}/"
        # subject = 'Checkout Registered Successfully'
        # message = render_to_string('password/get_password_email.html', {'reset_url': reset_url, 'password': password, 'user_name': user_name })
        # from_email = 'outlook_90311B5164E86D4B@outlook.com'
        # recipient_list = [store.email_address]
        # send_mail(subject, message, from_email,
        #           recipient_list, html_message=message)

        request.session["user_name"] = user_name
        messages.success(request, "Merchant Registration Successful")

        return HttpResponseRedirect("/register_successful")
    return render(request, "merchant/merchant_registration.html", {"ReqParams": ReqParams})



def check_email(request):
    context = {}

    if request.method == "POST":
        this_email = request.POST["value"]
        if Store_Info.objects.filter(email_address=this_email).exists():
            context["success"] = 1
        else:
            context["success"] = 0

    return HttpResponse(json.dumps(context), "application/json")


def check_username(request):
    context = {}

    if request.method == "POST":
        this_value = request.POST["value"]
        if Store_Info.objects.filter(user_name=this_value).exists():
            context["success"] = 1
        else:
            context["success"] = 0

    return HttpResponse(json.dumps(context), "application/json")


def check_phone(request):
    context = {}
    if request.method == "POST":
        if Store_Info.objects.filter(phone_number=request.POST["value"]).exists():
            context["success"] = 1
        else:
            context["success"] = 0

    return HttpResponse(json.dumps(context), "application/json")


def Merchant_Register_Successful(request):

    return render(request, 'merchant/register_successful.html', {"ReqParams": ReqParams})

def Discount_Requests(request,id):

    if ReqParams.owner_userid not in request.session:
        return HttpResponseRedirect("/")
    this_request = None
    if Personnel_Discount_Requests.objects.filter(pk = id).exists():
        this_request = Personnel_Discount_Requests.objects.get(pk = id)
    else:
        return HttpResponseRedirect("/page_not_found")    
    
    return render(request, 'store/personnel_discount_request.html', {"ReqParams": ReqParams,"this_request":this_request})

def is_what_percent_of(num_a, num_b):
    return (num_a * num_b) / 100

def accept_discount_request(request):

    context = {}
    if request.method == "POST":
        this_id = request.POST["this_id"]
        this_request = Personnel_Discount_Requests.objects.get(pk = this_id)
        this_discount = Discount_Personnel.objects.get(pk = this_request.personnel_discount_id)
        this_notification = Notifications.objects.get(merchant_id = this_request.store_id, order_id = this_request.order_id )
        this_account = Consumer.objects.get(pk = this_request.consumer_id)
        merchant = Store_Info.objects.get(pk = this_request.store_id)
        new_notif = Notifications()
        new_notif.consumer_id = this_account.pk
        new_notif.consumer_id_format = this_account.id_format
        new_notif.requested_response = "Rejected"
        new_notif.account_responded = this_request.store_id
        new_notif.account_responded_id_format  = this_request.store_id_format
        new_notif.account_responded_name  = merchant.store_name
        new_notif.order_id = this_request.order_id
        new_notif.order_id_format = this_request.order_id_format
        new_notif.content = f"Your discount request for order {this_request.order_id_format} has been accepted by the merchant."
        new_notif.url = settings.URL_SITE_DOMAIN + "/my_purchases"
        new_notif.notif_type = "Personnel Discount Request"
        new_notif.image = merchant.profile_picture
        new_notif.date_time = datetime.now()
        new_notif.save()
        order = Orders.objects.get(pk = this_request.order_id)
        order.discounted_flag = 1
        order.personnel_discount_id = this_request.pk
        order.personnel_status = this_discount.personnel_status
        order.percentage_discount = this_discount.discount_percentage
        order.total_personnel_discount = is_what_percent_of(this_discount.discount_percentage, order.total)
        order.total = order.total - is_what_percent_of(this_discount.discount_percentage, order.total)
        order.save()
        this_request.delete()
        this_notification.delete()
        context["success"] = 1
        context["msg"] = "Accepted!"
        

    return HttpResponse(json.dumps(context), "application/json")

def reject_discount_request(request):

    context = {}
    if request.method == "POST":
        this_id = request.POST["this_id"]
        this_request = Personnel_Discount_Requests.objects.get(pk = this_id)
        this_discount = Discount_Personnel.objects.get(pk = this_request.personnel_discount_id)
        this_notification = Notifications.objects.get(merchant_id = this_request.store_id, order_id = this_request.order_id )
        this_account = Consumer.objects.get(pk = this_request.consumer_id)
        merchant = Store_Info.objects.get(pk = this_request.store_id)
        new_notif = Notifications()
        new_notif.consumer_id = this_account.pk
        new_notif.consumer_id_format = this_account.id_format
        new_notif.requested_response = "Rejected"
        new_notif.account_responded = this_request.store_id
        new_notif.account_responded_id_format  = this_request.store_id_format
        new_notif.account_responded_name  = merchant.store_name
        new_notif.order_id = this_request.order_id
        new_notif.order_id_format = this_request.order_id_format
        new_notif.content = f"Your discount request for order {this_request.order_id_format} has been rejected by the merchant."
        new_notif.url = settings.URL_SITE_DOMAIN + "/my_purchases"
        new_notif.notif_type = "Personnel Discount Request"
        new_notif.image = merchant.profile_picture
        new_notif.date_time = datetime.now()
        new_notif.save()
        this_request.delete()
        this_notification.delete()
        context["success"] = 1
        context["msg"] = "Denied!"
        

    return HttpResponse(json.dumps(context), "application/json")

def Start_Voucher(id):

    if Vouchers.objects.filter(pk = id).exists():
        this_voucher = Vouchers.objects.get(pk = id)
        this_voucher.status = "Ongoing"
        this_voucher.save()
        # send email and notification to the merchant when its start
    return 0

def Stop_Voucher(id):

    if Vouchers.objects.filter(pk = id).exists():
        this_voucher = Vouchers.objects.get(pk = id)
        this_voucher.status = "Expired"
        this_voucher.save()
        # send email and notification to the merchant when its stop

    return 0

def add_product_vouchers(request):
    if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
        return HttpResponseRedirect("/page_not_found")
    
    id = request.session.get(ReqParams.owner_userid)
    store = Store_Info.objects.get(store_id=id)

    owner = Store_Info.objects.get(
    store_id=request.session.get(ReqParams.owner_userid))

    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]

    all_products = Products.objects.filter(is_archived=False, display_flag=1,store_id=store.id)
    merchant = Store_Info.objects.get(pk = request.session.get(ReqParams.owner_userid))
    if request.method == "POST":
        voucher = Vouchers()
        voucher.voucher_name = request.POST.get("name")
        voucher.date_start = request.POST.get("date_start")
        voucher.date_end = request.POST.get("date_end")
        voucher.voucher_type = "Product Voucher"
        voucher.discount_type = request.POST.get("discount_type")
        voucher.time_start = request.POST.get("time_start")
        voucher.time_end = request.POST.get("time_end")
        voucher.usage_quantity = request.POST.get("usage_quantity")
        if request.POST.get("discount_type") == "Fix Amount":
            voucher.fix_amount_discount = request.POST.get("amount_percentage")
        else:
            voucher.discount_percentage = request.POST.get("amount_percentage")
        product_list = request.POST.getlist("selected_products[]")
        for product in product_list:
            voucher.product_list += product + ","
        voucher.save()
        voucher.id_format = ID_FORMAT(voucher.id,"VOUCHER") 
        voucher.minimum_spend = request.POST.get("min_spend")
        voucher.store_id = request.session.get(ReqParams.owner_userid)
        voucher.store_id_format = merchant.id_format
        date_start = request.POST.get("date_start")
        date_time_obj = datetime.strptime(date_start, '%Y-%m-%d')
        today = datetime.strptime(str(date.today()), '%Y-%m-%d')
        time_start = voucher.time_start + ":00"
        time_start_object = datetime.strptime(time_start, '%H:%M:%S')
        schedId = f"voucher_start{voucher.id}"
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        time_obj = datetime.strptime(current_time, '%H:%M:%S')
        if date_time_obj > today:
            voucher.status = "Pending"
        elif date_time_obj == today or date_time_obj < today:
            if time_start_object > time_obj:
                voucher.status = "Pending"
            elif time_start_object < time_obj or time_start_object == time_obj:
                voucher.status = "Ongoing"  
        voucher.save()

        if voucher.status == "Pending":
            #schedule to start the voucher  
            schedId = f"voucher_start{voucher.id}"
            scheduler.add_job(func=Start_Voucher, args=[voucher.id],trigger='cron', hour=time_start_object.hour, minute=time_start_object.minute, month=date_time_obj.month, day=date_time_obj.day, year=date_time_obj.year, id=schedId,replace_existing=True,misfire_grace_time=None)
        time_end = voucher.time_end  
        time_end_object = datetime.strptime(time_end, '%H:%M')  
        date_end = voucher.date_end
        date_end_obj = datetime.strptime(date_end, '%Y-%m-%d')
        schedId = f"voucher_stop{voucher.id}"
        scheduler.add_job(func=Stop_Voucher, args=[voucher.id],trigger='cron', hour=time_end_object.hour, minute=time_end_object.minute, month=date_end_obj.month, day=date_end_obj.day, year=date_end_obj.year, id=schedId,replace_existing=True,misfire_grace_time=None) 

        try:
            scheduler.start()
        except:
            scheduler.resume()

        return HttpResponseRedirect("/seller/product_vouchers")
    return render(request,"store/add_product_vouchers.html",{"ReqParams": ReqParams, "owner": owner, "store": store, "all_notifications":all_notifications, "all_products":all_products})

def add_shop_vouchers(request):
    if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
        return HttpResponseRedirect("/page_not_found")
    
    id = request.session.get(ReqParams.owner_userid)
    store = Store_Info.objects.get(store_id=id)

    owner = Store_Info.objects.get(
    store_id=request.session.get(ReqParams.owner_userid))

    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]


    all_products = Products.objects.filter(is_archived=False, display_flag=1)
    merchant = Store_Info.objects.get(pk = request.session.get(ReqParams.owner_userid))
    if request.method == "POST":
        voucher = Vouchers()
        voucher.voucher_name = request.POST.get("name")
        voucher.date_start = request.POST.get("date_start")
        voucher.date_end = request.POST.get("date_end")
        voucher.voucher_type = "Shop Voucher"
        voucher.discount_type = request.POST.get("discount_type")
        voucher.time_start = request.POST.get("time_start")
        voucher.time_end = request.POST.get("time_end")
        voucher.usage_quantity = request.POST.get("usage_quantity")
        if request.POST.get("discount_type") == "Fix Amount":
            voucher.fix_amount_discount = request.POST.get("amount_percentage")
        else:
            voucher.discount_percentage = request.POST.get("amount_percentage")
    
        voucher.save()
        voucher.id_format = ID_FORMAT(voucher.id,"VOUCHER") 
        voucher.minimum_spend = request.POST.get("min_spend")
        voucher.store_id = request.session.get(ReqParams.owner_userid)
        voucher.store_id_format = merchant.id_format
        date_start = request.POST.get("date_start")
        date_time_obj = datetime.strptime(date_start, '%Y-%m-%d')
        today = datetime.strptime(str(date.today()), '%Y-%m-%d')
        time_start = voucher.time_start + ":00"
        time_start_object = datetime.strptime(time_start, '%H:%M:%S')
        schedId = f"voucher_start{voucher.id}"
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        time_obj = datetime.strptime(current_time, '%H:%M:%S')
        if date_time_obj > today:
            voucher.status = "Pending"
        elif date_time_obj == today or date_time_obj < today:
            if time_start_object > time_obj:
                voucher.status = "Pending"
            elif time_start_object < time_obj or time_start_object == time_obj:
                voucher.status = "Ongoing"  
        voucher.save()

        if voucher.status == "Pending":
            #schedule to start the voucher  
            schedId = f"voucher_start{voucher.id}"
            scheduler.add_job(func=Start_Voucher, args=[voucher.id],trigger='cron', hour=time_start_object.hour, minute=time_start_object.minute, month=date_time_obj.month, day=date_time_obj.day, year=date_time_obj.year, id=schedId,replace_existing=True,misfire_grace_time=None)
        time_end = voucher.time_end  
        time_end_object = datetime.strptime(time_end, '%H:%M')  
        date_end = voucher.date_end
        date_end_obj = datetime.strptime(date_end, '%Y-%m-%d')
        schedId = f"voucher_stop{voucher.id}"
        scheduler.add_job(func=Stop_Voucher, args=[voucher.id],trigger='cron', hour=time_end_object.hour, minute=time_end_object.minute, month=date_end_obj.month, day=date_end_obj.day, year=date_end_obj.year, id=schedId,replace_existing=True,misfire_grace_time=None) 

        try:
            scheduler.start()
        except:
            scheduler.resume()

        return HttpResponseRedirect("/seller/shop_vouchers")

    return render(request,"store/add_shop_vouchers.html",{"ReqParams": ReqParams, "owner": owner, "store": store, "all_notifications":all_notifications, "all_products":all_products})

def edit_variant_price(request):
    
    if request.method == "POST":
        this_id = request.POST["this_id"]
        variant = Product_Variations.objects.get(pk = this_id)
        variant.price = float(request.POST["value"])
        variant.save()

    return HttpResponse(json.dumps({}), "application/json")

def varaint_available_switch(request):
    if request.method == "POST":
        this_id = request.POST["this_id"]
        variant = Product_Variations.objects.get(pk = this_id)
        variant.available_flag = int(request.POST["value"])
        variant.save()

    return HttpResponse(json.dumps({}), "application/json")

def edit_variant_stocks(request):
    if request.method == "POST":
        this_id = request.POST["this_id"]
        variant = Product_Variations.objects.get(pk = this_id)
        variant.stocks = int(request.POST["value"])
        variant.save()

    return HttpResponse(json.dumps({}), "application/json")

def delete_variant(request):
    if request.method == "POST":
        this_id = request.POST["this_id"]
        variant = Product_Variations.objects.get(pk = this_id)
        product = Products.objects.get(pk = variant.product_id_id)
        options = StringTolist(variant.option_id,",")
        for opt in options:
            this_opt = Product_Attributes_Option.objects.get(pk = opt)
            this_opt.delete()
        variant.delete()    
        count = Product_Variations.objects.filter(product_id = product).count()
        attributes = Product_Attributes.objects.filter(product_id = product.pk)
        if count == 0:
            attributes = Product_Attributes.objects.filter(product_id = product.pk)
            for attr in attributes:
                attr.delete()
            product.has_variation = 0
            product.save()
        context = {
            "success":1,
            "id":this_id
        }

    return HttpResponse(json.dumps(context), "application/json")
