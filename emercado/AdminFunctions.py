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
import string
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from random import randint
import base64
import qrcode
from io import BytesIO
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


# adminnnnn
def ADMIN_ID_FORMAT(id,idtype):
    retval = idtype
    id_len = 10
    lastid = str(id)
    lastid_len = len(lastid)
    len_zeros = id_len - lastid_len
    while len_zeros != 0:
        retval += "0"
        len_zeros -= 1
    retval += lastid   
    
    return retval

def Admin_LoginPage(request):
    context = {}

    if request.method == "POST":
        context["userid"] = request.POST.get("userid")
        if System_User.objects.filter(email=request.POST.get('userid')).exists():
            this_email = request.POST.get('userid')
            context["userid"] = request.POST.get('userid')
            this_user = System_User.objects.get(email=this_email)
            password = request.POST.get("password")
            # convertion into base64
            passAscii = password.encode("ascii")
            passBytes = base64.b64encode(passAscii)
            if this_user.password == passBytes:

                request.session[ReqParams.admin_userid] = this_user.account_id
                return HttpResponseRedirect("/admin_dashboard")
            else:
                context["error_msg"] = "Invalid Credentials!"
                return render(request, 'admin/admin_login.html', {"context":context,})
        elif System_User.objects.filter(user_name = request.POST.get('userid')).exists():
            this_username = request.POST.get('userid')
            context["userid"] = request.POST.get('userid')
            this_user = System_User.objects.get(user_name = this_username)
            password = request.POST.get("password")
            # convertion into base64
            passAscii = password.encode("ascii")
            passBytes = base64.b64encode(passAscii)
            if this_user.password == passBytes:
                request.session[ReqParams.admin_userid] = this_user.account_id
                return HttpResponseRedirect("/admin_dashboard")
            else:
                context["error_msg"] = "Invalid Credentials!"
                return render(request, 'admin/admin_login.html', {"context":context,})
            
    return render(request, 'admin/admin_login.html', {"context":context,})


def Admin_Dashboard(request):
   
    if ReqParams.admin_userid not in request.session:
        return HttpResponseRedirect("/admin_login")
    user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    role = Role.objects.get(pk = user.role_id)
    return render(request, 'admin/dashboard.html', {"role":role,"user":user})

def Reports(request):
    if ReqParams.admin_userid not in request.session:
        return HttpResponseRedirect("/admin_login")
    user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    role = Role.objects.get(pk = user.role_id)
    if role.report_view_access != 1:
        return HttpResponseRedirect("/page_not_found")
    
    return render(request, 'admin/reports.html', {"role":role,"user":user})

def Discounted_Personnel_Page(request):
    if ReqParams.admin_userid not in request.session:
        return HttpResponseRedirect("/admin_login")
    user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    role = Role.objects.get(pk = user.role_id)
    if role.report_view_access != 1:
        return HttpResponseRedirect("/page_not_found")
    
    all_discounts = Discount_Personnel.objects.all()

    return render(request, 'admin/discounted_personnel.html',{"role":role,"user":user,"all_discounts":all_discounts})

def View_ShopVoucher_Page(request):
    # if ReqParams.admin_userid not in request.session:
    #     return HttpResponseRedirect("/admin_login")
    # user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    # role = Role.objects.get(pk = user.role_id)
    # if role.report_view_access != 1:
    #     return HttpResponseRedirect("/page_not_found")
    
    # all_discounts = Discount_Personnel.objects.all()

    return render(request, 'admin/view_shop_vouchers.html')

def View_ProductVoucher_Page(request):
    # if ReqParams.admin_userid not in request.session:
    #     return HttpResponseRedirect("/admin_login")
    # user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    # role = Role.objects.get(pk = user.role_id)
    # if role.report_view_access != 1:
    #     return HttpResponseRedirect("/page_not_found")
    
    # all_discounts = Discount_Personnel.objects.all()

    return render(request, 'admin/view_product_vouchers.html')


def add_discount_personnel(request):
    context = {}

    if request.method == "POST":
        new_discount = Discount_Personnel()
        status = request.POST["status"]
        discount = request.POST["discount"]
        new_discount.personnel_status = status.title()
        new_discount.discount_percentage = float(discount)
        new_discount.save()
        new_discount.id_format = ADMIN_ID_FORMAT(new_discount.id,"DIS")
        new_discount.save()

    return HttpResponse(json.dumps(context), "application/json")

def edit_discount_personnel(request):
    context = {}
    if request.method == "POST":
        discount = request.POST["discount"]
        this_id = request.POST["this_id"]
        this_discount = Discount_Personnel.objects.get(pk = this_id)
        this_discount.discount_percentage = float(discount)
        this_discount.save()
    return HttpResponse(json.dumps(context), "application/json")

