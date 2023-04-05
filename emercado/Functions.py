from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from .EmercadoDB import *
from .EmercadoUtil import *
from .models import *
import json
from django.shortcuts import redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.conf import settings
import random
import string
import itertools
import ast
from django.utils.crypto import get_random_string
import qrcode
from io import BytesIO
from PIL import Image
from django.http import HttpResponse
from random import randint
import base64
from datetime import datetime, timedelta
from datetime import date
from geopy.geocoders import Nominatim

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


def generates_qr_code(id_format):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(id_format)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')

    # Save the image to a buffer
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    return buffer

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

def generate_account_id():
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


def generate_product_id():
    n = 15
    does_exists = 1
    retval = ""
    while does_exists == 1:
        obj = ''.join(random.choice(string.digits) for num in range(n))
        if Products.objects.filter(pk=obj).exists():
            does_exists = 1
        else:
            retval = obj
            does_exists = 0

    return retval

def generate_order_id():
    n = 15
    does_exists = 1
    retval = ""
    while does_exists == 1:
        obj = ''.join(random.choice(string.digits) for num in range(n))
        if Orders.objects.filter(pk=obj).exists():
            does_exists = 1
        else:
            retval = obj
            does_exists = 0

    return retval

def generate_random():
    n = 7
    obj = ''.join(random.choice(string.digits) for num in range(n))
    return obj


def owner_signup(request):

    # if request.method == "POST":
    #     new_owner = Store_Info()
    #     new_owner.account_id = generate_account_id()
    #     new_owner.email = request.POST.get(ReqParams.email_address)
    #     new_owner.first_name = request.POST.get(ReqParams.firstname)
    #     new_owner.last_name = request.POST.get(ReqParams.lastname)
    #     new_owner.address = request.POST.get(ReqParams.address)
    #     new_owner.phone_number1 = request.POST.get(ReqParams.phone_number1)
    #     new_owner.phone_number2 = request.POST.get(ReqParams.phone_number2)
    #     new_owner.user_name = request.POST.get(ReqParams.user_name)

    #     password = request.POST["password"]
    #     # convertion into base64
    #     passAscii = password.encode("ascii")
    #     passBytes = base64.b64encode(passAscii)
    #     new_owner.password = passBytes
    #     new_owner.save()
    #     messages.success(request, "Store Owner Successfully Registered")

    #     return HttpResponseRedirect("/seller/login")
    return render(request, "store/Store_Info_signup.html", {"ReqParams": ReqParams})

def add_new_store(request):

    # if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
    #     return HttpResponseRedirect("/page_not_found")

    # owner = Store_Info.objects.filter(
    #     account_id=request.session.get(ReqParams.owner_userid))

    # if request.method == "POST":
    #     store = Store_Info()
    #     seller = Store_Info.objects.get(
    #         pk=request.session.get(ReqParams.owner_userid))
    #     store.store_id = generate_store_id()
    #     store.store_name = request.POST.get(ReqParams.store_name)
    #     store.branch_name = request.POST.get(ReqParams.branch_name)
    #     store.store_address1 = request.POST.get(ReqParams.address1)
    #     store.store_address2 = request.POST.get(ReqParams.address2)
    #     store.store_category = request.POST.get(ReqParams.category)
    #     store.owner_id = seller
    #     store.store_link = settings.URL_SITE_DOMAIN + "/store_id/" + store.store_id
    #     store.phone_number = request.POST.get(ReqParams.phonenumber)
    #     store.email_address = request.POST.get(ReqParams.email_address)
    #     this_random = generate_random()
    #     upload_storepic_image(request.FILES.get(
    #         "profile_pic"), store.store_id, this_random)
    #     store.profile_pic = store.store_id + "." + this_random + ".jpg"
    #     store.save()
    #     return HttpResponseRedirect("/seller/dashboard")

    return render(request, "store/add_new_store.html", {"ReqParams": ReqParams,  })


def merchant_login(request):
    default_username = ""
    if request.session.get("user_name"):
        default_username = request.session.get("user_name")
    context = {
        "userid": default_username,
        "error_msg": "",
        "success_msg": ""
    }

    if request.method == "POST":
        # we check weither user uses email or user name
        if Store_Info.objects.filter(email_address=request.POST['userid']).exists():
            this_email = request.POST['userid']
            context["userid"] = request.POST['userid']
            this_user = Store_Info.objects.get(email_address=this_email)
            password = request.POST["password"]
            # convertion into base64
            passAscii = password.encode("ascii")
            passBytes = base64.b64encode(passAscii)
            if this_user.password == passBytes:
                # success login

                # we used this session/ cookie value to call data from other table
                # it is also going to be used to check if an user has been login
                request.session[ReqParams.owner_userid] = this_user.store_id
                return HttpResponseRedirect("/seller/orders/orders_list/dine_in_tile")
            else:
                context["error_msg"] = "Invalid Credentials!"
                return render(request, "store/login.html", {"ReqParams": ReqParams, "context": context})
        elif Store_Info.objects.filter(user_name=request.POST['userid']).exists():
            this_username = request.POST['userid']
            context["userid"] = request.POST['userid']
            this_user = Store_Info.objects.get(user_name=this_username)
            password = request.POST["password"]
            # convertion into base64
            passAscii = password.encode("ascii")
            passBytes = base64.b64encode(passAscii)
            if this_user.password == passBytes:
                # success login

                # we used this session/ cookie value to call data from other table
                # it is also going to be used to check if an user has been login
                request.session[ReqParams.owner_userid] = this_user.store_id
                return HttpResponseRedirect("/seller/orders/orders_list/dine_in_tile")
            else:
                context["error_msg"] = "Invalid Credentials!"
                return render(request, "store/login.html", {"ReqParams": ReqParams, "context": context})
        else:
            context["userid"] = request.POST['userid']
            context["error_msg"] = "Invalid Credentials!"
            return render(request, "store/login.html", {"ReqParams": ReqParams, "context": context})

    return render(request, "store/login.html", {"ReqParams": ReqParams, "context": context})


def page_not_found(request):

    return render(request, "store/page_not_found.html", {"ReqParams": ReqParams})


def dashboard(request):

    # if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
    #     return HttpResponseRedirect("/page_not_found")

    # my_stores = Store_Info.objects.filter(
    #     owner_id=request.session.get(ReqParams.owner_userid))

    # id = request.session.get(ReqParams.owner_userid)

    # my_stores = Store_Info.objects.filter(owner_id=id)
    # owner = Store_Info.objects.filter(account_id=id)
    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]
    return render(request, "store/dashboard.html", {"all_notifications":all_notifications})



def product_details(request, id):

    if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
        return HttpResponseRedirect("/page_not_found")

    product = Products.objects.get(product_id=id)
    attr_opt = []
    product_attributes = Product_Attributes.objects.filter(product_id=id)
    for obj in product_attributes:
        this_option = Product_Attributes_Option.objects.filter(
            attribute_id=obj.id)
        temp = ""
        for option in this_option:
            temp += option.option_name + ","
        attr_opt.append(
            {
                "attr_name": obj.attribute_name,
                "opt_name": temp,
                "id": obj.id
            }
        )

    product_variants = Product_Variations.objects.filter(product_id=id)
    owner = Store_Info.objects.get(store_id=request.session.get(
        ReqParams.owner_userid, "product_attributes"))

    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]

    return render(request, "store/product_details.html", {"ReqParams": ReqParams, "owner": owner, "product": product, "attr_opt": attr_opt, "product_attributes": product_attributes, "product_variants": product_variants,
                                                          "all_notifications":all_notifications})


def Order_Dine_In_List(request):

    if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
        return HttpResponseRedirect("/page_not_found")

    id = request.session.get(ReqParams.owner_userid)
    this_store = Store_Info.objects.get(store_id=id)

    owner = Store_Info.objects.get(
        store_id=request.session.get(ReqParams.owner_userid))

    request.session[ReqParams.store_id] = id
    Pending = Orders.objects.filter(store_id = id,order_status="Pending",service_flag = 2)
    Preparing = Orders.objects.filter(store_id = id,order_status="Preparing",service_flag = 2)
    Prepared = Orders.objects.filter(store_id = id,order_status="Prepared",service_flag = 2)
    Completed = Orders.objects.filter(store_id = id,order_status="Completed",service_flag = 2)
    Cancelled = Orders.objects.filter(store_id = id,order_status="Cancelled",service_flag = 2)

    all_orders = Orders.objects.filter(store_id = id,service_flag = 2)
    retval = []
    for order in all_orders:
        temp = []
        for item in Line_Items.objects.filter(order_id = order.order_id):
            product = Products.objects.get(pk = item.product_id)
            variation = ""
            price = product.original_price
            if item.variation_id:
                this_varation = Product_Variations.objects.get(pk = item.variation_id)
                variation = this_varation.options_name
                price = this_varation.price
            total = price * item.quantity
            temp.append({
                "product_name":product.product_name,
                "product_id":product.product_id,
                "product_image":product.default_image,
                "variation":variation,
                "quantity":item.quantity,
                "price":price,
                "total":total
            })

        retval.append(
            {
                "name":order.fullname,
                "order_id":order.order_id,
                "email":order.email_address,
                "phone":order.phone,
                "total":order.total,
                "line_items":temp,
                "items":order.items,

            }
        )
    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]
    return render(request, "store/order_dine_in_list.html", {"ReqParams": ReqParams, "owner": owner, "this_store": this_store,"all_notifications":all_notifications,
                                                             "Pending":Pending,"Preparing":Preparing,"Prepared":Prepared,"Completed":Completed,"Cancelled":Cancelled,"all_orders":all_orders,"retval":retval})

def Order_Dine_In_Tile(request):

    if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
        return HttpResponseRedirect("/page_not_found")

    id = request.session.get(ReqParams.owner_userid)
    this_store = Store_Info.objects.get(store_id=id)

    owner = Store_Info.objects.get(
        store_id=request.session.get(ReqParams.owner_userid))

    request.session[ReqParams.store_id] = id
    Pending = Orders.objects.filter(store_id = id,order_status="Pending",service_flag = 2)
    Preparing = Orders.objects.filter(store_id = id,order_status="Preparing",service_flag = 2)
    Prepared = Orders.objects.filter(store_id = id,order_status="Prepared",service_flag = 2)
    Completed = Orders.objects.filter(store_id = id,order_status="Completed",service_flag = 2)
    Cancelled = Orders.objects.filter(store_id = id,order_status="Cancelled",service_flag = 2)

    all_orders = Orders.objects.filter(store_id = id,service_flag = 2)
    retval = []
    for order in all_orders:
        temp = []
        for item in Line_Items.objects.filter(order_id = order.order_id):
            product = Products.objects.get(pk = item.product_id)
            variation = ""
            price = product.original_price
            if item.variation_id:
                this_varation = Product_Variations.objects.get(pk = item.variation_id)
                variation = this_varation.options_name
                price = this_varation.price
            total = price * item.quantity
            temp.append({
                "product_name":product.product_name,
                "product_id":product.product_id,
                "product_image":product.default_image,
                "variation":variation,
                "quantity":item.quantity,
                "price":price,
                "total":total
            })

        retval.append(
            {
                "name":order.fullname,
                "order_id":order.order_id,
                "email":order.email_address,
                "phone":order.phone,
                "total":order.total,
                "line_items":temp,
                "items":order.items,

            }
        )

    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]
    return render(request, "store/order_dine_in_tile.html", {"ReqParams": ReqParams, "owner": owner, "this_store": this_store,"all_notifications":all_notifications,
                                                             "Pending":Pending,"Preparing":Preparing,"Prepared":Prepared,"Completed":Completed,"Cancelled":Cancelled,"all_orders":all_orders,"retval":retval})


