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
import random
from django.template.loader import render_to_string
from datetime import datetime, timedelta
import string
import pytz
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from random import randint
import base64
import qrcode
from io import BytesIO
from PIL import Image
from .tokens import generate_token
from django.db.utils import IntegrityError
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django import template
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives, send_mail, BadHeaderError, EmailMessage
from geopy.geocoders import Nominatim
from geopy import distance
from django.db.models import Q, F, Value, FloatField
import geocoder
import math
from django.http import JsonResponse

def save_location(request):
  if request.method == 'POST':
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')
    store_id = request.session.get('store_id')

    try:
      store_info = Store_Info.objects.get(store_id=store_id)
      store_info.latitude = latitude
      store_info.longitude = longitude
      store_info.save()
      return JsonResponse({'success': True})
    except Exception as e:
      return JsonResponse({'success': False, 'error': str(e)})
  else:
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
  
# def generate_qr_code(account_id):
#     qr = qrcode.QRCode(version=1, box_size=10, border=5)
#     qr.add_data(account_id)
#     qr.make(fit=True)
#     img = qr.make_image(fill_color='black', back_color='white')

#     # Save the image to a buffer
#     buffer = BytesIO()
#     img.save(buffer)
#     buffer.seek(0)

#     return buffer

def generate_qr_code(id_format, logo_image=None):
    # Generate the QR code image
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(id_format)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color='black', back_color='white')

    if logo_image is not None:
        # Resize the logo image
        logo_size = qr_image.size[0] // 8
        logo = logo_image.resize((logo_size, logo_size))

        # Create a blank image and paste the QR code onto it
        qr_with_logo = Image.new('RGB', qr_image.size, 'white')
        qr_with_logo.paste(qr_image, (0, 0))

        # Calculate the center coordinates of the QR code
        center_x = qr_image.size[0] // 2
        center_y = qr_image.size[1] // 2

        # Calculate the top-left coordinates of the logo image
        logo_x = center_x - logo_size // 2
        logo_y = center_y - logo_size // 2

        # Paste the logo image onto the QR code
        qr_with_logo.paste(logo, (logo_x, logo_y))

        # Save the QR code with the logo to a buffer
        buffer = BytesIO()
        qr_with_logo.save(buffer, format='PNG')
    else:
        # Save the QR code to a buffer
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')

    buffer.seek(0)
    return buffer


def ID_FORMAT(id, idtype):
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


def generate_account_id():
    n = 15
    does_exists = 1
    retval = ""
    while does_exists == 1:
        obj = ''.join(random.choice(string.digits) for num in range(n))
        if Consumer.objects.filter(pk=obj).exists():
            does_exists = 1
        else:
            retval = obj
            does_exists = 0
    return retval


def Anonymous_Key():
    n = 18
    obj = ''.join(random.choice(string.digits) for num in range(n))

    return obj


def EmercadoPage(request):
    request.session[ReqParams.ANONYMOUS_KEY] = get_random_string(length=28)
    stores = Store_Info.objects.all

    return render(request, "emercado.html", {"ReqParams": ReqParams, "stores": stores})


def generate_random():
    n = 7
    obj = ''.join(random.choice(string.digits) for num in range(n))
    return obj

def generate_verification_code():
    n = 6
    obj = ''.join(random.choice(string.digits) for num in range(n))
    return obj

def SignupPage(request):

    if request.method == "POST":
        new_user = Consumer()
        new_user.email = request.POST.get(ReqParams.email_address)
        new_user.first_name = request.POST.get(ReqParams.firstname)
        new_user.last_name = request.POST.get(ReqParams.lastname)
        new_user.address = request.POST.get(ReqParams.address)
        new_user.phone_number1 = request.POST.get(ReqParams.phone_number1)
        # new_user.phone_number2 = request.POST.get(ReqParams.phone_number2)
        new_user.user_name = request.POST.get(ReqParams.user_name)

        password = request.POST.get(ReqParams.password)
        # convertion into base64
        passAscii = password.encode("ascii")
        passBytes = base64.b64encode(passAscii)
        new_user.password = passBytes
        new_user.save()
        new_user.id_format = ID_FORMAT(new_user.account_id, "CUS")
        # Generate the QR code for the order
        qr_buffer = generate_qr_code(new_user.id_format, logo_image=Image.open(new_user.profile_picture))
        # Save the QR code image to the Order model
        new_user.qr_code.save(
            f'consumer_{new_user.id_format}.png', qr_buffer, save=True)
        
        account_verification_link_expiration = datetime.now() + timedelta(hours=3)
        token = generate_verification_code() # generate a random token
        new_user.account_verification_code = token
        new_user.account_verification_expiry = account_verification_link_expiration
        new_user.save()

        # Send a verification email to the user
        reset_url = f"{request.scheme}://{request.get_host()}/login_verification/{token}/"
        subject = 'Checkout Verification Code'
        message = render_to_string('password/verification_code_email.html', {'reset_url': reset_url, 'token':token})
        from_email = 'outlook_90311B5164E86D4B@outlook.com'
        recipient_list = [new_user.email]
        send_mail(subject, message, from_email,
                  recipient_list, html_message=message)

        messages.success(request, "User Successfully Registered. Please Check Your Email And Get Your Verification Code!")
        return HttpResponseRedirect("/login")

    return render(request, "signup_page.html", {"ReqParams": ReqParams})