def delete_discount_personnel(request):
    context = {}
    if request.method == "POST":
    
        this_id = request.POST["this_id"]
        this_discount = Discount_Personnel.objects.get(pk = this_id)
        this_discount.delete()

    return HttpResponse(json.dumps(context), "application/json")

def check_personnel_status(request):
    context = {}

    if request.method == "POST":
        this_value = request.POST["value"]
        if Discount_Personnel.objects.filter(personnel_status = this_value.title()).exists():
            context["success"] = 1
            context["msg"] = "Duplicate Discount Personnel!"
        else:
            context["success"] = 0

    return HttpResponse(json.dumps(context), "application/json")

# category
def Admin_SubCategory(request):

    if ReqParams.admin_userid not in request.session:
        return HttpResponseRedirect("/admin_login")
    user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    role = Role.objects.get(pk = user.role_id)
    if role.add_sub_category_access != 1:
        return HttpResponseRedirect("/page_not_found")
    
    return render(request, 'admin/sub-category.html', {"role":role,"user":user})

def Admin_Category(request):
    if ReqParams.admin_userid not in request.session:
        return HttpResponseRedirect("/admin_login")
    user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    role = Role.objects.get(pk = user.role_id)
   
    
    return render(request, 'admin/category.html', {"role":role,"user":user})

# merchants
def Create_Merchants(request):

    if ReqParams.admin_userid not in request.session:
        return HttpResponseRedirect("/admin_login")
    user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    role = Role.objects.get(pk = user.role_id)
    if role.add_user_access != 1:
        return HttpResponseRedirect("/page_not_found")
    
    return render(request, 'admin/create_merchants.html', {"role":role,"user":user})

def Approved_Merchants(request):
    if ReqParams.admin_userid not in request.session:
        return HttpResponseRedirect("/admin_login")
    user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    role = Role.objects.get(pk = user.role_id)
    if role.merchant_approved_flag != 1:
        return HttpResponseRedirect("/page_not_found")
    
    return render(request, 'admin/approved_merchants.html', {"role":role,"user":user})


def Pending_Merchants(request):

    if ReqParams.admin_userid not in request.session:
        return HttpResponseRedirect("/admin_login")
    user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    role = Role.objects.get(pk = user.role_id)
    if role.merchant_pending_access != 1:
        return HttpResponseRedirect("/page_not_found")
    
    return render(request, 'admin/pending_merchants.html', {"role":role,"user":user})

def Suspended_Merchants(request):

    if ReqParams.admin_userid not in request.session:
        return HttpResponseRedirect("/admin_login")
    user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    role = Role.objects.get(pk = user.role_id)
    if role.merchant_suspend_access != 1:
        return HttpResponseRedirect("/page_not_found")
    
    return render(request, 'admin/suspended_merchants.html', {"role":role,"user":user})

# admin user
def Admin_Add_User(request):
    if ReqParams.admin_userid not in request.session:
        return HttpResponseRedirect("/admin_login")
    user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    role = Role.objects.get(pk = user.role_id)
    if role.add_user_access != 1:
        return HttpResponseRedirect("/page_not_found")
    
    roles = Role.objects.filter(display_flag = 1)
    department = Department.objects.all()
    if request.method == "POST":
        new_user = System_User()
        new_user.first_name = request.POST.get("firstname")
        new_user.last_name = request.POST.get("lastname")
        new_user.email = request.POST.get("email_address")
        new_user.user_name = request.POST.get("username")
        password = request.POST.get("password")
        # convertion into base64
        passAscii = password.encode("ascii")
        passBytes = base64.b64encode(passAscii)
        new_user.password = passBytes
        new_user.save()
        new_user.id_format = ADMIN_ID_FORMAT(new_user.account_id,"ADMIN")
        if request.POST.get("role"):
            this_role = Role.objects.get(pk = request.POST.get("role"))
            new_user.role_id = request.POST.get("role")
            new_user.role_name = this_role.role_name
        if request.POST.get("department"):    
            this_department = Department.objects.get(pk = request.POST.get("department"))
            new_user.department_id = request.POST.get("department")
            new_user.department_name = this_department.department_name
        new_user.save()

        return HttpResponseRedirect(f"/admin_user/{new_user.account_id}")

    
    return render(request, 'admin/add_user.html', {"roles":roles,"role":role,"user":user,"department":department})

def Admin_View_User(request):

    if ReqParams.admin_userid not in request.session:
        return HttpResponseRedirect("/admin_login")
    user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    role = Role.objects.get(pk = user.role_id)
    if role.user_list_flag != 1:
        return HttpResponseRedirect("/page_not_found")
    all_user = System_User.objects.all()
    return render(request, 'admin/view_user.html', {"role":role,"user":user,"all_user":all_user})