def Order_Pick_Up_List(request):

    if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
        return HttpResponseRedirect("/page_not_found")

    id = request.session.get(ReqParams.owner_userid)
    this_store = Store_Info.objects.get(store_id=id)

    owner = Store_Info.objects.get(
        store_id=request.session.get(ReqParams.owner_userid))

    request.session[ReqParams.store_id] = id
    Pending = Orders.objects.filter(store_id = id,order_status="Pending",service_flag = 1)
    Preparing = Orders.objects.filter(store_id = id,order_status="Preparing",service_flag = 1)
    Prepared = Orders.objects.filter(store_id = id,order_status="Prepared",service_flag = 1)
    Completed = Orders.objects.filter(store_id = id,order_status="Completed",service_flag = 1)
    Cancelled = Orders.objects.filter(store_id = id,order_status="Cancelled",service_flag = 1)
    all_orders = Orders.objects.filter(store_id = id,service_flag = 1)
    retval = []
    for order in all_orders:
        temp = []
        for item in Line_Items.objects.filter(order_id = order.order_id):
            product = Products.objects.get(pk = item.product_id)
            variation = ""
            price = product.original_price
            if item.variation_id:
                this_varation = Product_Variations.objects.get(pk = item.variation_id)
                variation = this_varation.options_name
                price = this_varation.price
            total = price * item.quantity
            temp.append({
                "product_name":product.product_name,
                "product_id":product.product_id,
                "product_image":product.default_image,
                "variation":variation,
                "quantity":item.quantity,
                "price":price,
                "total":total
            })

        retval.append(
            {
                "name":order.fullname,
                "order_id":order.order_id,
                "email":order.email_address,
                "phone":order.phone,
                "total":order.total,
                "line_items":temp,
                "items":order.items,

            }
        )

    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]

    return render(request,"store/order_pick_up_list.html",{"ReqParams":ReqParams, "owner":owner, "this_store":this_store,"all_notifications":all_notifications,
                                                           "Pending":Pending,"Preparing":Preparing,"Prepared":Prepared,"Completed":Completed,"Cancelled":Cancelled,"all_orders":all_orders,"retval":retval})

def Order_Pick_Up_Tile(request):

    if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
        return HttpResponseRedirect("/page_not_found")

    id = request.session.get(ReqParams.owner_userid)
    this_store = Store_Info.objects.get(store_id=id)

    owner = Store_Info.objects.get(
        store_id=request.session.get(ReqParams.owner_userid))

    request.session[ReqParams.store_id] = id
    Pending = Orders.objects.filter(store_id = id,order_status="Pending",service_flag = 1)
    Preparing = Orders.objects.filter(store_id = id,order_status="Preparing",service_flag = 1)
    Prepared = Orders.objects.filter(store_id = id,order_status="Prepared",service_flag = 1)
    Completed = Orders.objects.filter(store_id = id,order_status="Completed",service_flag = 1)
    Cancelled = Orders.objects.filter(store_id = id,order_status="Cancelled",service_flag = 1)
    all_orders = Orders.objects.filter(store_id = id,service_flag = 1)
    retval = []
    for order in all_orders:
        temp = []
        for item in Line_Items.objects.filter(order_id = order.order_id):
            product = Products.objects.get(pk = item.product_id)
            variation = ""
            price = product.original_price
            if item.variation_id:
                this_varation = Product_Variations.objects.get(pk = item.variation_id)
                variation = this_varation.options_name
                price = this_varation.price
            total = price * item.quantity
            print(variation)
            temp.append({
                "product_name":product.product_name,
                "product_id":product.product_id,
                "product_image":product.default_image,
                "variation":variation,
                "quantity":item.quantity,
                "price":price,
                "total":total
            })

        retval.append(
            {
                "name":order.fullname,
                "profile_picture":order.profile_picture,
                "order_id":order.order_id,
                "email":order.email_address,
                "phone":order.phone,
                "total":order.total,
                "line_items":temp,
                "items":order.items,

            }
        )

    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]

    return render(request,"store/order_pick_up_tile.html",{"ReqParams":ReqParams, "owner":owner, "this_store":this_store,"all_notifications":all_notifications,
                                                           "Pending":Pending,"Preparing":Preparing,"Prepared":Prepared,"Completed":Completed,"Cancelled":Cancelled,"all_orders":all_orders,"retval":retval})

def Order_Delivery_List(request):

    if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
        return HttpResponseRedirect("/page_not_found")

    id = request.session.get(ReqParams.owner_userid)
    this_store = Store_Info.objects.get(store_id=id)

    owner = Store_Info.objects.get(
        store_id=request.session.get(ReqParams.owner_userid))

    request.session[ReqParams.store_id] = id
    Pending = Orders.objects.filter(store_id = id,order_status="Pending",service_flag = 3)
    Preparing = Orders.objects.filter(store_id = id,order_status="Preparing",service_flag = 3)
    Prepared = Orders.objects.filter(store_id = id,order_status="Prepared",service_flag = 3)
    Completed = Orders.objects.filter(store_id = id,order_status="Completed",service_flag = 3)
    Cancelled = Orders.objects.filter(store_id = id,order_status="Cancelled",service_flag = 3)
    all_orders = Orders.objects.filter(store_id = id,service_flag = 3)
    retval = []
    for order in all_orders:
        temp = []
        for item in Line_Items.objects.filter(order_id = order.order_id):
            product = Products.objects.get(pk = item.product_id)
            variation = ""
            price = product.original_price
            if item.variation_id:
                this_varation = Product_Variations.objects.get(pk = item.variation_id)
                variation = this_varation.options_name
                price = this_varation.price
            total = price * item.quantity

            temp.append({
                "product_name":product.product_name,
                "product_id":product.product_id,
                "product_image":product.default_image,
                "variation":variation,
                "quantity":item.quantity,
                "price":price,
                "total":total
            })

        retval.append(
            {
                "name":order.fullname,
                "order_id":order.order_id,
                "email":order.email_address,
                "phone":order.phone,
                "total":order.total,
                "line_items":temp,
                "items":order.items,

            }
        )

    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]

    return render(request,"store/order_delivery_list.html",{"ReqParams":ReqParams, "owner":owner, "this_store":this_store,"all_notifications":all_notifications,
                                                            "Pending":Pending,"Preparing":Preparing,"Prepared":Prepared,"Completed":Completed,"Cancelled":Cancelled,"all_orders":all_orders,"retval":retval})

def Order_Delivery_Tile(request):

    if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
        return HttpResponseRedirect("/page_not_found")

    id = request.session.get(ReqParams.owner_userid)
    this_store = Store_Info.objects.get(store_id=id)

    owner = Store_Info.objects.get(
        store_id=request.session.get(ReqParams.owner_userid))

    request.session[ReqParams.store_id] = id
    Pending = Orders.objects.filter(store_id = id,order_status="Pending",service_flag = 3)
    Preparing = Orders.objects.filter(store_id = id,order_status="Preparing",service_flag = 3)
    Prepared = Orders.objects.filter(store_id = id,order_status="Prepared",service_flag = 3)
    Completed = Orders.objects.filter(store_id = id,order_status="Completed",service_flag = 3)
    Cancelled = Orders.objects.filter(store_id = id,order_status="Cancelled",service_flag = 3)
    all_orders = Orders.objects.filter(store_id = id,service_flag = 3)
    retval = []
    for order in all_orders:
        temp = []
        for item in Line_Items.objects.filter(order_id = order.order_id):
            product = Products.objects.get(pk = item.product_id)
            variation = ""
            price = product.original_price
            if item.variation_id:
                this_varation = Product_Variations.objects.get(pk = item.variation_id)
                variation = this_varation.options_name
                price = this_varation.price
            total = price * item.quantity
            temp.append({
                "product_name":product.product_name,
                "product_id":product.product_id,
                "product_image":product.default_image,
                "variation":variation,
                "quantity":item.quantity,
                "price":price,
                "total":total
            })

        retval.append(
            {
                "name":order.fullname,
                "order_id":order.order_id,
                "email":order.email_address,
                "phone":order.phone,
                "total":order.total,
                "line_items":temp,
                "items":order.items,

            }
        )


    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]

    return render(request,"store/order_delivery_tile.html",{"ReqParams":ReqParams, "owner":owner, "this_store":this_store,"all_notifications":all_notifications,
                                                            "Pending":Pending,"Preparing":Preparing,"Prepared":Prepared,"Completed":Completed,"Cancelled":Cancelled,"all_orders":all_orders,"retval":retval})

def order_details(request, id):

    owner = Store_Info.objects.get(store_id=request.session.get(ReqParams.owner_userid))

    request.session[ReqParams.store_id] = id

    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]

    return render(request, "store/order_details.html", {"ReqParams": ReqParams, "owner":owner,"all_notifications":all_notifications})

def product_list(request):

    if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
        return HttpResponseRedirect("/page_not_found")

    id = request.session.get(ReqParams.owner_userid)
    store = Store_Info.objects.get(store_id=id)

    product = Products.objects.filter(store_id = store, is_archived=False)

    owner = Store_Info.objects.get(
        store_id=request.session.get(ReqParams.owner_userid))

    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]

    return render(request, "store/product_list.html", {"ReqParams": ReqParams, "owner": owner, "product": product,"all_notifications":all_notifications})

def discounted_product(request):

    if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
        return HttpResponseRedirect("/page_not_found")

    id = request.session.get(ReqParams.owner_userid)
    store = Store_Info.objects.get(store_id=id)

    product = Products.objects.filter(store_id = store, is_archived=False)

    owner = Store_Info.objects.get(
        store_id=request.session.get(ReqParams.owner_userid))

    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]

    return render(request, "store/discounted_products.html", {"ReqParams": ReqParams, "owner": owner, "product": product,"all_notifications":all_notifications})


def product_addons(request):

    if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
        return HttpResponseRedirect("/page_not_found")

    id = request.session.get(ReqParams.owner_userid)
    store = Store_Info.objects.get(store_id=id)

    product = Products.objects.filter(store_id = store, is_archived=False)

    owner = Store_Info.objects.get(
        store_id=request.session.get(ReqParams.owner_userid))

    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]

    return render(request, "store/product_addons.html", {"ReqParams": ReqParams, "owner": owner, "product": product,"all_notifications":all_notifications})


def product_archive(request):

    if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
        return HttpResponseRedirect("/page_not_found")

    id = request.session.get(ReqParams.owner_userid)
    store = Store_Info.objects.get(store_id=id)

    product = Products.objects.filter(store_id = store,is_archived=True)

    owner = Store_Info.objects.get(
        store_id=request.session.get(ReqParams.owner_userid))

    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]

    return render(request, "store/product_archive.html", {"ReqParams": ReqParams,  "product": product, "owner":owner,"all_notifications":all_notifications})


def archive_item(request, id):
    product = Products.objects.get(product_id=id)
    product.is_archived = True
    product.save()
    messages.success(request, 'Successfully Archive')
    return HttpResponseRedirect(f"/seller/my_store/product_archive")


def restore_item(request, id):
    product = Products.objects.get(product_id=id)
    product.is_archived = False
    product.save()
    messages.success(request, 'Successfully Restore')
    return HttpResponseRedirect(f"/seller/my_store/product_list")