def Login_Verification_Page(request, token):
    context = {
        "error_msg":"",
        "success_msg":""
    }
    try:
        user = Consumer.objects.get(account_verification_code=token)
    except Consumer.DoesNotExist:
        context["error_msg"] = "Invalid or verification code link."
        return render(request, "signup_page.html", {"ReqParams": ReqParams, "context": context})
    
    now = datetime.now()
    now_local = pytz.utc.localize(now)

    if user.account_verification_expiry > now_local:
            context["error_msg"] = "The verification code link has expired."
            return render(request, "signup_page.html", {"ReqParams": ReqParams, "context": context})

    if request.method == 'POST':
        verification = request.POST.get('verification_code')
        if user.account_verification_code == verification:
            user.account_verification_flag = 1
            user.save()
            context["success_msg"] = "Confirm successfully."
            return render(request, "login.html", {"ReqParams": ReqParams, "context": context})
        else:
            messages.error(request, "Verification code do not match.")
            return redirect(f'/login_verification/{token}/')

    return render(request, 'login_verification.html', {'token': token, "context":context})

def EmercadoPage(request):

    request.session[ReqParams.ANONYMOUS_KEY] = get_random_string(length=32)

    search_store = request.GET.get('search')

    if search_store:
        stores = Store_Info.objects.filter(
            Q(store_name__icontains=search_store))
    else:
        # If not searched, return default posts
        stores = Store_Info.objects.all().order_by("-store_id")

    products = Products.objects.filter(
        is_archived=False, display_flag=1, is_available=1)

    consumer = None
    my_cart = None
    notifications = None
    if Consumer.objects.filter(account_id=request.session.get(ReqParams.consumer_userid)).exists():
        consumer = Consumer.objects.get(
            account_id=request.session.get(ReqParams.consumer_userid))
        my_cart = Cart.objects.filter(
            account_id=consumer.account_id).order_by("-id")
        notifications = Notifications.objects.filter(
            consumer_id = request.session.get(ReqParams.consumer_userid)).order_by('-id')[:15]
    else:
        my_cart = Cart.objects.filter(account_id=request.session.get(
            ReqParams.ANONYMOUS_KEY)).order_by("-id")

    return render(request, "emercado.html", {"ReqParams": ReqParams, "consumer": consumer, "stores": stores, "my_cart": my_cart, "products": products,"notifications":notifications})

def distance(lat1, lon1, lat2, lon2):
    R = 6371  # radius of the Earth in kilometers
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def DinePage(request):
    address = request.POST.get('address', '')
    search = Store_Info.objects.filter(store_address2__icontains=address)
    
    g = geocoder.ip('me')

    # Get latitude and longitude
    #lat, lon = g.latlng
    lat = 0
    lon = 0
    if g.latlng:
        lat = g.latlng
        lon = g.latlng
    print(lat)
    # Assign values to lon1 and lat1 variables
    lon1 = lon
    lat1 = lat

    for store in search:
        lat2 = store.latitude
        lon2 = store.longitude
        try:
            store.distance_from_user = distance(lat1, lon1, lat2, lon2)
        except:
            pass
        
    
    searchstore = sorted(search, key=lambda x: x.distance_from_user)

    stores = Store_Info.objects.all()
    # Calculate the distance between the user's location and each store
    for store in stores:
        lat2 = store.latitude
        lon2 = store.longitude
        try:
            store.distance_from_user = distance(lat1, lon1, lat2, lon2)
        except:
            pass

        

    # Sort the stores by distance
    nearest_store = sorted(stores, key=lambda x: x.distance_from_user)
   
   # setting Anonymous key
    if ReqParams.ANONYMOUS_KEY not in request.session:
        request.session[ReqParams.ANONYMOUS_KEY] = get_random_string(length=32)

    search_store = request.GET.get('search')

    if search_store:
        stores = Store_Info.objects.filter(
            Q(store_name__icontains=search_store))
    else:
        # If not searched, return default posts
        stores = Store_Info.objects.all().order_by("-store_id")

    products = Products.objects.filter(is_archived=False, display_flag=1, is_available=1)

    products = Products.objects.filter(
        is_archived=False, display_flag=1, is_available=1)

    # attr_list = []
    # opt_list = []
    retval = []
    # store_list = []
    for product in products:
        attributes = Product_Attributes.objects.filter(
            product_id=product.product_id)
        if attributes:
            attr_temp = []
            opt_temp = []
            for attr in attributes:
                attr_temp.append(attr)
                opt_temp.append(
                    Product_Attributes_Option.objects.filter(attribute_id=attr.id))
            this_variant = zip(attr_temp, opt_temp)
            retval.append({
                "product_id": product.product_id,
                "default_image": product.default_image,
                "product_name": product.product_name,
                "available_flag": product.available_flag,
                "status_type": product.status_type,
                "stock": product.stock,
                "description": product.description,
                "variants": this_variant,
                "original_price": product.original_price,
                "images": Product_Images.objects.filter(product_id=product.product_id)
            })
        else:
            retval.append({
                "product_id": product.product_id,
                "default_image": product.default_image,
                "product_name": product.product_name,
                "available_flag": product.available_flag,
                "status_type": product.status_type,
                "description": product.description,
                "stock": product.stock,
                "variants": [],
                "original_price": product.original_price,
                "images": Product_Images.objects.filter(product_id=product.product_id)
            })
        
        consumer = None
        my_cart = None
        notifications = None
        if Consumer.objects.filter(account_id=request.session.get(ReqParams.consumer_userid)).exists():
            consumer = Consumer.objects.get(
                account_id=request.session.get(ReqParams.consumer_userid))
            my_cart = Cart.objects.filter(
                account_id=consumer.account_id).order_by("-id")
            notifications = Notifications.objects.filter(
                consumer_id = request.session.get(ReqParams.consumer_userid)).order_by('-id')[:15]
        else:
            my_cart = Cart.objects.filter(account_id=request.session.get(
                ReqParams.ANONYMOUS_KEY)).order_by("-id")
       

    return render(request, "dine.html", {"address":address,"searchstore":searchstore,"lat": lat1,"lng": lon1,"nearest_store":nearest_store,
                                        "ReqParams": ReqParams, "consumer": consumer, "stores": stores, 
                                        "my_cart": my_cart, "products": products, "retval": retval,"notifications":notifications,
                                        "nearest_store":nearest_store})