def Admin_Edit_User(request,id):
    
    if ReqParams.admin_userid not in request.session:
        return HttpResponseRedirect("/admin_login")
    user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    role = Role.objects.get(pk = user.role_id)
    if role.edit_user_access != 1:
        return HttpResponseRedirect("/page_not_found")
    
    this_user = System_User.objects.get(pk = id)
    this_role = Role.objects.get(pk = this_user.role_id)
    


    return render(request, 'admin/edit_user.html',{"role":role,"user":user,"this_role":this_role})

def Admin_Archived_User(request):

    if ReqParams.admin_userid not in request.session:
        return HttpResponseRedirect("/admin_login")
    user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    role = Role.objects.get(pk = user.role_id)
    if role.archive_user_access != 1:
        return HttpResponseRedirect("/page_not_found")
    
    return render(request, 'admin/archived_user.html', {"role":role,"user":user})

# role
def Role_Settings(request):
    if ReqParams.admin_userid not in request.session:
        return HttpResponseRedirect("/admin_login")
    user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    role = Role.objects.get(pk = user.role_id)
    if role.role_flag != 1:
        return HttpResponseRedirect("/page_not_found")
    all_roles = Role.objects.filter(display_flag = 1)
    retval = []
    for obj in all_roles:
        retval.append({
            "id":obj.id,
            "id_format":obj.id_format,
            "role_name":obj.role_name,
            "num_of_users":System_User.objects.filter(role_id = obj.id).count()
        })
    return render(request, 'admin/role.html', {"role":role,"user":user,"retval":retval})

def Add_Role_Settings(request):

    if ReqParams.admin_userid not in request.session:
        return HttpResponseRedirect("/admin_login")
    user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    role = Role.objects.get(pk = user.role_id)
    if role.add_role_access != 1:
        return HttpResponseRedirect("/page_not_found")
    
    return render(request, 'admin/add_role.html', {"role":role,"user":user})

def Edit_Role_Settings(request,id):

    if ReqParams.admin_userid not in request.session:
        return HttpResponseRedirect("/admin_login")
    user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    role = Role.objects.get(pk = user.role_id)
    this_role = Role.objects.get(pk = id)
    if role.edit_role_access != 1:
        return HttpResponseRedirect("/page_not_found")
    
    return render(request, 'admin/edit_role.html', {"role":role,"user":user,"this_role":this_role})

def View_Role_Settings(request,id):

    if ReqParams.admin_userid not in request.session:
        return HttpResponseRedirect("/admin_login")
    user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    role = Role.objects.get(pk = user.role_id)
    this_role = Role.objects.get(pk = id)
    if role.role_flag != 1:
        return HttpResponseRedirect("/page_not_found")
    
    return render(request, 'admin/view_role.html',  {"role":role,"user":user,"this_role":this_role})

# department
def Department_Settings(request):

    if ReqParams.admin_userid not in request.session:
        return HttpResponseRedirect("/admin_login")
    user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    role = Role.objects.get(pk = user.role_id)
    if role.department_flag != 1:
        return HttpResponseRedirect("/page_not_found")
    
    return render(request, 'admin/department.html', {"role":role,"user":user})

def View_Department_Settings(request):

    if ReqParams.admin_userid not in request.session:
        return HttpResponseRedirect("/admin_login")
    user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    role = Role.objects.get(pk = user.role_id)
    if role.department_flag != 1:
        return HttpResponseRedirect("/page_not_found")
    
    return render(request, 'admin/view_department.html', {"role":role,"user":user})

def Edit_Department_Settings(request):

    if ReqParams.admin_userid not in request.session:
        return HttpResponseRedirect("/admin_login")
    user = System_User.objects.get(pk = request.session.get(ReqParams.admin_userid))
    role = Role.objects.get(pk = user.role_id)
    if role.edit_department_access != 1:
        return HttpResponseRedirect("/page_not_found")
    
    return render(request, 'admin/edit_department.html', {"role":role,"user":user})


def check_email_admin(request):
    context = {}

    if request.method == "POST":
        this_email = request.POST["value"]
        if System_User.objects.filter(email=this_email).exists():
            context["success"] = 1
        else:
            context["success"] = 0

    return HttpResponse(json.dumps(context), "application/json")

def check_username_admin(request):
    context = {}

    if request.method == "POST":
        this_username = request.POST["value"]
        if System_User.objects.filter(user_name = this_username).exists():
            context["success"] = 1
        else:
            context["success"] = 0

    return HttpResponse(json.dumps(context), "application/json")