def add_new_item(request):

    if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
        return HttpResponseRedirect("/page_not_found")

    owner = Store_Info.objects.get(
        store_id=request.session.get(ReqParams.owner_userid))

    id = request.session.get(ReqParams.owner_userid)
    store = Store_Info.objects.get(store_id=id)
    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]
    if request.method == "POST":
        new_item = Products()

        new_item.product_name = request.POST.get(ReqParams.name)
        new_item.description = request.POST.get(ReqParams.description)
        new_item.original_price = request.POST.get(ReqParams.price)
        new_item.product_category = request.POST.get(ReqParams.category)
        new_item.product_name = request.POST.get(ReqParams.name)
        new_item.store_id = store
        if request.POST.get(ReqParams.weight):
            new_item.weight = request.POST.get(ReqParams.weight)

        new_item.sku = request.POST.get(ReqParams.sku)
        new_item.status_type = request.POST.get(ReqParams.available_flag)
        if request.POST.get("display_product"):
            new_item.display_flag = 1

        if request.POST.get(ReqParams.available_flag) == "2":
            new_item.available_flag = 1
        else:
            new_item.stock = request.POST.get(ReqParams.stocks)
        new_item.save()
        if request.FILES.getlist(ReqParams.product_images):
            images = request.FILES.getlist(ReqParams.product_images)

            x = 0
            for file in images:
                file_name = file.name
                print(file_name.lstrip('.'))
                # all_image = Product_Images.objects.latest('id')
                product_image = Product_Images()
                product_image.product_id = new_item
                product_image.save()
                product_image.file_name = str(new_item.product_id) + "." + str(product_image.id) + ".jpg"
                product_image.save()
                upload_product_image(
                    file, str(new_item.product_id), str(product_image.id))
                if x == 0:
                    new_item.default_image = str(new_item.product_id)+ "." + str(product_image.id) + ".jpg"

                x += 1

        new_item.save()
        new_item.id_format = ID_FORMAT(new_item.product_id,"PROD")
        # qr_buffer = generate_qr_code(new_item.id_format, logo_image=Image.open(new_item.default_image))
        # # Save the QR code image to the Order model
        # new_item.qr_code.save(f'product_{new_item.id_format}.png', qr_buffer, save=True)
        new_item.save()
        attr_len = json.loads(request.POST.get("opt_len"))

        has_variation_flag = 0
        if attr_len:
            has_variation_flag = 1
            for key, value in attr_len.items():
                has_variation_flag += 1
                attributes = Product_Attributes()
                attributes.attribute_name = key
                attributes.product_id = new_item.product_id
                attributes.save()

                json_tags = json.loads(value)
                for tag in json_tags:
                    options = Product_Attributes_Option()
                    options.option_name = tag["value"]
                    options.attribute_id = attributes.id
                    options.save()

        add_ons = request.POST.get("add_ons_item")
        print(request.POST.get("add_ons_item"))
        if add_ons:
            add_ons_obj = json.loads(request.POST.get("add_ons_item"))
            for obj in add_ons_obj:
                product_add_ons = Product_AddOns()
                product_add_ons.product_name = obj["product_name"]
                product_add_ons.status_type = int(obj["status_type"])
                product_add_ons.price = float(obj["price"])
                if int(obj["status_type"]) == 2:
                    product_add_ons.available_flag = 1
                else:
                    if obj["stocks"]:
                        product_add_ons.stocks = int(obj["stocks"])
                    else:
                        product_add_ons.stocks = 0
                product_add_ons.product_id = new_item
                product_add_ons.save()

        this_attr = Product_Attributes.objects.filter(
            product_id=new_item.product_id)
        if this_attr:
            if len(this_attr) == 1:
                for attr in this_attr:
                    options_ids = Product_Attributes_Option.objects.filter(
                        attribute_id=attr.id)

                    for opt in options_ids:
                        variations = Product_Variations()
                        variations.option_id = str(opt.id) + ","
                        variations.options_name = opt.option_name
                        variations.product_id = new_item
                        variations.attribute_id = str(attr.id)
                        variations.status_type = request.POST.get(
                            ReqParams.available_flag)
                        if request.POST.get(ReqParams.available_flag) == 2:
                            variations.available_flag = 1
                        else:
                            variations.stocks = 0
                        variations.price = 0
                        variations.save()
            else:
                # we get all options
                all_options = []
                for attr in this_attr:
                    this_opt = Product_Attributes_Option.objects.filter(
                        attribute_id=attr.id)
                    temp = []
                    for opt in this_opt:
                        temp.append(str(opt.id))
                    all_options.append(temp)

                # we make all the combinations
                combinations = list(itertools.product(*all_options))

                # we make the variations
                for obj in combinations:
                    variations = Product_Variations()
                    for opt in obj:
                        this_opt = Product_Attributes_Option.objects.get(
                            pk=int(opt))
                        variations.option_id += opt + ","
                        variations.options_name += this_opt.option_name + "|"
                        variations.attribute_id += str(this_opt.id) + ","
                    variations.status_type = request.POST.get(
                        ReqParams.available_flag)
                    variations.product_id = new_item
                    if request.POST.get(ReqParams.available_flag) == 2:
                        variations.available_flag = 1
                    else:
                        variations.stocks = 0
                    variations.price = 0
                    variations.save()

        if has_variation_flag != 0:
            return HttpResponseRedirect(f"/seller/setup_variations/product_id={new_item.product_id}")
        else:
            return HttpResponseRedirect(f"/seller/my_store/product_list")

    return render(request, "store/add_new_item.html", {"ReqParams": ReqParams, "id": id, "owner": owner,"all_notifications":all_notifications})


def setup_variations(request, id):
    if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
        return HttpResponseRedirect("/page_not_found")

    this_store = Store_Info.objects.get(pk= request.session.get(ReqParams.owner_userid))
    oid = request.session.get(ReqParams.owner_userid)

    owner = Store_Info.objects.get(store_id=oid)
    product = Products.objects.get(pk=id)
    retval = Product_Variations.objects.filter(product_id=id)
    product_images = Product_Images.objects.filter(product_id=id)

    print()
    if str(this_store.store_id) != str(product.store_id_id):
        return HttpResponseRedirect("/page_not_found")

    if request.method == "POST":
        for variant in retval:
            print(request.POST.get("available_flag" + str(variant.id)))
            variant.price = request.POST.get("price" + str(variant.id))
            variant.status_type = int(request.POST.get(
                "available_flag" + str(variant.id)))
            if int(request.POST.get("available_flag" + str(variant.id))) == 2:
                variant.available_flag = 1
            else:
                variant.stocks = int(request.POST.get(
                    "stocks" + str(variant.id)))
            variant.image = request.POST.get(
                "image_for_variant" + str(variant.id))
            variant.save()
        return HttpResponseRedirect("/seller/my_store/product_list")
    return render(request, "store/variations_setup.html", {"ReqParams": ReqParams, "owner": owner,"retval": retval, "product_images": product_images, "id": id, "this_store": this_store,  "product": product})


def check_email_seller(request):
    context = {}

    # if request.method == "POST":
    #     this_email = request.POST["value"]
    #     if Store_Info.objects.filter(email=this_email).exists():
    #         context["success"] = 1
    #     else:
    #         context["success"] = 0

    return HttpResponse(json.dumps(context), "application/json")


def check_username_seller(request):
    context = {}

    # if request.method == "POST":
    #     this_value = request.POST["value"]
    #     if Store_Info.objects.filter(user_name=this_value).exists():
    #         context["success"] = 1
    #     else:
    #         context["success"] = 0

    return HttpResponse(json.dumps(context), "application/json")


def profile(request):

    context = {
        "error_msg": "",
        "success_msg": ""
    }

    if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
        return HttpResponseRedirect("/page_not_found")

    id = request.session.get(ReqParams.owner_userid)
    store = Store_Info.objects.get(store_id=id)

    owner = Store_Info.objects.get(
        store_id=request.session.get(ReqParams.owner_userid))

    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]

    # Get the current user's Merchant object
    merchant = Store_Info.objects.get(
        store_id=request.session.get(ReqParams.owner_userid))
    if request.method == 'POST':
        # Update the user's information
        merchant.user_name = request.POST['user_name']
        merchant.first_name = request.POST['first_name']
        merchant.last_name = request.POST['last_name']
        merchant.email_address= request.POST['email_address']
        merchant.phone_number = request.POST['phone_number']
        merchant.store_address1 = request.POST['store_address1']
        merchant.store_name = request.POST['store_name']
        merchant.store_category = request.POST['store_category']
        merchant.store_phone_number = request.POST['store_phone_number']
        merchant.save()
        # merchant.store_address2 = request.POST['store_address2']
        store_street = request.POST.get("store_street")
        store_city = request.POST.get("store_city")
        store_state = request.POST.get("store_state")
        store_postal_code = request.POST.get("store_postal_code")
        store_country = request.POST.get("store_country")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        # Check if latitude and longitude are not empty
        if latitude and longitude:
            merchant.latitude = float(latitude)
            merchant.longitude = float(longitude)
            # initialize Nominatim API
            geolocator = Nominatim(user_agent="geoapiExercises")
            # using reverse() to get the address of the location
            location = geolocator.reverse(f"{latitude},{longitude}")
            if location is not None:
                merchant.store_address2 = location.address
        else:
            merchant.store_address2 = f"{store_street}, {store_city}, {store_state}, {store_postal_code}, {store_country}"
            geolocator = Nominatim(user_agent='geoapiExercises')
            location = geolocator.geocode(merchant.store_address2)
            if location is not None:
                merchant.latitude = location.latitude
                merchant.longitude = location.longitude

        this_random = generate_random()
        if 'profile_picture' in request.FILES:
            upload_profilepicture_image(request.FILES.get(
                "profile_picture"), merchant.store_id, this_random)
            merchant.profile_picture = str(
                merchant.store_id) + "." + str(this_random) + ".jpg"

        this_random = generate_random()
        if 'profile_pic' in request.FILES:
            upload_profilepic_image(request.FILES.get(
                "profile_pic"), merchant.store_id, this_random)
            merchant.profile_pic = str(
                merchant.store_id) + "." + str(this_random) + ".jpg"
        merchant.save()
        # Show a success message to the user
        messages.success(request, "Profile updated successfully")
        return redirect('/seller/profile')

    return render(request, "store/profile.html", {"ReqParams": ReqParams, "context": context, "merchant": merchant, "owner": owner,"store": store, "all_notifications":all_notifications})

def Product_Vouchers(request):

    if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
        return HttpResponseRedirect("/page_not_found")

    id = request.session.get(ReqParams.owner_userid)
    store = Store_Info.objects.get(store_id=id)

    owner = Store_Info.objects.get(
        store_id=request.session.get(ReqParams.owner_userid))

    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]
    all_vouchers = Vouchers.objects.filter(store_id = owner.store_id,voucher_type = "Product Voucher").order_by("-id")
    return render(request, "store/product_vouchers.html", {"ReqParams": ReqParams, "owner": owner,"store": store, "all_notifications":all_notifications,"all_vouchers":all_vouchers})