def LoginPage(request):

    context = {
        "userid": "",
        "error_msg": "",
        "success_msg": ""
    }
    if request.method == "POST":
        # we check weither user uses email or user name
        if Consumer.objects.filter(email=request.POST.get('userid')).exists():
            this_email = request.POST.get('userid')
            context["userid"] = request.POST.get('userid')
            this_user = Consumer.objects.get(email=this_email)
            password = request.POST.get(ReqParams.password)
            # convertion into base64
            passAscii = password.encode("ascii")
            passBytes = base64.b64encode(passAscii)
            if this_user.password == passBytes:
                # success login

                # we used this session/ cookie value to call data from other table
                # it is also going to be used to check if an user has been login
                request.session[ReqParams.consumer_userid] = this_user.account_id
                pathstr = "/"
                if ReqParams.LOGIN_REDIRECTION in request.session:
                    pathstr = request.session.get(ReqParams.LOGIN_REDIRECTION)

                if ReqParams.ANONYMOUS_KEY in request.session:
                    if Cart_Key.objects.filter(account_id=request.session.get(ReqParams.ANONYMOUS_KEY)).exists():
                        cart_key = Cart_Key.objects.filter(
                            account_id=request.session.get(ReqParams.ANONYMOUS_KEY))
                        for key in cart_key:
                            this_cart = Cart.objects.filter(cart_key=key.id)
                            this_key = None
                            if Cart_Key.objects.filter(account_id=this_user.account_id, store_id=key.store_id).exists():
                                this_key = Cart_Key.objects.get(
                                    account_id=this_user.account_id, store_id=key.store_id)
                            else:
                                this_key = Cart_Key()
                                this_key.account_id = this_user.account_id
                                this_key.store_id = key.store_id
                                this_key.save()

                            for cart in this_cart:
                                cart.account_id = this_user.account_id
                                cart.cart_key = this_key.id
                                cart.save()
                            key.account_id = this_user.account_id
                            key.delete()

                return HttpResponseRedirect(pathstr)
            else:
                context["error_msg"] = "Invalid Credentials!"
                return render(request, "login.html", {"ReqParams": ReqParams, "context": context})
        elif Consumer.objects.filter(user_name=request.POST.get('userid')).exists():
            this_username = request.POST.get('userid')
            context["userid"] = request.POST.get('userid')
            this_user = Consumer.objects.get(user_name=this_username)
            password = request.POST.get(ReqParams.password)
            # convertion into base64
            passAscii = password.encode("ascii")
            passBytes = base64.b64encode(passAscii)
            if this_user.password == passBytes:
                # success login

                # we used this session/ cookie value to call data from other table
                # it is also going to be used to check if an user has been login
                request.session[ReqParams.consumer_userid] = this_user.account_id
                pathstr = "/"
                if ReqParams.LOGIN_REDIRECTION in request.session:
                    pathstr = request.session.get(ReqParams.LOGIN_REDIRECTION)

                if ReqParams.ANONYMOUS_KEY in request.session:
                    if Cart_Key.objects.filter(account_id=request.session.get(ReqParams.ANONYMOUS_KEY)).exists():
                        cart_key = Cart_Key.objects.filter(
                            account_id=request.session.get(ReqParams.ANONYMOUS_KEY))
                        for key in cart_key:
                            this_key = None
                            this_cart = Cart.objects.filter(cart_key=key.id)
                            if Cart_Key.objects.filter(account_id=this_user.account_id, store_id=key.store_id).exists():
                                this_key = Cart_Key.objects.get(
                                    account_id=this_user.account_id, store_id=key.store_id)
                            else:
                                this_key = Cart_Key()
                                this_key.account_id = this_user.account_id
                                this_key.store_id = key.store_id
                                this_key.save()

                            for cart in this_cart:
                                cart.account_id = this_user.account_id
                                cart.cart_key = this_key.id
                                cart.save()
                            key.account_id = this_user.account_id
                            key.delete()
                return HttpResponseRedirect(pathstr)
            else:
                context["error_msg"] = "Invalid Credentials!"
                return render(request, "login.html", {"ReqParams": ReqParams, "context": context})
        else:
            context["userid"] = request.POST.get('userid')
            context["error_msg"] = "Invalid Credentials!"
            return render(request, "login.html", {"ReqParams": ReqParams, "context": context})

    return render(request, "login.html", {"ReqParams": ReqParams, "context": context})


def check_email(request):
    context = {}

    if request.method == "POST":
        this_email = request.POST["value"]
        if Consumer.objects.filter(email=this_email).exists():
            context["success"] = 1
        else:
            context["success"] = 0

    return HttpResponse(json.dumps(context), "application/json")