def Shop_Vouchers(request):

    if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
        return HttpResponseRedirect("/page_not_found")

    id = request.session.get(ReqParams.owner_userid)
    store = Store_Info.objects.get(store_id=id)

    owner = Store_Info.objects.get(
        store_id=request.session.get(ReqParams.owner_userid))

    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]
    all_vouchers = Vouchers.objects.filter(store_id = owner.store_id,voucher_type = "Shop Voucher").order_by("-id")
    return render(request, "store/shop_vouchers.html", {"ReqParams": ReqParams, "owner": owner,"store": store, "all_notifications":all_notifications,"all_vouchers":all_vouchers})

def StoreReports(request):

    if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
        return HttpResponseRedirect("/page_not_found")

    id = request.session.get(ReqParams.owner_userid)
    store = Store_Info.objects.get(store_id=id)

    owner = Store_Info.objects.get(
        store_id=request.session.get(ReqParams.owner_userid))

    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]

    return render(request, "store/store_reports.html", {"ReqParams": ReqParams, "owner": owner, "store": store, "all_notifications":all_notifications})


def Add_Staff(request):
    context = {}

    return render(request, "store/add_staff.html",)

def View_Staff(request):
    context = {}

    return render(request, "store/view_staff.html",)

def Edit_Staff(request):
    context = {}

    return render(request, "store/edit_staff.html",)


def Store_Notification_Page(request):

    if ReqParams.owner_userid not in request.session or request.session.get(ReqParams.owner_userid) == None:
        return HttpResponseRedirect("/page_not_found")

    id = request.session.get(ReqParams.owner_userid)
    store = Store_Info.objects.get(store_id=id)

    owner = Store_Info.objects.get(
        store_id=request.session.get(ReqParams.owner_userid))
    
    all_notifications = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid)).order_by('-id')[:15]

    return render(request, "store/store_notifications.html", {"ReqParams": ReqParams, "owner": owner, "store": store, "all_notifications":all_notifications})

def Logout(request):
    logout(request)
    if ReqParams.owner_userid in request.session:
        del request.session[ReqParams.owner_userid]
    messages.success(request, "You have successfully logged out.")
    return HttpResponseRedirect("/merchant/login")


def add_to_cart(request):
    context = {}
    if ReqParams.ANONYMOUS_KEY not in request.session:
        request.session[ReqParams.ANONYMOUS_KEY] = get_random_string(length=32)

    if request.method == "POST":

        acc_id = request.session.get(ReqParams.consumer_userid)
        retval = json.loads(request.POST["value"])
        product = Products.objects.get(pk=retval["product_id"])
        storeid = Store_Info.objects.get(store_id=product.store_id_id)
        variant = None
        if acc_id:

            if retval["variation"]:
                variant = Product_Variations.objects.get(
                    option_id=retval["variation"])

            cart_key = None
            # checking the cart id
            if Cart_Key.objects.filter(account_id=acc_id, store_id=str(storeid.store_id)).exists():
                cart_key = Cart_Key.objects.get(
                    account_id=acc_id, store_id=str(storeid.store_id))
            else:
                # we add cart key
                cart_key = Cart_Key()
                cart_key.store_id = storeid.store_id
                cart_key.account_id = acc_id
                cart_key.save()

            if cart_key:
                # cart = Cart()
                # cart.product_id = product.product_id
                # cart.account_id = acc_id
                # cart.store_id = storeid.store_id
                # cart.price = float(retval["price"])
                # cart.total = float(retval["price"]) * int(retval["quantity"])
                # cart.quantity = int(retval["quantity"])
                if variant:
                    if Cart.objects.filter(account_id=acc_id, product_id=product.product_id, variation_id=variant.id).exists():
                        this_cart = Cart.objects.filter(
                            account_id=acc_id, product_id=product.product_id, variation_id=variant.id)
                        cart = this_cart[0]
                        context["id"] = cart.id
                        context["success"] = 1
                        context["already_in"] = 1
                        context["msg"] = "Product is already added in your cart."
                    else:
                        cart = Cart()
                        cart.product_id = product.product_id
                        cart.product_name = product.product_name
                        cart.account_id = acc_id
                        cart.store_id = storeid.store_id
                        cart.price = float(retval["price"])
                        cart.total = float(
                            retval["price"]) * int(retval["quantity"])
                        cart.quantity = int(retval["quantity"])
                        if variant:
                            cart.variation_id = variant.id
                            cart.variation_name = variant.options_name
                            if variant.image:
                                cart.product_image = variant.image
                            else:
                                cart.product_image = product.default_image
                        else:
                            cart.product_image = product.default_image
                        cart.cart_key = cart_key.id
                        cart.date_added = datetime.now()
                        cart.save()
                        context["id"] = cart.id
                        context["success"] = 1

                        element = {
                            "cart_id":cart_key.id,
                            "image":cart.product_image,
                            "quantity":cart.quantity,
                            "total":cart.total,
                            "product_name":product.product_name
                        }
                        context["already_in"] = 0
                        context["element"] = element
                        context["msg"] = "Product has been added to your cart."
                else:
                    if Cart.objects.filter(account_id=acc_id, product_id=product.product_id).exists():
                        this_cart = Cart.objects.filter(
                            account_id=acc_id, product_id=product.product_id)
                        cart = this_cart[0]
                        context["id"] = cart.id
                        context["success"] = 1
                        context["already_in"] = 1
                        context["msg"] = "Product is already added in your cart."
                    else:
                        cart = Cart()
                        cart.product_id = product.product_id
                        cart.product_name = product.product_name
                        cart.account_id = acc_id
                        cart.store_id = storeid.store_id
                        cart.price = float(retval["price"])
                        cart.total = float(
                            retval["price"]) * int(retval["quantity"])
                        cart.quantity = int(retval["quantity"])
                        cart.product_image = product.default_image
                        if variant:
                            cart.variation_id = variant.id
                            cart.variation_name = variant.options_name
                        cart.cart_key = cart_key.id
                        cart.date_added = datetime.now()
                        cart.save()
                        context["id"] = cart.id
                        context["success"] = 1
                        element = {
                            "cart_id":cart_key.id,
                            "image":cart.product_image,
                            "quantity":cart.quantity,
                            "total":cart.total,
                            "product_name":product.product_name
                        }
                        context["already_in"] = 0
                        context["element"] = element
                        context["msg"] = "Product has been added to your cart."
            if Cart.objects.filter(account_id=acc_id).count() == 1:
                context["count"] = 1            
        else:
            acc_id = request.session.get(ReqParams.ANONYMOUS_KEY)
            # if Cart.objects.filter(account_id=acc_id, product_id=product.product_id).exists():
            #     context["success"] = 0
            #     context["msg"] = "Product is already added in your cart."
            # else:
            variant = None
            if retval["variation"]:
                variant = Product_Variations.objects.get(
                    option_id=retval["variation"])

            cart_key = None
            # checking the cart id
            if Cart_Key.objects.filter(account_id=acc_id, store_id=str(storeid.store_id)).exists():
                cart_key = Cart_Key.objects.get(
                    account_id=acc_id, store_id=str(storeid.store_id))
            else:
                # we add cart key
                cart_key = Cart_Key()
                cart_key.store_id = storeid.store_id
                cart_key.account_id = acc_id
                cart_key.save()

            if cart_key:
                if variant:
                    if Cart.objects.filter(account_id=acc_id, product_id=product.product_id, variation_id=variant.id).exists():
                        this_cart = Cart.objects.filter(
                            account_id=acc_id, product_id=product.product_id, variation_id=variant.id)
                        cart = this_cart[0]
                        context["id"] = cart.id
                        context["success"] = 1
                        context["already_in"] = 1
                        context["msg"] = "Product is already added in your cart."
                    else:
                        cart = Cart()
                        cart.product_id = product.product_id
                        cart.product_name = product.product_name
                        cart.account_id = acc_id
                        cart.store_id = storeid.store_id
                        cart.price = float(retval["price"])
                        cart.total = float(retval["price"]) * int(retval["quantity"])
                        cart.quantity = int(retval["quantity"])
                        if variant:
                            cart.variation_id = variant.id
                            cart.variation_name = variant.options_name
                            if variant.image:
                                cart.product_image = variant.image
                            else:
                                cart.product_image = product.default_image
                        else:
                            cart.product_image = product.default_image

                        cart.cart_key = cart_key.id
                        cart.date_added = datetime.now()
                        cart.save()
                        context["success"] = 1
                        element = {
                            "cart_id":cart_key.id,
                            "image":cart.product_image,
                            "quantity":cart.quantity,
                            "total":cart.total,
                            "product_name":product.product_name
                        }
                        context["already_in"] = 0
                        context["element"] = element
                        context["msg"] = "Product has been added to your cart."
                else:
                    if Cart.objects.filter(account_id=acc_id, product_id=product.product_id).exists():
                        this_cart = Cart.objects.filter(
                            account_id=acc_id, product_id=product.product_id)
                        cart = this_cart[0]
                        context["id"] = cart.id
                        context["success"] = 1
                        context["already_in"] = 1
                        context["msg"] = "Product is already added in your cart."
                    else:
                        cart = Cart()
                        cart.product_id = product.product_id
                        cart.product_name = product.product_name
                        cart.account_id = acc_id
                        cart.store_id = storeid.store_id
                        cart.price = float(retval["price"])
                        cart.total = float(
                            retval["price"]) * int(retval["quantity"])
                        cart.quantity = int(retval["quantity"])
                        cart.product_image = product.default_image
                        if variant:
                            cart.variation_id = variant.id
                            cart.variation_name = variant.options_name
                        cart.cart_key = cart_key.id
                        cart.date_added = datetime.now()
                        cart.save()
                        context["id"] = cart.id
                        context["success"] = 1
                        element = {
                            "cart_id":cart_key.id,
                            "image":cart.product_image,
                            "quantity":cart.quantity,
                            "total":cart.total,
                            "product_name":product.product_name
                        }
                        context["already_in"] = 0
                        context["element"] = element
                        context["msg"] = "Product has been added to your cart."
            if Cart.objects.filter(account_id=acc_id).count() == 1:
                context["count"] = 1    
                
    return HttpResponse(json.dumps(context), "application/json")


def quick_place_order(request):
    context = {}
    if ReqParams.ANONYMOUS_KEY not in request.session:
        request.session[ReqParams.ANONYMOUS_KEY] = get_random_string(length=32)

    if request.method == "POST":
        if request.session.get(ReqParams.consumer_userid):
            acc_id = request.session.get(ReqParams.consumer_userid)
            retval = json.loads(request.POST["value"])
            product = Products.objects.get(pk=retval["product_id"])
            storeid = Store_Info.objects.get(store_id=product.store_id_id)
            variant = None

            if retval["variation"]:
                variant = Product_Variations.objects.get(
                    option_id=retval["variation"])

            cart_key = None
            # checking the cart id
            if Cart_Key.objects.filter(account_id=acc_id, store_id=storeid.store_id).exists():
                cart_key = Cart_Key.objects.get(account_id=acc_id, store_id=str(storeid.store_id))
            else:
                # we add cart key
                cart_key = Cart_Key()
                cart_key.store_id = storeid.store_id
                cart_key.account_id = acc_id
                cart_key.save()

            if cart_key:
                cart = None
                context["cart_key"] = cart_key.id
                if variant:
                    if Cart.objects.filter(account_id=acc_id, product_id=product.product_id, variation_id=variant.id).exists():
                        this_cart = Cart.objects.filter(
                            account_id=acc_id, product_id=product.product_id, variation_id=variant.id)
                        cart = this_cart[0]
                        context["id"] = cart.id
                        context["success"] = 1
                    else:
                        cart = Cart()
                        cart.product_id = product.product_id
                        cart.account_id = acc_id
                        cart.store_id = storeid.store_id
                        cart.price = float(retval["price"])
                        cart.total = float(
                            retval["price"]) * int(retval["quantity"])
                        cart.quantity = int(retval["quantity"])
                        if variant:
                            cart.variation_id = variant.id
                            cart.variation_name = variant.options_name
                            if variant.image:
                                cart.product_image = variant.image
                            else:
                                cart.product_image = product.default_image

                        else:
                            cart.product_image = product.default_image
                        cart.product_name = product.product_name
                        cart.cart_key = cart_key.id
                        cart.date_added = datetime.now()
                        cart.save()
                        context["id"] = cart.id
                        context["success"] = 1
                else:
                    if Cart.objects.filter(account_id=acc_id, product_id=product.product_id).exists():
                        this_cart = Cart.objects.filter(
                            account_id=acc_id, product_id=product.product_id)
                        cart = this_cart[0]
                        context["id"] = cart.id
                        context["success"] = 1
                    else:
                        cart = Cart()
                        cart.product_id = product.product_id
                        cart.account_id = acc_id
                        cart.store_id = storeid.store_id
                        cart.price = float(retval["price"])
                        cart.total = float(
                            retval["price"]) * int(retval["quantity"])
                        cart.quantity = int(retval["quantity"])
                        cart.product_image = product.default_image
                        cart.product_name = product.product_name
                        if variant:
                            cart.variation_id = variant.id
                            cart.variation_name = variant.options_name
                        cart.cart_key = cart_key.id
                        cart.date_added = datetime.now()
                        cart.save()
                        context["id"] = cart.id
                        context["success"] = 1
        else:
            acc_id = request.session.get(ReqParams.ANONYMOUS_KEY)
            retval = json.loads(request.POST["value"])
            product = Products.objects.get(pk=retval["product_id"])
            storeid = Store_Info.objects.get(store_id=product.store_id_id)
            variant = None

            if retval["variation"]:
                variant = Product_Variations.objects.get(
                    option_id=retval["variation"])

            cart_key = None
            # checking the cart id
            if Cart_Key.objects.filter(account_id=acc_id, store_id=storeid.store_id).exists():
                cart_key = Cart_Key.objects.get(account_id=acc_id, store_id=str(storeid.store_id))
            else:
                # we add cart key
                cart_key = Cart_Key()
                cart_key.store_id = storeid.store_id
                cart_key.account_id = acc_id
                cart_key.save()

            if cart_key:
                cart = None
                context["cart_key"] = cart_key.id
                if variant:
                    if Cart.objects.filter(account_id=acc_id, product_id=product.product_id, variation_id=variant.id).exists():
                        this_cart = Cart.objects.filter(
                            account_id=acc_id, product_id=product.product_id, variation_id=variant.id)
                        cart = this_cart[0]
                        context["id"] = cart.id
                        context["success"] = 1
                    else:
                        cart = Cart()
                        cart.product_id = product.product_id
                        cart.product_name = product.product_name
                        cart.account_id = acc_id
                        cart.store_id = storeid.store_id
                        cart.price = float(retval["price"])
                        cart.total = float(
                            retval["price"]) * int(retval["quantity"])
                        cart.quantity = int(retval["quantity"])
                        if variant:
                            cart.variation_id = variant.id
                            cart.variation_name = variant.options_name
                            if variant.image:
                                cart.product_image = variant.image
                            else:
                                cart.product_image = product.default_image
                        else:
                            cart.product_image = product.default_image
                        cart.cart_key = cart_key.id
                        cart.date_added = datetime.now()
                        cart.save()
                        context["id"] = cart.id
                        context["success"] = 1
                else:
                    if Cart.objects.filter(account_id=acc_id, product_id=product.product_id).exists():
                        this_cart = Cart.objects.filter(
                            account_id=acc_id, product_id=product.product_id)
                        cart = this_cart[0]
                        context["id"] = cart.id
                        context["success"] = 1
                    else:
                        cart = Cart()
                        cart.product_id = product.product_id
                        cart.account_id = acc_id
                        cart.store_id = storeid.store_id
                        cart.price = float(retval["price"])
                        cart.total = float(
                            retval["price"]) * int(retval["quantity"])
                        cart.quantity = int(retval["quantity"])
                        cart.product_image = product.default_image
                        if variant:
                            cart.variation_id = variant.id
                            cart.variation_name = variant.options_name
                        cart.cart_key = cart_key.id
                        cart.date_added = datetime.now()
                        cart.save()
                        context["id"] = cart.id
                        context["success"] = 1

    return HttpResponse(json.dumps(context), "application/json")


def update_variation(request):
    context = {}
    if request.method == "POST":
        if Cart.objects.filter(pk=request.POST["id"]).exists():
            this_cart = Cart.objects.get(pk=request.POST["id"])
            value = request.POST["value"]
            if Product_Variations.objects.filter(option_id=value).exists():
                variation = Product_Variations.objects.get(option_id=value)
                this_variation = Product_Variations.objects.get(
                    option_id=value)
                this_cart.price = variation.price
                this_cart.total = variation.price * this_cart.quantity
                this_cart.variation_name = variation.options_name
                this_cart.variation_id = variation.id
                this_cart.save()
                context["total"] = this_cart.total
                context["variation_name"] = variation.options_name
                context["price"] = this_variation.price
                context["success"] = 1
            else:
                context["success"] = 0
        else:
            context["success"] = 0

    return HttpResponse(json.dumps(context), "application/json")


def get_variant_price(request):
    context = {}
    if request.method == "POST":
        value = request.POST["value"]
        if Product_Variations.objects.filter(option_id=value).exists():
            context["success"] = 1
            this_variation = Product_Variations.objects.get(option_id=value)
            context["price"] = this_variation.price
            if this_variation.image:
                context["has_image"] = 1
                context["image"] = this_variation.image
        else:
            context["success"] = 0
    return HttpResponse(json.dumps(context), "application/json")


def check_user_login(request):
    context = {}
    if request.method == "POST":
        context["success"] = 0
        # redirect_url = request.POST["redirect_url"]
        # if ReqParams.consumer_userid not in request.session or request.session.get(ReqParams.consumer_userid) == None:
        #     context["success"] = 1
        #     request.session[ReqParams.LOGIN_REDIRECTION] = redirect_url
        # else:
        #     context["success"] = 0

    return HttpResponse(json.dumps(context), "application/json")

def remove_order_item(request):
    context = {}    
    if request.method == "POST":
        this_id = request.POST["this_id"] + ","
        order_items = StringTolist(request.session.get(ReqParams.CHECKOUT_ITEMS) , "|") 
        new_order_items = ""
        for item in order_items:
            if this_id in item:
                this_str = item.replace(this_id,"")
                if this_str != "":
                    new_order_items += this_str + "|"
            else:
                new_order_items += item + "|"
        
        request.session[ReqParams.CHECKOUT_ITEMS] = new_order_items
        context["success"] = 1
        this_cart = Cart.objects.get(pk = int(request.POST["this_id"]))
        context["store_id"] = this_cart.store_id

    return HttpResponse(json.dumps(context), "application/json")

def Checkout(request):

    if ReqParams.ANONYMOUS_KEY not in request.session:
        request.session[ReqParams.ANONYMOUS_KEY] = get_random_string(length=32)

    if ReqParams.CHECKOUT_ITEMS not in request.session:
        return HttpResponseRedirect("/")

    consumer = None
    retval = []
    store_items = []
    cart_list = []
    total_list = []
    this_json = StringTolist(request.session.get(ReqParams.CHECKOUT_ITEMS),"|")

    if request.session.get(ReqParams.consumer_userid):
        consumer = Consumer.objects.get(
        pk=request.session.get(ReqParams.consumer_userid))
        for value in this_json:
            this_id = StringTolist(value,",")
            temp = []
            index = 0
            total = 0
            for obj in this_id:
                cart_obj = Cart.objects.get(pk=int(obj))

                if str(cart_obj.account_id) != str(request.session.get(ReqParams.consumer_userid)):
                    return HttpResponseRedirect("/error_page")
                else:
                    product = Products.objects.get(pk=cart_obj.product_id)
                    store = Store_Info.objects.get(pk=cart_obj.store_id)
                    if index == 0:
                        store_items.append({
                                "store_name":store.store_name,
                                "store_id":store.store_id,
                                "store_image":store.profile_pic,
                                "store_link":store.store_link
                            }
                            )

                    total += cart_obj.total
                    product_image = product.default_image
                    if cart_obj.product_image:
                        product_image = cart_obj.product_image
                    temp.append(
                        {
                            "id": cart_obj.id,
                            "product_id": product.product_id,
                            "product_name": product.product_name,
                            "price": cart_obj.price,
                            "total": cart_obj.total,
                            "quantity": cart_obj.quantity,
                            "store_name": store.store_name,
                            "store_id": store.store_id,
                            "variation_id": cart_obj.variation_id,
                            "variation_name": cart_obj.variation_name,
                            "product_image": product_image,
                            "store_image": store.profile_pic
                        }
                    )
                index = index + 1
            total_list.append(total)
            cart_list.append(temp)
    else:
        for value in this_json:
            this_id = StringTolist(value,",")
            temp = []
            index = 0
            total = 0
            for obj in this_id:
                cart_obj = Cart.objects.get(pk=int(obj))

                if cart_obj.account_id != request.session.get(ReqParams.ANONYMOUS_KEY):
                    return HttpResponseRedirect("/error_page")
                else:
                    product = Products.objects.get(pk=cart_obj.product_id)
                    store = Store_Info.objects.get(pk=cart_obj.store_id)
                    if index == 0:
                        store_items.append({
                                "store_name":store.store_name,
                                "store_id":store.store_id,
                                "store_image":store.profile_pic,
                                "store_link":store.store_link
                            }
                            )

                    total += cart_obj.total
                    product_image = product.default_image
                    if cart_obj.product_image:
                        product_image = cart_obj.product_image
                    temp.append(
                        {
                            "id": cart_obj.id,
                            "product_id": product.product_id,
                            "product_name": product.product_name,
                            "price": cart_obj.price,
                            "total": cart_obj.total,
                            "quantity": cart_obj.quantity,
                            "store_name": store.store_name,
                            "store_id": store.store_id,
                            "variation_id": cart_obj.variation_id,
                            "variation_name": cart_obj.variation_name,
                            "product_image": product_image,
                            "store_image": store.profile_pic
                        }
                    )
                index = index + 1
            total_list.append(total)
            cart_list.append(temp)


    retval = zip(store_items,cart_list,total_list)
 
    if request.method == "POST":
        # checkout_obj = request.session.get(ReqParams.CHECKOUT_ITEMS)
        anonymous_flag = 0
        acc_id = None
        if request.session.get(ReqParams.consumer_userid):
            acc_id = request.session.get(ReqParams.consumer_userid)
        else:
            acc_id = request.session.get(ReqParams.ANONYMOUS_KEY)
            anonymous_flag = 1

        x = 0
        for key in store_items:
            order = Orders()
            store_id = key["store_id"]
            service_flag = request.POST.get(f"service_flag{store_id}")

            post_date = request.POST.get(f"date{store_id}")
            if request.POST.get(f"order_timing{store_id}") == "now":
                post_date = date.today()

            time = request.POST.get(f"time{store_id}")
            instruction = request.POST.get(f"instruction{store_id}")
            product_cart = cart_list[x]
            order.tax = 0
            order.shipping_fee = 0
            order.online_payment_charge = 0
            order.account_id = acc_id
            order.store_id = store_id
            # order.store_image = store.profile_pic
            order.order_status = "Pending"
            order.date_created = datetime.now()
            order.service_flag = service_flag
            order.date_service = post_date
            order.date_time_service = time
            order.service_instructions = instruction
            order.service_fee = 0


            order.save()
            order.id_format = ID_FORMAT(order.order_id,"ORD")
            # # Generate the QR code for the order
            qr_buffer = generates_qr_code(order.id_format)
            # # Save the QR code image to the Order model
            order.qr_code.save(f'order_{order.id_format}.png', qr_buffer, save=True)

            items = 0
            total = 0
            print(product_cart)
            for product in product_cart:
                items += product["quantity"]
                line_items = Line_Items()
                line_items.product_id = product["product_id"]

                if product["variation_id"]:
                    line_items.variation_id = product["variation_id"]

                line_items.quantity = product["quantity"]
                line_items.order_id = order.order_id

                line_items.save()
                if Cart.objects.filter( pk = product["id"]).exists():
                    this_cart  = Cart.objects.get( pk = product["id"])
                    this_cart.delete()

                this_product = Products.objects.get(pk = product["product_id"])
                if this_product.status_type == 1:
                    stocks = this_product.stock - product["quantity"]
                    this_product.stock = stocks
                    this_product.save()
                    if this_product.stock == 0:
                        this_product.is_available = 0
                        this_product.save()

                total += product["total"]
            order.items = items
            order.subtotal = total
            order.total = total + order.shipping_fee + order.shipping_fee + order.service_fee + order.online_payment_charge
            if anonymous_flag == 1:
                print(request.POST.get("fname"))
                order.fullname = request.POST.get("fname")
                order.phone = request.POST.get("phone")
                order.email_address = request.POST.get("emailadd")
            else:
                order.fullname = consumer.first_name + " " + consumer.last_name
                order.phone = consumer.phone_number1
                order.email_address = consumer.email
                order.profile_picture = consumer.profile_picture

            order.save()
            x = x + 1

        if ReqParams.CHECKOUT_ITEMS  in request.session:
            del request.session[ReqParams.CHECKOUT_ITEMS]
        if anonymous_flag == 1:
            request.session[ReqParams.ANONYMOUS_KEY] = get_random_string(length=32)
            return HttpResponseRedirect(f"/user/purchase/key={request.session.get(ReqParams.ANONYMOUS_KEY)}")
        else:
            return HttpResponseRedirect("/my_purchases")

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


    return render(request,"checkout_page.html",{"retval":retval,"id":id,"consumer":consumer, "my_cart": my_cart,"notifications":notifications})