def check_username(request):
    context = {}

    if request.method == "POST":
        this_value = request.POST["value"]
        if Consumer.objects.filter(user_name=this_value).exists():
            context["success"] = 1
        else:
            context["success"] = 0

    return HttpResponse(json.dumps(context), "application/json")


def Error_Page(request):

    return render(request, "error_page.html", {"ReqParams": ReqParams})


def IndexPage(request):

    # setting Anonymous key
   
    request.session[ReqParams.ANONYMOUS_KEY] = get_random_string(length=28)

    search_store = request.GET.get('search')

    if search_store:
        stores = Store_Info.objects.filter(
            Q(store_name__icontains=search_store))
    else:
        # If not searched, return default posts
        stores = Store_Info.objects.all().order_by("-store_id")

    products = Products.objects.filter(is_archived=False, display_flag=1)

    consumer = None
    my_cart = None
    notifications = None
    if Consumer.objects.filter(account_id=request.session.get(ReqParams.consumer_userid)).exists():
        consumer = Consumer.objects.get(
            account_id=request.session.get(ReqParams.consumer_userid))
        my_cart = Cart.objects.filter(
            account_id=consumer.account_id).order_by("-id")
        notifications = Notifications.objects.filter(
            consumer_id = request.session.get(ReqParams.consumer_userid)).order_by('-id')[:15]
    else:
        my_cart = Cart.objects.filter(account_id=request.session.get(
            ReqParams.ANONYMOUS_KEY)).order_by("-id")

    return render(request, "index.html", {"ReqParams": ReqParams, "consumer": consumer, "stores": stores, "my_cart": my_cart, "products": products,"notifications":notifications})


def StorePage(request, id):

    this_store = Store_Info.objects.get(store_id=id)
    products = Products.objects.filter(
        store_id=this_store, is_archived=False, display_flag=1)

    # attr_list = []
    # opt_list = []
    retval = []
    #variants = []
    for product in products:
        attributes = Product_Attributes.objects.filter(
            product_id=product.product_id)
        if attributes:
            attr_temp = []
            opt_temp = []
            for attr in attributes:
                attr_temp.append(attr)
                opt_temp.append(
                    Product_Attributes_Option.objects.filter(attribute_id=attr.id))
            this_variant = zip(attr_temp, opt_temp)
            retval.append({
                "product_id": product.product_id,
                "default_image": product.default_image,
                "product_name": product.product_name,
                "available_flag": product.available_flag,
                "status_type": product.status_type,
                "stock": product.stock,
                "description": product.description,
                "variants": this_variant,
                "original_price": product.original_price,
                "images": Product_Images.objects.filter(product_id=product.product_id)

            })
        else:
            retval.append({
                "product_id": product.product_id,
                "default_image": product.default_image,
                "product_name": product.product_name,
                "available_flag": product.available_flag,
                "status_type": product.status_type,
                "description": product.description,
                "stock": product.stock,
                "variants": [],
                "original_price": product.original_price,
                "images": Product_Images.objects.filter(product_id=product.product_id)
            })
        
    consumer = None
    my_cart = None
    notifications = None
    if Consumer.objects.filter(account_id=request.session.get(ReqParams.consumer_userid)).exists():
        consumer = Consumer.objects.get(
            account_id=request.session.get(ReqParams.consumer_userid))
        my_cart = Cart.objects.filter(
            account_id=consumer.account_id).order_by("-id")
        notifications = Notifications.objects.filter(
            consumer_id = request.session.get(ReqParams.consumer_userid)).order_by('-id')[:15]
    else:
        my_cart = Cart.objects.filter(account_id=request.session.get(
            ReqParams.ANONYMOUS_KEY)).order_by("-id")
        
    return render(request, "stores.html", {"ReqParams": ReqParams, "consumer": consumer,
                                           "this_store": this_store, "products": products, "my_cart": my_cart, "retval": retval,"notifications":notifications})

def MenuPage(request, id):

    product = Products.objects.get(product_id=id)
    product_image = Product_Images.objects.filter(
        product_id=product.product_id)
    consumer = None
    my_cart = None
    notifications = None
    if Consumer.objects.filter(account_id=request.session.get(ReqParams.consumer_userid)).exists():
        consumer = Consumer.objects.get(
            account_id=request.session.get(ReqParams.consumer_userid))
        my_cart = Cart.objects.filter(
            account_id=consumer.account_id).order_by("-id")
        notifications = Notifications.objects.filter(
            consumer_id = request.session.get(ReqParams.consumer_userid)).order_by('-id')[:15]
    else:
        my_cart = Cart.objects.filter(account_id=request.session.get(
            ReqParams.ANONYMOUS_KEY)).order_by("-id")

    attr_list = []
    opt_list = []
    variants = []
    attributes = Product_Attributes.objects.filter(product_id=id)
    if attributes:
        for attr in attributes:
            attr_list.append(attr)
            opt_list.append(
                Product_Attributes_Option.objects.filter(attribute_id=attr.id))
        variants = zip(attr_list, opt_list)

    return render(request, "menu.html", {"ReqParams": ReqParams, "consumer": consumer, "product": product, "variants": variants, "my_cart": my_cart, "product_image": product_image,"notifications":notifications})


def Cart_Items_Page(request):

    retval = []
    cart_key = None
    cart = []
    cart_key_dict = []
    variants = []
    consumer = None
    notifications = None
    if request.session.get(ReqParams.consumer_userid):
        notifications = Notifications.objects.filter(consumer_id = request.session.get(ReqParams.consumer_userid)).order_by('-id')[:15]
        id = request.session.get(ReqParams.consumer_userid)
        consumer = Consumer.objects.get(account_id=id)
        cart_key = Cart_Key.objects.filter(account_id=consumer.account_id)

        for key in cart_key:
            if Cart.objects.filter(cart_key=key.id).exists():
                temp = []
                for obj in Cart.objects.filter(cart_key=key.id):
                    product = Products.objects.get(pk=obj.product_id)
                    varation_id = None
                    variation_name = None
                    variation_options = None

                    attributes = Product_Attributes.objects.filter(
                        product_id=product.product_id)

                    context = {}
                    context1 = {}
                    if attributes:
                        for attr in attributes:
                            options = Product_Attributes_Option.objects.filter(
                                attribute_id=attr.id)
                            temp_dict = {}
                            context1[attr.id] = attr.attribute_name
                            for opt in options:
                                temp_dict[opt.id] = opt.option_name
                            context[attr.attribute_name] = temp_dict

                    if Product_Variations.objects.filter(pk=obj.variation_id).exists():
                        this_variant = Product_Variations.objects.get(
                            pk=obj.variation_id)
                        varation_id = this_variant.id
                        variation_name = this_variant.options_name
                        variation_options = this_variant.option_id
                    product_image = product.default_image
                    if obj.product_image:
                        product_image = obj.product_image
                    temp.append(
                        {
                            "id": obj.id,
                            "product_id": obj.product_id,
                            "product_name": product.product_name,
                            "product_image": product_image,
                            "quantity": obj.quantity,
                            "total": obj.total,
                            "price": obj.price,
                            "variation_id": varation_id,
                            "variation_name": variation_name,
                            "variation_options": variation_options,
                            "options": context,
                            "attributes": context1

                        }

                    )
                cart.append(
                    temp
                )
                store = Store_Info.objects.get(store_id=key.store_id)
                cart_key_dict.append({
                    "id": key.id,
                    "store_name": store.store_name,
                    "store_image": store.profile_pic,
                    "store_id": store.store_id,
                    "store_link":store.store_link,
                }
                )
        retval = zip(cart_key_dict, cart)
    else:
        id = request.session.get(ReqParams.ANONYMOUS_KEY)
        cart_key = Cart_Key.objects.filter(account_id=id)

        for key in cart_key:
            if Cart.objects.filter(cart_key=key.id).exists():
                temp = []
                for obj in Cart.objects.filter(cart_key=key.id):
                    product = Products.objects.get(pk=obj.product_id)
                    varation_id = None
                    variation_name = None
                    variation_options = None

                    attributes = Product_Attributes.objects.filter(
                        product_id=product.product_id)

                    context = {}
                    context1 = {}
                    if attributes:
                        for attr in attributes:
                            options = Product_Attributes_Option.objects.filter(
                                attribute_id=attr.id)
                            temp_dict = {}
                            context1[attr.id] = attr.attribute_name
                            for opt in options:
                                temp_dict[opt.id] = opt.option_name
                            context[attr.attribute_name] = temp_dict

                    if Product_Variations.objects.filter(pk=obj.variation_id).exists():
                        this_variant = Product_Variations.objects.get(
                            pk=obj.variation_id)
                        varation_id = this_variant.id
                        variation_name = this_variant.options_name
                        variation_options = this_variant.option_id
                    product_image = product.default_image
                    if obj.product_image:
                        product_image = obj.product_image
                    temp.append(
                        {
                            "id": obj.id,
                            "product_id": obj.product_id,
                            "product_name": product.product_name,
                            "product_image": product_image,
                            "quantity": obj.quantity,
                            "total": obj.total,
                            "price": obj.price,
                            "variation_id": varation_id,
                            "variation_name": variation_name,
                            "variation_options": variation_options,
                            "options": context,
                            "attributes": context1

                        }

                    )
                cart.append(
                    temp
                )
                store = Store_Info.objects.get(store_id=key.store_id)
                cart_key_dict.append({
                    "id": key.id,
                    "store_name": store.store_name,
                    "store_image": store.profile_pic,
                    "store_id": store.store_id,
                    "store_link":store.store_link,
                }
                )

        retval = zip(cart_key_dict, cart)

    if request.method == "POST":
        checkout_list = []
        for key in cart_key:
            if request.POST.get("group_order_key" + str(key.id)):
                this_keys = request.POST.get("group_order_key" + str(key.id))
                checkout_list.append({
                    "value": this_keys
                })

        request.session[ReqParams.CHECKOUT_ITEMS] = json.dumps(checkout_list)
        return HttpResponseRedirect("/checkout")

    consumer = None
    my_cart = None
    if Consumer.objects.filter(account_id=request.session.get(ReqParams.consumer_userid)).exists():
        consumer = Consumer.objects.get(
            account_id=request.session.get(ReqParams.consumer_userid))
        my_cart = Cart.objects.filter(
            account_id=consumer.account_id).order_by("-id")
    else:
        my_cart = Cart.objects.filter(account_id=request.session.get(
            ReqParams.ANONYMOUS_KEY)).order_by("-id")

    return render(request, "cart_items.html", {"ReqParams": ReqParams, "consumer": consumer, "retval": retval, "cart_key": cart_key, "my_cart": my_cart,"notifications":notifications})