def redirect_login(request):
    context = {}
    if request.method == "POST":
        request.session[ReqParams.LOGIN_REDIRECTION] = request.POST["current_url"]
        print(request.POST["current_url"])
        context["success"] = 1
    return HttpResponse(json.dumps(context), "application/json")


def select_cart_obj(request):

    context = {}
    if request.method == "POST":
        this_list = StringTolist(request.POST["value"], ",")
        total = 0
        for obj in this_list:
            cart = Cart.objects.get(pk=int(obj))
            total += cart.total
        context["success"] = 1
        context["total"] = total
    return HttpResponse(json.dumps(context), "application/json")


def update_quatity(request):
    context = {}
    if request.method == "POST":
        id = request.POST["id"]
        if Cart.objects.filter(pk=int(id)).exists():
            this_cart = Cart.objects.get(pk=int(id))
            this_cart.quantity = int(request.POST["value"])
            this_cart.total = int(request.POST["value"]) * this_cart.price
            this_cart.save()
            total = int(request.POST["value"]) * this_cart.price
            context["total"] = total
            context["price"] = this_cart.price
            context["success"] = 1
        else:
            context["success"] = 0

    return HttpResponse(json.dumps(context), "application/json")


def check_phone(request):
    context = {}
    if request.method == "POST":
        if Consumer.objects.filter(phone_number1=request.POST["value"]).exists():
            context["success"] = 1
        else:
            context["success"] = 0

    return HttpResponse(json.dumps(context), "application/json")


def quick_checkout(request):

    context = {}
    if request.method == "POST":
        this_list = request.POST["value"]
        request.session[ReqParams.CHECKOUT_ITEMS] = this_list
        context["success"] = 1
        print(request.session.get(ReqParams.CHECKOUT_ITEMS))
    return HttpResponse(json.dumps(context), "application/json")


def checkout_items(request):

    context = {}
    if request.method == "POST":
        request.session[ReqParams.CHECKOUT_ITEMS] = request.POST["value"]
        context["success"] = 1
        print(request.session.get(ReqParams.CHECKOUT_ITEMS))
    return HttpResponse(json.dumps(context), "application/json")


def order_list(request):

    if ReqParams.consumer_userid not in request.session:
        return HttpResponseRedirect("/")
    accid = request.session.get(ReqParams.consumer_userid)

    retval = []
    orders = []
    products = []
    my_orders = Orders.objects.filter(account_id = accid)
    for order in my_orders:

        store = None
        if Store_Info.objects.filter(pk = order.store_id).exists():
            store = Store_Info.objects.get(pk = order.store_id)
            orders.append({
                "order_id":order.order_id,
                "id_format":order.id_format,
                "qr_code": order.qr_code,
                "total":order.total,
                "store_id":store.store_id,
                "store_link": store.store_link,
                "store_image":store.profile_pic,
                "store_name":store.store_name,
                "total":order.total
            } )

        else:
            orders.append({
                "order_id":0,
            } )



        line_items = Line_Items.objects.filter(order_id = order.order_id)
        temp = []
        for item in line_items:

            product = None
            if Products.objects.filter(pk = item.product_id).exists():
                product =  Products.objects.get(pk = item.product_id)
            if product:
                variation = ""
                price = product.original_price
                if item.variation_id:
                    if Product_Variations.objects.filter(pk = item.variation_id).exists():
                        this_varation = Product_Variations.objects.get(pk = item.variation_id)
                        variation = this_varation.options_name
                        price = this_varation.price
                temp.append({

                    "product_id":product.product_id,
                    "image":product.default_image,
                    "quantity":item.quantity,
                    "product_name":product.product_name,
                    "price":price,
                    "varation_name":variation

                })
            else:
                temp.append({
                    "product_id":0,
                })



        products.append(temp)
    retval = zip(orders,products)

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

    return render(request, 'order_list.html',{"ReqParams":ReqParams, "consumer":consumer, "my_cart":my_cart, "products": products, "retval":retval,"notifications":notifications} )

def anonymous_order_list(request,id):

    accid = id
    retval = []
    orders = []
    products = []
    my_orders = Orders.objects.filter(account_id = accid)
    for order in my_orders:

        store = None
        if Store_Info.objects.filter(pk = order.store_id).exists():
            store = Store_Info.objects.get(pk = order.store_id)
            orders.append({
                "order_id":order.order_id,
                "id_format":order.id_format,
                "qr_code": order.qr_code,
                "total":order.total,
                "store_id":store.store_id,
                "store_link": store.store_link,
                "store_image":store.profile_pic,
                "store_name":store.store_name,
                "total":order.total
            } )

        else:
            orders.append({
                "order_id":0,
            } )

        line_items = Line_Items.objects.filter(order_id = order.order_id)
        temp = []
        for item in line_items:

            product = None
            if Products.objects.filter(pk = item.product_id).exists():
                product =  Products.objects.get(pk = item.product_id)
            if product:
                variation = ""
                price = product.original_price
                if item.variation_id:
                    if Product_Variations.objects.filter(pk = item.variation_id).exists():
                        this_varation = Product_Variations.objects.get(pk = item.variation_id)
                        variation = this_varation.options_name
                        price = this_varation.price
                temp.append({

                    "product_id":product.product_id,
                    "image":product.default_image,
                    "quantity":item.quantity,
                    "product_name":product.product_name,
                    "price":price,
                    "varation_name":variation

                })
            else:
                temp.append({
                    "product_id":0,
                })
        products.append(temp)
    retval = zip(orders,products)

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

    return render(request, 'order_list.html', {"ReqParams":ReqParams, "consumer":consumer, "my_cart":my_cart, "products": products,"retval":retval,"id":id,"notifications":notifications})

def quick_login(request):
    context = {}

    if request.method == "POST":
        if Consumer.objects.filter(email=request.POST['userid']).exists():
            this_email = request.POST['userid']
            context["userid"] = request.POST['userid']
            this_user = Consumer.objects.get(email=this_email)
            password = request.POST["password"]
            # convertion into base64
            passAscii = password.encode("ascii")
            passBytes = base64.b64encode(passAscii)
            if this_user.password == passBytes:
                # success login

                # we used this session/ cookie value to call data from other table
                # it is also going to be used to check if an user has been login
                request.session[ReqParams.consumer_userid] = this_user.account_id
                context["success"] = 1
                if ReqParams.ANONYMOUS_KEY in request.session:
                    if Cart_Key.objects.filter(account_id = request.session.get(ReqParams.ANONYMOUS_KEY)).exists():
                        cart_key = Cart_Key.objects.filter(account_id = request.session.get(ReqParams.ANONYMOUS_KEY))
                        for key in cart_key:
                            this_cart = Cart.objects.filter(cart_key = key.id)
                            this_key = None
                            if Cart_Key.objects.filter(account_id = this_user.account_id,store_id = key.store_id).exists():
                                this_key = Cart_Key.objects.get(account_id = this_user.account_id,store_id = key.store_id)
                            else:
                                this_key = Cart_Key()
                                this_key.account_id = this_user.account_id
                                this_key.store_id = key.store_id
                                this_key.save()

                            for cart in this_cart:
                                cart.account_id = this_user.account_id
                                cart.cart_key = this_key.id
                                cart.save()
                            key.account_id =  this_user.account_id
                            key.delete()

            else:
                context["error_msg"] = "User ID or  Password in incorrect!"
                context["success"] = 0

        elif Consumer.objects.filter(user_name=request.POST['userid']).exists():
            this_username = request.POST['userid']
            context["userid"] = request.POST['userid']
            this_user = Consumer.objects.get(user_name=this_username)
            password = request.POST["password"]
            # convertion into base64
            passAscii = password.encode("ascii")
            passBytes = base64.b64encode(passAscii)
            if this_user.password == passBytes:
                # success login

                # we used this session/ cookie value to call data from other table
                # it is also going to be used to check if an user has been login
                request.session[ReqParams.consumer_userid] = this_user.account_id
                context["success"] = 1
                if ReqParams.ANONYMOUS_KEY in request.session:
                    if Cart_Key.objects.filter(account_id = request.session.get(ReqParams.ANONYMOUS_KEY)).exists():
                        cart_key = Cart_Key.objects.filter(account_id = request.session.get(ReqParams.ANONYMOUS_KEY))
                        for key in cart_key:
                            this_key = None
                            this_cart = Cart.objects.filter(cart_key = key.id)
                            if Cart_Key.objects.filter(account_id = this_user.account_id,store_id = key.store_id).exists():
                                this_key = Cart_Key.objects.get(account_id = this_user.account_id,store_id = key.store_id)
                            else:
                                this_key = Cart_Key()
                                this_key.account_id = this_user.account_id
                                this_key.store_id = key.store_id
                                this_key.save()

                            for cart in this_cart:
                                cart.account_id = this_user.account_id
                                cart.cart_key = this_key.id
                                cart.save()
                            key.account_id =  this_user.account_id
                            key.delete()
            else:
                context["error_msg"] = "User ID or  Password in incorrect!"
                context["success"] = 0

        else:
            context["userid"] = request.POST['userid']
            context["error_msg"] = "User ID or  Password in incorrect!"
            context["success"] = 0

    return HttpResponse(json.dumps(context), "application/json")

def get_cart_total(request):
    context = {}

    if request.method == "POST":
        accid = None
        if ReqParams.consumer_userid in request.session:
            accid = request.session.get(ReqParams.consumer_userid)
        else:
            accid = request.session.get(ReqParams.ANONYMOUS_KEY)
        context["count"] = Cart.objects.filter(account_id = accid).count()
    return HttpResponse(json.dumps(context), "application/json")


def check_available_product(request):
    context = {}
    retval = ""
    if request.method == "POST":
        accid = None
        if ReqParams.consumer_userid in request.session:
            accid = request.session.get(ReqParams.consumer_userid)
        else:
            accid = request.session.get(ReqParams.ANONYMOUS_KEY)

        my_cart = Cart.objects.filter(account_id = accid)
        for cart in my_cart:
            this_product = Products.objects.get(product_id = cart.product_id)
            if this_product.is_available == 0:
                retval += str(cart.id) + ","

        context["retval"] = retval
    return HttpResponse(json.dumps(context), "application/json")

def check_available_product(request):
    context = {}
    retval = ""
    if request.method == "POST":
        accid = None
        if ReqParams.consumer_userid in request.session:
            accid = request.session.get(ReqParams.consumer_userid)
        else:
            accid = request.session.get(ReqParams.ANONYMOUS_KEY)

        my_cart = Cart.objects.filter(account_id = accid)
        for cart in my_cart:
            this_product = Products.objects.get(product_id = cart.product_id)
            if this_product.is_available == 0:
                retval += str(cart.id) + ","

        context["retval"] = retval
    return HttpResponse(json.dumps(context), "application/json")

def check_quantity(request):
    context = {}
    retval = ""
    msg = ""
    if request.method == "POST":
        accid = None
        if ReqParams.consumer_userid in request.session:
            accid = request.session.get(ReqParams.consumer_userid)
        else:
            accid = request.session.get(ReqParams.ANONYMOUS_KEY)

        my_cart = Cart.objects.filter(account_id = accid)
        for cart in my_cart:
            this_product = Products.objects.get(product_id = cart.product_id)
            if this_product.status_type == 1:
                if this_product.stock < cart.quantity:
                    retval += str(cart.id) + ","
                    item = "item"
                    if this_product.stock > 1:
                        item = "items"
                    msg +=  f"Only {this_product.stock} {item} left."+ ","
        context["retval"] = retval
        context["msg"] = msg

    return HttpResponse(json.dumps(context), "application/json")

def check_variations(request):
    context = {}
    retval = ""
    msg = ""
    if request.method == "POST":
        accid = None
        if ReqParams.consumer_userid in request.session:
            accid = request.session.get(ReqParams.consumer_userid)
        else:
            accid = request.session.get(ReqParams.ANONYMOUS_KEY)

        my_cart = Cart.objects.filter(account_id = accid)
        for cart in my_cart:
            if cart.variation_id:
                # this_product = Products.objects.get(product_id = cart.product_id)
                this_variation = Product_Variations.objects.get(pk = cart.variation_id)
                if this_variation.status_type == 1:
                    if this_variation.stocks != 0:
                        if this_variation.stocks < cart.quantity:
                            retval += str(cart.id) + ","
                            item = "item"
                            if this_variation.stocks > 1:
                                item = "items"
                            msg += f"Only {this_variation.stocks} {item} for Variation {this_variation.options_name}."  + ","
                    else:
                        retval += str(cart.id) + ","

                        msg += f"Variation {this_variation.options_name} is not available at the moment."  + ","

                else:
                    if this_variation.available_flag != 1:
                        retval += str(cart.id) + ","
                        msg += f"Variation {this_variation.options_name} is not available at the moment." + ","

        context["retval"] = retval
        context["msg"] = msg

    return HttpResponse(json.dumps(context), "application/json")


def disable_cart_variation(request):
    context = {}
    retval = ""
    if request.method == "POST":
        accid = None
        if ReqParams.consumer_userid in request.session:
            accid = request.session.get(ReqParams.consumer_userid)
        else:
            accid = request.session.get(ReqParams.ANONYMOUS_KEY)

        my_cart = Cart.objects.filter(account_id = accid).exclude(variation_id = None)
        for cart in my_cart:
            this_attr = Product_Attributes.objects.filter(product_id = cart.product_id)
            for attr in this_attr:
                this_options = Product_Attributes_Option.objects.filter(attribute_id = attr.id)
                for opt in this_options:
                    this_str = str(opt.id) + ","
                    this_variation = Product_Variations.objects.filter(option_id__icontains=this_str)
                    flag = 0
                    for variation in this_variation:

                        if variation.status_type == 1:
                            if variation.stocks == 0:
                                flag += 1
                        else:
                            if variation.available_flag == 0:
                                flag += 1
                    if flag == len(this_variation):
                        retval += str(opt.id) + ","

        context["retval"] = retval

    return HttpResponse(json.dumps(context), "application/json")

def disable_product_variation(request):
    context = {}
    retval = ""
    if request.method == "POST":
        this_id = request.POST["value"]
        this_product = Products.objects.get(pk = this_id)
        this_attr = Product_Attributes.objects.filter(product_id = this_product.product_id)
        for attr in this_attr:
            this_options = Product_Attributes_Option.objects.filter(attribute_id = attr.id)
            for opt in this_options:
                this_str = str(opt.id) + ","
                this_variation = Product_Variations.objects.filter(option_id__icontains=this_str)
                flag = 0
                for variation in this_variation:
                    if variation.status_type == 1:
                        if variation.stocks == 0:
                            flag += 1
                    else:
                        if variation.available_flag == 0:
                            flag += 1
                if flag == len(this_variation):
                    retval += str(opt.id) + ","

        context["retval"] = retval
    return HttpResponse(json.dumps(context), "application/json")

def available_switch(request):

    if request.method == "POST":
        this_value = request.POST["value"]
        this_product = Products.objects.get(pk = request.POST["this_id"])
        this_product.available_flag = int(this_value)
        this_product.save()

    return HttpResponse(json.dumps({}), "application/json")

def disable_product(request):
    context = {}
    if request.method == "POST":
        this_value = request.POST["value"]
        this_product = Products.objects.get(pk = this_value)
        if this_product.is_available == 0:
            context["success"] = 1
        else:
            context["success"] = 0

    return HttpResponse(json.dumps(context), "application/json")

def drag_order_status(request):

    context = {
        "col1":"Pending",
        "col2":"Preparing",
        "col3":"Prepared",
        "col4":"Completed",
        "col5":"Cancelled",
    }
    if request.method == "POST":
        this_id = request.POST["this_id"]
        this_col = request.POST["this_col"]
        this_order = Orders.objects.get(pk = this_id)
        this_order.order_status = context[this_col]
        if context[this_col] == "Completed":
            this_order.date_paid = datetime.now()
            this_order.date_completed = datetime.now()
            context["paid"] = 1
            context["order_id"] = this_order.order_id
        this_order.save()

    return HttpResponse(json.dumps(context), "application/json")


def run_script(request):
    consumer = Consumer.objects.all()
    for con in consumer:
        con.id_format = ID_FORMAT(con.account_id,"CON")
        con.save()
    product = Products.objects.all()
    for con in product:
        con.id_format = ID_FORMAT(con.product_id,"PROD")
        con.save()
    order = Orders.objects.all()
    for con in order:
        con.id_format = ID_FORMAT(con.order_id,"ORD")
        con.save()
    merchant = Store_Info.objects.all()
    for con in merchant:
        con.id_format = ID_FORMAT(con.store_id,"MER")
        con.save()

    return HttpResponseRedirect("/")

def request_share_order(request):
    context = {}

    if request.method == "POST":
        this_id = request.POST["value"]

        if Orders.objects.filter(id_format = this_id).exists():
            if Orders.objects.filter(account_id = request.session.get(ReqParams.consumer_userid), id_format = this_id).exists():
                context["success"] = 1
                context["msg"] = f"You cant request your own order!"
            else:
                order = Orders.objects.get(id_format = this_id)
                if order.order_status != "Pending":
                    print("12121")
                    context["success"] = 1
                    context["msg"] = f"Order {this_id} can't be shared!"
                else:

                    context["success"] = 0
                    context["msg"] = f"Share Order Request has been sent!"
                    new_notif = Notifications()
                    this_account = Consumer.objects.get(pk = order.account_id)
                    account = Consumer.objects.get(pk = request.session.get(ReqParams.consumer_userid))
                    new_notif.consumer_id = this_account.account_id
                    new_notif.consumer_id_format = this_account.id_format
                    new_notif.requesting_share_order = account.account_id
                    new_notif.requesting_name = account.first_name + " " + account.last_name
                    new_notif.requesting_id_format = account.id_format
                    new_notif.order_id = order.order_id
                    new_notif.order_id_format = order.id_format
                    new_notif.content = f"wants to add items into your {order.id_format}. Allow it?"
                    new_notif.url = settings.URL_SITE_DOMAIN + "/request_share_order"
                    new_notif.date_time = datetime.now()
                    new_notif.notif_type = "Share Order"
                    new_notif.image = this_account.profile_picture
                    new_notif.save()

        else:
            context["success"] = 1
            context["msg"] = f"Order {this_id} does not exist!"

    return HttpResponse(json.dumps(context), "application/json")

def accept_request(request):
    context = {}

    if request.method == "POST":
        this_id = request.POST["this_id"]
        if Notifications.objects.filter(pk = this_id).exists():
            notif = Notifications.objects.get(pk = this_id)
            this_order = Orders.objects.get(pk = notif.order_id)
            account = Consumer.objects.get(pk = request.session.get(ReqParams.consumer_userid))

            requesting_account = Consumer.objects.get(pk = notif.requesting_share_order)
            print("dfsdfsdfdf" + str(requesting_account.pk))
            notif.requested_response = "Yes"
            notif.save()
            if not this_order.shared_to:
                this_order.shared_to = ""
                this_order.save()
            this_order.shared_to = this_order.shared_to + str(requesting_account.pk) + ","
            this_order.save()


            new_notif = Notifications()
            new_notif.consumer_id = requesting_account.account_id
            new_notif.consumer_id_format = requesting_account.id_format
            new_notif.requested_response = "Yes"
            new_notif.account_responded = account.account_id
            new_notif.account_responded_name = account.first_name + " " + account.last_name
            new_notif.account_responded_id_format = account.id_format
            new_notif.order_id = this_order.order_id
            new_notif.order_id_format = this_order.id_format
            new_notif.content = f"Your request for share order to {this_order.id_format} was approved by {account.id_format}."
            new_notif.url = settings.URL_SITE_DOMAIN + f"/shared_order/{this_order.order_id}"
            new_notif.date_time = datetime.now()
            new_notif.notif_type = "Share Order Response"
            new_notif.image = account.profile_picture
            new_notif.save()
            context["success"] = 1
            context["msg"] = "Accepted!"
        else:
            context["success"] = 0
            context["msg"] = "Something went wrong!"
    return HttpResponse(json.dumps(context), "application/json")