def Featured_Items(request):

    consumer = None
    my_cart = None
    notifications = None
    if Consumer.objects.filter(account_id=request.session.get(ReqParams.consumer_userid)).exists():
        consumer = Consumer.objects.get(
            account_id=request.session.get(ReqParams.consumer_userid))
        my_cart = Cart.objects.filter(
            account_id=consumer.account_id).order_by("-id")
        notifications = Notifications.objects.filter(
            consumer_id = request.session.get(ReqParams.consumer_userid)).order_by('-id')[:15]
    else:
        my_cart = Cart.objects.filter(account_id=request.session.get(
            ReqParams.ANONYMOUS_KEY)).order_by("-id")

    return render(request, "featured_items.html", {"ReqParams": ReqParams, "consumer": consumer, "my_cart": my_cart,"notifications":notifications})


def TrackingPage(request):

    consumer = None
    my_cart = None
    notifications = None
    if Consumer.objects.filter(account_id=request.session.get(ReqParams.consumer_userid)).exists():
        consumer = Consumer.objects.get(
            account_id=request.session.get(ReqParams.consumer_userid))
        my_cart = Cart.objects.filter(
            account_id=consumer.account_id).order_by("-id")
        notifications = Notifications.objects.filter(
            consumer_id = request.session.get(ReqParams.consumer_userid)).order_by('-id')[:15]
    else:
        my_cart = Cart.objects.filter(account_id=request.session.get(
            ReqParams.ANONYMOUS_KEY)).order_by("-id")

    return render(request, 'tracking.html', {"ReqParams": ReqParams, "consumer": consumer, "my_cart": my_cart,"notifications":notifications})


def CouponsPage(request):

    consumer = None
    my_cart = None
    notifications = None
    if Consumer.objects.filter(account_id=request.session.get(ReqParams.consumer_userid)).exists():
        consumer = Consumer.objects.get(
            account_id=request.session.get(ReqParams.consumer_userid))
        my_cart = Cart.objects.filter(
            account_id=consumer.account_id).order_by("-id")
        notifications = Notifications.objects.filter(
            consumer_id = request.session.get(ReqParams.consumer_userid)).order_by('-id')[:15]
    else:
        my_cart = Cart.objects.filter(account_id=request.session.get(
            ReqParams.ANONYMOUS_KEY)).order_by("-id")

    return render(request, "coupons.html", {"ReqParams": ReqParams, "consumer": consumer, "my_cart": my_cart,"notifications":notifications})


def RewardsPage(request):

    consumer = None
    my_cart = None
    notifications = None
    if Consumer.objects.filter(account_id=request.session.get(ReqParams.consumer_userid)).exists():
        consumer = Consumer.objects.get(
            account_id=request.session.get(ReqParams.consumer_userid))
        my_cart = Cart.objects.filter(
            account_id=consumer.account_id).order_by("-id")
        notifications = Notifications.objects.filter(
            consumer_id = request.session.get(ReqParams.consumer_userid)).order_by('-id')[:15]
    else:
        my_cart = Cart.objects.filter(account_id=request.session.get(
            ReqParams.ANONYMOUS_KEY)).order_by("-id")

    return render(request, "rewards.html", {"ReqParams": ReqParams, "consumer": consumer, "my_cart": my_cart,"notifications":notifications})


def MyPurchase_Page(request):

    if ReqParams.consumer_userid not in request.session:
        return HttpResponseRedirect("/")
    accid = request.session.get(ReqParams.consumer_userid)
    notifications = Notifications.objects.filter(consumer_id = accid).order_by('-id')[:15]
    retval = []
    orders = []
    products = []
    Pending = Orders.objects.filter(account_id=accid,order_status="Pending",service_flag = 1).order_by("-order_id")
    Preparing = Orders.objects.filter(account_id=accid,order_status="Preparing",service_flag = 1).order_by("-order_id")
    Prepared = Orders.objects.filter(account_id=accid,order_status="Prepared",service_flag = 1).order_by("-order_id")
    Completed = Orders.objects.filter(account_id=accid,order_status="Completed",service_flag = 1).order_by("-order_id")
    Cancelled = Orders.objects.filter(account_id=accid,order_status="Cancelled",service_flag = 1).order_by("-order_id")
    my_orders = Orders.objects.filter(account_id=accid).order_by("-order_id")
    all_discounts = Discount_Personnel.objects.all()
    for order in my_orders:

        store = None
        if Store_Info.objects.filter(pk=order.store_id).exists():
            store = Store_Info.objects.get(pk=order.store_id)
            print(order.id_format)
            orders.append({
                "order_id": order.order_id,
                "order_status":order.order_status,
                "discounted_flag":order.discounted_flag,
                "qr_code": order.qr_code,
                "total": order.total,
                "store_id": store.store_id,
                "store_image": store.profile_pic,
                "store_link": store.store_link,
                "store_name": store.store_name,
                "id_format": order.id_format,
            })

        else:
            orders.append({
                "order_id": 0,
            })

        line_items = Line_Items.objects.filter(order_id=order.order_id)
        temp = []
        for item in line_items:
            product = None
            if Products.objects.filter(pk=item.product_id).exists():
                product = Products.objects.get(pk=item.product_id)
            if product:
                variation = ""
                price = product.original_price
                if item.variation_id:
                    if Product_Variations.objects.filter(pk=item.variation_id).exists():
                        this_varation = Product_Variations.objects.get(
                            pk=item.variation_id)
                        variation = this_varation.options_name
                        price = this_varation.price
                        total = price * item.quantity
                    temp.append({

                        "product_id": product.product_id,
                        "image": product.default_image,
                        "quantity": item.quantity,
                        "product_name": product.product_name,
                        "price": price,
                        "total": total,
                        "varation_name": variation

                    })
                else:
                    total = price * item.quantity
                    temp.append({

                        "product_id": product.product_id,
                        "image": product.default_image,
                        "quantity": item.quantity,
                        "product_name": product.product_name,
                        "price": price,
                        "total": total,
                        "varation_name": ""

                    })

        products.append(temp)
    retval = zip(orders, products)

    consumer = None
    my_cart = None
    if Consumer.objects.filter(account_id=request.session.get(ReqParams.consumer_userid)).exists():
        consumer = Consumer.objects.get(
            account_id=request.session.get(ReqParams.consumer_userid))
        my_cart = Cart.objects.filter(
            account_id=consumer.account_id).order_by("-id")
    else:
        my_cart = Cart.objects.filter(account_id=request.session.get(
            ReqParams.ANONYMOUS_KEY)).order_by("-id")

    return render(request, "my_purchases.html", {"ReqParams": ReqParams, "consumer": consumer, "my_cart": my_cart, "products": products, "retval": retval,"notifications":notifications,
                                                 "all_discounts":all_discounts,"Pending":Pending,"Preparing":Preparing,"Prepared":Prepared,"Completed":Completed,"Cancelled":Cancelled})


def Notification_Page(request):

    if ReqParams.consumer_userid not in request.session:
        return HttpResponseRedirect("/")
    accid = request.session.get(ReqParams.consumer_userid)
    notifications = Notifications.objects.filter(consumer_id = accid).order_by('-id')[:15]

    consumer = None
    my_cart = None
    if Consumer.objects.filter(account_id=request.session.get(ReqParams.consumer_userid)).exists():
        consumer = Consumer.objects.get(
            account_id=request.session.get(ReqParams.consumer_userid))
        my_cart = Cart.objects.filter(
            account_id=consumer.account_id).order_by("-id")
    else:
        my_cart = Cart.objects.filter(account_id=request.session.get(
            ReqParams.ANONYMOUS_KEY)).order_by("-id")

    return render(request, "notifications.html", {"ReqParams": ReqParams, "consumer": consumer, "my_cart": my_cart,"notifications":notifications})

def Add_To_Order_ModalPage(request):

    if ReqParams.ANONYMOUS_KEY not in request.session:
        request.session[ReqParams.ANONYMOUS_KEY] = get_random_string(length=32)

    search_store = request.GET.get('search')

    if search_store:
        stores = Store_Info.objects.filter(
            Q(store_name__icontains=search_store))
    else:
        # If not searched, return default posts
        stores = Store_Info.objects.all().order_by("-store_id")
    
    products = Products.objects.filter(
        is_archived=False, display_flag=1, is_available=1)

    # product_image = []
    # for product in products:
    #     product_image.append(Product_Images.objects.filter(product_id=product.product_id))

    consumer = None
    my_cart = None
    notifications = None
    if Consumer.objects.filter(account_id=request.session.get(ReqParams.consumer_userid)).exists():
        consumer = Consumer.objects.get(
            account_id=request.session.get(ReqParams.consumer_userid))
        my_cart = Cart.objects.filter(
            account_id=consumer.account_id).order_by("-id")
        notifications = Notifications.objects.filter(
            consumer_id = request.session.get(ReqParams.consumer_userid)).order_by('-id')[:15]
    else:
        my_cart = Cart.objects.filter(account_id=request.session.get(
            ReqParams.ANONYMOUS_KEY)).order_by("-id")

    # attr_list = []
    # opt_list = []
    retval = []
    #variants = []
    for product in products:
        attributes = Product_Attributes.objects.filter(
            product_id=product.product_id)
        if attributes:
            attr_temp = []
            opt_temp = []
            for attr in attributes:
                attr_temp.append(attr)
                opt_temp.append(
                    Product_Attributes_Option.objects.filter(attribute_id=attr.id))
            this_variant = zip(attr_temp, opt_temp)
            retval.append({
                "product_id": product.product_id,
                "default_image": product.default_image,
                "product_name": product.product_name,
                "available_flag": product.available_flag,
                "status_type": product.status_type,
                "stock": product.stock,
                "description": product.description,
                "variants": this_variant,
                "original_price": product.original_price,
                "images": Product_Images.objects.filter(product_id=product.product_id)

            })
        else:
            retval.append({
                "product_id": product.product_id,
                "default_image": product.default_image,
                "product_name": product.product_name,
                "available_flag": product.available_flag,
                "status_type": product.status_type,
                "description": product.description,
                "stock": product.stock,
                "variants": [],
                "original_price": product.original_price,
                "images": Product_Images.objects.filter(product_id=product.product_id)
            })
    return render(request, "add_to_order_modal.html", {"ReqParams": ReqParams, "consumer": consumer,
                                           "stores": stores, "products": products, "my_cart": my_cart, "retval": retval,"notifications":notifications})