def denied_request(request):
    context = {}
    if request.method == "POST":
        this_id = request.POST["this_id"]
        if Notifications.objects.filter(pk = this_id).exists():
            notif = Notifications.objects.get(pk = this_id)
            this_order = Orders.objects.get(pk = notif.order_id)
            account = Consumer.objects.get(pk = request.session.get(ReqParams.consumer_userid))
            requesting_account = Consumer.objects.get(pk = notif.requesting_share_order)
            notif.requested_response = "No"
            notif.save()

            new_notif = Notifications()
            new_notif.consumer_id = requesting_account.account_id
            new_notif.consumer_id_format = requesting_account.id_format
            new_notif.requested_response = "No"
            new_notif.account_responded = account.account_id
            new_notif.account_responded_name = account.first_name + " " + account.last_name
            new_notif.account_responded_id_format = account.id_format
            new_notif.order_id = this_order.order_id
            new_notif.order_id_format = this_order.id_format
            new_notif.content = f"Your request for share order to {this_order.id_format} was denied by {account.id_format}."
            new_notif.url = settings.URL_SITE_DOMAIN + f"/my_purchases"
            new_notif.date_time = datetime.now()
            new_notif.notif_type = "Share Order Response"
            new_notif.image = account.profile_picture
            new_notif.save()
            context["success"] = 1
            context["msg"] = "Denied!"
        else:
            context["success"] = 0
            context["msg"] = "Something went wrong!"
    return HttpResponse(json.dumps(context), "application/json")

def add_item_to_order(request,id,order_id):
    if ReqParams.consumer_userid not in request.session:
        return HttpResponseRedirect("/")

    order = Orders.objects.get(pk = order_id)
    if order.shared_to:
        this_id = StringTolist(order.shared_to,",")
        if str(request.session.get(ReqParams.consumer_userid)) not in this_id or order.order_status != "Pending":
            return HttpResponseRedirect("/error_page")
    else:
        return HttpResponseRedirect("/error_page")

    this_store = Store_Info.objects.get(store_id=id)
    products = Products.objects.filter(
        store_id=this_store, is_archived=False, display_flag=1)

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
    return render(request, "add_item_to_order.html", {"ReqParams": ReqParams, "consumer": consumer,"order":order,
                                           "this_store": this_store, "products": products, "my_cart": my_cart, "retval": retval,"notifications":notifications})

def add_to_order(request): #add item to existing order
    context = {}

    if request.method == "POST":
        order_id = request.POST["order_id"]
        retval = json.loads(request.POST["value"])
        order = Orders.objects.get(pk = order_id)
        product = Products.objects.get(pk=retval["product_id"])
        # account = Consumer.objects.get(pk = request.session.get(ReqParams.consumer_userid))
        # storeid = Store_Info.objects.get(store_id=product.store_id_id)
        variant = None
        line_item = Line_Items()
        if retval["variation"]:
            variant = Product_Variations.objects.get(option_id=retval["variation"])
            print(variant.id)
            if Line_Items.objects.filter(product_id = retval["product_id"],order_id = order_id,variation_id = str(variant.id)).exists():
                print("1")
                total = int(retval["quantity"]) * float(retval["price"])
                order.subtotal += total
                order.total += total
                order.items = int(retval["quantity"])
                order.save()

                this_line_item = Line_Items.objects.get(product_id = product.product_id,order_id = order.order_id,variation_id = variant.id)
                this_line_item.quantity += int(retval["quantity"])
                this_line_item.save()
            else:
                total = int(retval["quantity"]) * float(retval["price"])
                order.subtotal += total
                order.total += total
                order.items = int(retval["quantity"])
                order.save()
                line_item.quantity = int(retval["quantity"])
                line_item.product_id = product.pk
                line_item.variation_id = str(variant.id)
                line_item.order_id = order.pk
                line_item.save()
                print("2")
        else:
            if Line_Items.objects.filter(product_id = product.product_id,order_id = order.order_id).exists():
                total = int(retval["quantity"]) * float(retval["price"])
                order.subtotal += total
                order.total += total
                order.items = int(retval["quantity"])
                order.save()
                this_line_item = Line_Items.objects.get(product_id = product.product_id,order_id = order.order_id)
                this_line_item.quantity += int(retval["quantity"])
                this_line_item.save()
            else:
                total = int(retval["quantity"]) * float(retval["price"])
                order.subtotal += total
                order.total += total
                order.items = int(retval["quantity"])
                order.save()
                line_item.quantity = int(retval["quantity"])
                line_item.product_id = product.pk
                line_item.order_id = order.pk
                line_item.save()
        context["success"] = 1
        context["msg"] = f"Item has added to order {order.id_format}."

    return HttpResponse(json.dumps(context), "application/json")

def unread_notifications(request):
    context = {}

    if request.method == "POST":
        if ReqParams.consumer_userid in request.session:
            if Consumer.objects.filter(pk = request.session.get(ReqParams.consumer_userid)).exists():
                notif_count = Notifications.objects.filter(consumer_id = request.session.get(ReqParams.consumer_userid),read = 0).count()
                context["success"] = 1
                context["count"] = notif_count
            else:
                context["success"] = 0
        else:
            context["success"] = 0

    return HttpResponse(json.dumps(context), "application/json")

def unread_notifications_merchant(request):
    context = {}

    if request.method == "POST":
        if ReqParams.consumer_userid in request.session:
            if Store_Info.objects.filter(pk = request.session.get(ReqParams.owner_userid)).exists():
                notif_count = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid),read = 0).count()
                context["success"] = 1
                context["count"] = notif_count
            else:
                context["success"] = 0
        else:
            context["success"] = 0

    return HttpResponse(json.dumps(context), "application/json")

def read_notifications(request):
    context = {}

    if request.method == "POST":
        if ReqParams.consumer_userid in request.session:
            if Consumer.objects.filter(pk = request.session.get(ReqParams.consumer_userid)).exists():
                notif_count = Notifications.objects.filter(consumer_id = request.session.get(ReqParams.consumer_userid),read = 0)
                if notif_count:
                    for notif in notif_count:
                        notif.read = 1
                        notif.save()
                context["success"] = 1
            else:
                context["success"] = 0
        else:
            context["success"] = 0

    return HttpResponse(json.dumps(context), "application/json")

def read_notifications_merchant(request):
    context = {}

    if request.method == "POST":
        if ReqParams.consumer_userid in request.session:
            if Store_Info.objects.filter(pk = request.session.get(ReqParams.owner_userid)).exists():
                notif_count = Notifications.objects.filter(merchant_id = request.session.get(ReqParams.owner_userid),read = 0)
                if notif_count:
                    for notif in notif_count:
                        notif.read = 1
                        notif.save()
                context["success"] = 1
            else:
                context["success"] = 0
        else:
            context["success"] = 0

    return HttpResponse(json.dumps(context), "application/json")

def remove_cart_item(request):
    context = {}

    if request.method == "POST":
        this_id = request.POST["this_id"]
        if Cart.objects.filter(pk = this_id).exists():
            this_item =  Cart.objects.get(pk = this_id)
            context["cart_key"] = this_item.cart_key
            this_item.delete()
            context["success"] = 1
            context["msg"] = "Successfully Removed!"
        else:
            context["success"] = 0
            context["msg"] = "Can't Removed!"

    return HttpResponse(json.dumps(context), "application/json")

def remove_notif(request):
    context = {}

    if request.method == "POST":
        this_id = request.POST["this_id"]
        if Notifications.objects.filter(pk = this_id).exists():
            notif =  Notifications.objects.get(pk = this_id)
            notif.delete()
            context["success"] = 1
            context["msg"] = "Successfully Removed!"
        else:
            context["success"] = 0
            context["msg"] = "Can't Removed!"

    return HttpResponse(json.dumps(context), "application/json")

def request_discount(request):

    context = {}
    if request.method == "POST":

        this_file = request.FILES['myfile']
        this_dicount_id = request.POST['discount_id']
        order_id = request.POST['order_id']
        consumer = Consumer.objects.get(pk = request.session.get(ReqParams.consumer_userid))
        order = Orders.objects.get(pk = order_id)
        merchant = Store_Info.objects.get(pk = order.store_id)
        personnel_discount = Discount_Personnel.objects.get(pk = this_dicount_id)

        new_request_discount = Personnel_Discount_Requests()
        new_request_discount.consumer_id = consumer.pk
        new_request_discount.consumer_id_format = consumer.id_format
        new_request_discount.order_id = order.pk
        new_request_discount.order_id_format = order.id_format
        new_request_discount.personnel_discount_id = personnel_discount.pk
        new_request_discount.personnel_discount_id_format = personnel_discount.id_format
        new_request_discount.personnel_status = personnel_discount.personnel_status
        new_request_discount.store_id = merchant.pk
        new_request_discount.store_id_format = merchant.id_format
        new_request_discount.save()
        new_request_discount.id_format = ID_FORMAT(new_request_discount.id,"ReqDis")
        new_request_discount.file = "discount_file_" +  str(new_request_discount.id) + "." + str(consumer.pk) + ".jpg"
        upload_discount_file(this_file, str(new_request_discount.id), str(consumer.pk))
        new_request_discount.save()


        new_notif = Notifications()
        new_notif.merchant_id = merchant.pk
        new_notif.merchant_id_format = merchant.id_format
        new_notif.requesting_discount = consumer.pk
        new_notif.requesting_id_format = consumer.id_format
        new_notif.order_id = order.pk
        new_notif.order_id_format = order.id_format
        new_notif.requesting_name = consumer.first_name + " " + consumer.last_name
        if merchant.profile_picture:
            new_notif.image = merchant.profile_picture
        new_notif.url = settings.URL_SITE_DOMAIN + f"/personnel_discount/request={new_request_discount.id}"
        new_notif.notif_type = "Personnel Discount Request"
        new_notif.date_time = datetime.now()
        new_notif.content = f"requested a discount into order {order.id_format}. Accept it?"
        new_notif.save()

        context["success"] = 1
        context["msg"] = "Your request for a discount has been submitted to the merchant. Please wait for the approval of your request."



    return HttpResponse(json.dumps(context), "application/json")

def Requested_Discounts(request):
    context = {}

    if request.method == "POST":
        pending_orders = Orders.objects.filter(order_status = "Pending",discounted_flag = 0)
        retval = ""
        for pending in pending_orders:
            if Personnel_Discount_Requests.objects.filter(consumer_id = request.session.get(ReqParams.consumer_userid),order_id = pending.pk).exists():
                retval += str(pending.pk) + ","
        if retval:
            retval = retval[:-1]
            context["success"] = 1
        else:
            context["success"] = 0         

        context["retval"] = retval       
    return HttpResponse(json.dumps(context), "application/json")

def checkout_all(request):
    acc_id = None
    if ReqParams.consumer_userid in request.session:
        acc_id = request.session.get(ReqParams.consumer_userid)
    else:
        acc_id = request.session.get(ReqParams.ANONYMOUS_KEY)   

    cart_key = Cart_Key.objects.filter(account_id = acc_id)
    retval = ""
    for key in cart_key:
        temp = ""
        if Cart.objects.filter(cart_key = key.id).exists():
            cart = Cart.objects.filter(cart_key = key.id)
            for obj in cart:
                temp += str(obj.id) + ","
            retval += temp + "|"

    request.session[ReqParams.CHECKOUT_ITEMS] = retval

    return HttpResponseRedirect("/checkout")