def Display_Share_OrderPage(request,id):
    
    retval = []
    orders = []
    products = []
    order = Orders.objects.get(pk = id)
    if order.shared_to:
        this_id = StringTolist(order.shared_to,",")
        if str(request.session.get(ReqParams.consumer_userid)) not in this_id or order.order_status != "Pending":
           
            return HttpResponseRedirect("/error_page")
    else:
        return HttpResponseRedirect("/error_page")
    
    store = None
    if Store_Info.objects.filter(pk=order.store_id).exists():
        store = Store_Info.objects.get(pk=order.store_id)
        orders.append({
            "order_id": order.order_id,
            "qr_code": order.qr_code,
            "total": order.total,
            "store_id": store.store_id,
            "store_link": store.store_link,
            "store_image": store.profile_pic,
            "store_name": store.store_name,
            "total": order.total,
            "id_format": order.id_format,
        })

    else:
        orders.append({
            "order_id": 0,
        })

    line_items = Line_Items.objects.filter(order_id=order.order_id)
    temp = []
    for item in line_items:
        product = None
        if Products.objects.filter(pk=item.product_id).exists():
            product = Products.objects.get(pk=item.product_id)
        if product:
            variation = ""
            price = product.original_price
            if item.variation_id:
                if Product_Variations.objects.filter(pk=item.variation_id).exists():
                    this_varation = Product_Variations.objects.get(
                        pk=item.variation_id)
                    variation = this_varation.options_name
                    price = this_varation.price
                    total = price * item.quantity
                temp.append({

                    "product_id": product.product_id,
                    "image": product.default_image,
                    "quantity": item.quantity,
                    "product_name": product.product_name,
                    "price": price,
                    "total": total,
                    "varation_name": variation

                })
            else:
                total = price * item.quantity
                temp.append({

                    "product_id": product.product_id,
                    "image": product.default_image,
                    "quantity": item.quantity,
                    "product_name": product.product_name,
                    "price": price,
                    "total": total,
                    "varation_name": ""

                })

    products.append(temp)
    retval = zip(orders, products)

    consumer = None
    my_cart = None
    notifications = None
    if Consumer.objects.filter(account_id=request.session.get(ReqParams.consumer_userid)).exists():
        consumer = Consumer.objects.get(
            account_id=request.session.get(ReqParams.consumer_userid))
        my_cart = Cart.objects.filter(
            account_id=consumer.account_id).order_by("-id")
        notifications = Notifications.objects.filter(
            consumer_id = request.session.get(ReqParams.consumer_userid)).order_by('-id')[:15]
    else:
        my_cart = Cart.objects.filter(account_id=request.session.get(
            ReqParams.ANONYMOUS_KEY)).order_by("-id")


    return render(request, "display_share_order.html", {"ReqParams": ReqParams, "consumer": consumer, "my_cart": my_cart, "products": products, "retval": retval,"order":order,"notifications":notifications})

def request_shared_order(request,id):
    notification = Notifications.objects.get(pk = id)
    order = Orders.objects.get(pk = notification.order_id)
    return render(request,"view_request_share_order",{"order":order,"notification":notification})

def Store_Feature_Page(request):

    consumer = None
    my_cart = None
    notifications = None
    if Consumer.objects.filter(account_id=request.session.get(ReqParams.consumer_userid)).exists():
        consumer = Consumer.objects.get(
            account_id=request.session.get(ReqParams.consumer_userid))
        my_cart = Cart.objects.filter(
            account_id=consumer.account_id).order_by("-id")
        notifications = Notifications.objects.filter(
            consumer_id = request.session.get(ReqParams.consumer_userid)).order_by('-id')[:15]
    else:
        my_cart = Cart.objects.filter(account_id=request.session.get(
            ReqParams.ANONYMOUS_KEY)).order_by("-id")

    return render(request, 'store_feature.html', {"ReqParams": ReqParams, "consumer": consumer, "my_cart": my_cart,"notifications":notifications})


def User_Profile_Page(request):
    context = {
        "error_msg": "",
        "success_msg": ""
    }
    # Get the current user's Consumer object
    user = Consumer.objects.get(
        account_id=request.session.get(ReqParams.consumer_userid))
    if request.method == 'POST':
        # Update the user's information
        user.user_name = request.POST['user_name']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.phone_number1 = request.POST['phone_number']
        user.address = request.POST['address']
        this_random = generate_random()
        if 'profile_picture' in request.FILES:
            upload_profilepic_image(request.FILES.get(
                "profile_picture"), user.account_id, this_random)
            user.profile_picture = str(
                user.account_id) + "." + str(this_random) + ".jpg"
        user.save()
        # Show a success message to the user
        messages.success(request, "Profile updated successfully")
        return redirect('/user_profile')
    
    consumer = None
    my_cart = None
    notifications = None
    if Consumer.objects.filter(account_id=request.session.get(ReqParams.consumer_userid)).exists():
        consumer = Consumer.objects.get(
            account_id=request.session.get(ReqParams.consumer_userid))
        my_cart = Cart.objects.filter(
            account_id=consumer.account_id).order_by("-id")
        notifications = Notifications.objects.filter(
            consumer_id = request.session.get(ReqParams.consumer_userid)).order_by('-id')[:15]
    else:
        my_cart = Cart.objects.filter(account_id=request.session.get(
            ReqParams.ANONYMOUS_KEY)).order_by("-id")

    return render(request, "user_profile.html", {"ReqParams": ReqParams, "user": user, "consumer": consumer, "context": context, "my_cart": my_cart,"notifications":notifications})

def loading_spinner(request):
    
    return render(request, 'loading_spinner.html', {"ReqParams": ReqParams})


def LogoutPage(request):
    if ReqParams.consumer_userid in request.session:
        del request.session[ReqParams.consumer_userid]
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return HttpResponseRedirect("/login")




