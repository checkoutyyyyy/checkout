from django.db import models
from django.utils import timezone
from datetime import date
import os
import datetime



# Create your models here.


class Consumer(models.Model):
    account_id = models.BigAutoField( primary_key = True)
    email = models.EmailField(max_length=255,  unique=True)
    first_name = models.CharField(max_length = 45, blank = True, null = True)
    last_name = models.CharField(max_length = 45, blank = True, null = True)
    address = models.CharField(max_length = 45, blank = True, null = True)
    phone_number1 = models.CharField(max_length=45)
    # phone_number2 = models.CharField(max_length=45,null= True,blank = True)
    user_name = models.CharField(max_length=45)
    password = models.BinaryField()
    id_format = models.CharField(default="",max_length=45)
    reset_password_token = models.CharField(max_length=45,null = True)
    reset_password_token_expiry = models.DateTimeField(null=True)
    reset_number_token = models.CharField(max_length=45,null = True)
    reset_number_token_expiry = models.DateTimeField(null=True)
    account_verification_code = models.CharField(max_length=45,null = True)
    account_verification_expiry = models.DateTimeField(null=True)
    account_verification_flag = models.IntegerField(default = 0)
    profile_picture = models.ImageField(default="profile_default.jpg", null=True, blank=True)
    qr_code = models.ImageField(max_length=120, blank=True)


    def __str__(self):
        return self.account_id

    class Meta:
        db_table = 'emcdo_consumer_info'

# class Store_Owner(models.Model):
#     account_id = models.CharField( primary_key = True,max_length=45)
#     email = models.EmailField(max_length=255,  unique=True)
#     first_name = models.CharField(max_length = 45)
#     last_name = models.CharField(max_length = 45)
#     address = models.CharField(max_length = 120)
#     phone_number1 = models.CharField(max_length=45)
#     phone_number2 = models.CharField(max_length=45,null= True,blank = True)
#     user_name = models.CharField(max_length=45)
#     password = models.BinaryField()
#     reset_password_token = models.CharField(max_length=45,null = True)
#     reset_password_token_expiry = models.DateTimeField(null=True)
#     custom_attributes = models.TextField(default="",null=True)
#     custom_category = models.TextField(default="",null=True)

#     def __str__(self):
#         return self.account_id

#     class Meta:
#         db_table = "emcdo_store_owner_info"
    
# class Merchant_Owner(models.Model):
#     merchant_id = models.AutoField( primary_key= True)
#     email = models.EmailField(max_length=255,  unique=True)
#     first_name = models.CharField(max_length = 45)
#     last_name = models.CharField(max_length = 45)
#     user_name = models.CharField(max_length=45)
#     address = models.CharField(max_length = 120)
#     store_address = models.CharField( max_length=120)
#     phone_number = models.CharField(max_length=45)
#     business_name = models.CharField(max_length=120)
#     store_link = models.CharField( max_length=120)
#     store_category = models.CharField( max_length=120)
#     password = models.BinaryField()
#     reset_password_token = models.CharField(max_length=45,null = True)
#     reset_password_token_expiry = models.DateTimeField(null=True)
#     custom_attributes = models.TextField(default="",null=True)
#     custom_category = models.TextField(default="",null=True)
#     reset_number_token = models.CharField(max_length=45,null = True)
#     reset_number_token_expiry = models.DateTimeField(null=True)
#     profile_picture = models.ImageField(upload_to='profile/img', default="profile_default.jpg", null=True, blank=True)
#     profile_pic = models.CharField(max_length=120,default="")

#     def __str__(self):
#         return self.merchant_id

#     class Meta:
#         db_table = "emcdo_merchant_owner_info"

class Store_Info(models.Model):
    store_id = models.BigAutoField( primary_key = True)
    id_format = models.CharField(default="",max_length=45)
    store_name = models.CharField( max_length=45)
    branch_name  = models.CharField( max_length=120)
    store_address1 = models.CharField( max_length=120)
    store_address2 = models.CharField( max_length=300,default="")
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    distance_from_user = 0.0
    store_category = models.CharField( max_length=120)
    # owner_id = models.ForeignKey(Store_Owner,on_delete = models.CASCADE,default = "")
    store_link = models.CharField( max_length=120)
    phone_number = models.CharField( max_length=120)
    store_phone_number = models.CharField( max_length=120,default="")
    email_address = models.CharField( max_length=120)
    profile_pic = models.CharField(max_length=120, default="cart_logo.png", null=True, blank=True) #store Profile
    profile_picture = models.ImageField(default="profile_default.jpg", null=True, blank=True)#store owner Profile
    first_name = models.CharField(max_length = 45,default="")
    last_name = models.CharField(max_length = 45,default="")
    user_name = models.CharField(max_length=45,default="")
    password = models.BinaryField(null=True)
    reset_password_token = models.CharField(max_length=45,null = True)
    reset_password_token_expiry = models.DateTimeField(null=True)
    reset_number_token = models.CharField(max_length=45,null = True)
    reset_number_token_expiry = models.DateTimeField(null=True)
    status = models.IntegerField(default = 0)
    qr_code = models.ImageField(max_length=120, blank=True)

    def __str__(self):
        return self.store_id

    class Meta:
        db_table = "emcdo_store_info"

class Products(models.Model):
    product_id = models.BigAutoField( primary_key = True)
    id_format = models.CharField(default="",max_length=45)
    product_name = models.CharField( max_length=120)
    description = models.TextField(default="")
    product_category = models.TextField()
    has_variation = models.IntegerField( default = 0)
    default_image = models.CharField( max_length=120)
    store_id = models.ForeignKey(Store_Info,on_delete = models.CASCADE,default = "")
    original_price = models.FloatField(default = 1)
    available_flag = models.IntegerField(default=0) #available switch
    stock  = models.IntegerField( default=0)
    sku   = models.CharField( max_length=120)
    weight = models.FloatField(default=0,null=True)
    status_type = models.IntegerField(default=0)
    is_archived = models.BooleanField(default=False)
    is_available = models.IntegerField(default=1)
    display_flag = models.IntegerField(default=0)
    qr_code = models.ImageField(max_length=120, blank=True)
    
    def __str__(self):
        return self.product_id

    class Meta:
        db_table = "emcdo_products"

class Product_Attributes(models.Model):
    id = models.BigAutoField( primary_key= True)
    attribute_name = models.CharField( max_length=45)
    product_id  = models.IntegerField(default=0)

    # def __str__(self):
    #     return self.id

    class Meta:
        db_table = "emcdo_product_attributes"

class Product_Attributes_Option(models.Model):
    id = models.BigAutoField( primary_key= True)
    option_name = models.CharField( max_length=45)
    attribute_id  = models.IntegerField(default=0)

    # def __str__(self):
    #     return self.id

    class Meta:
        db_table = "emcdo_product_attributes_options"

class Product_Variations(models.Model):   #options
    id = models.BigAutoField( primary_key= True)
    option_id = models.TextField()
    options_name = models.TextField(default="")
    attribute_id = models.TextField()
    available_flag = models.IntegerField(default=1)
    product_id = models.ForeignKey(Products,on_delete = models.CASCADE,default = "")
    price = models.FloatField(default=0)
    stocks = models.IntegerField(default=0)
    image = models.CharField(max_length=120,null=True,default = "")
    status_type = models.IntegerField( default=0)

    def __str__(self):
        return self.id

    class Meta:
        db_table = "emcdo_product_variations"


class Product_Images(models.Model):

    id = models.BigAutoField( primary_key= True)
    file_name = models.CharField( max_length=150)
    product_id  = models.ForeignKey(Products,on_delete = models.CASCADE,default = "")

    def __str__(self):
        return self.id

    class Meta:
        db_table = "emcdo_product_images"

class Product_AddOns(models.Model):
    id = models.BigAutoField( primary_key= True)
    product_name = models.CharField( max_length=150)
    available_flag = models.IntegerField(default=0)
    product_id = models.ForeignKey(Products,on_delete = models.CASCADE,default = "")
    price = models.FloatField(default=0)
    stocks = models.IntegerField(default=0)
    image = models.CharField(max_length=120,null=True)
    status_type = models.IntegerField(default=0)

    def __str__(self):
        return self.id

    class Meta:
        db_table = "emcdo_product_add_ons"


class Cart(models.Model):
    id = models.BigAutoField( primary_key= True)
    product_id = models.CharField(max_length=45)
    product_image = models.CharField(max_length=120,null=True)
    product_name = models.CharField(max_length=120,null=True)
    account_id = models.CharField(max_length=45,null=True)
    store_id = models.CharField(max_length=20)
    price = models.FloatField(default = 0)
    total = models.FloatField(default = 0)
    quantity = models.IntegerField(default=0)
    variation_id = models.CharField(max_length=20,null=True)
    variation_name = models.CharField(max_length=120,null=True)
    addon_id = models.TextField(null=True)
    addon_product_name = models.TextField(null=True)
    date_added = models.DateTimeField()
    cart_key = models.IntegerField(default=0)



    class Meta:
        db_table = "emcdo_cart"

class Cart_Key(models.Model): # A key to group the product via store / branches
    id = models.BigAutoField(primary_key= True)
    account_id = models.CharField(max_length=45)
    store_id = models.CharField(max_length=20)

    class Meta:
        db_table = "emcdo_cart_key"


class Orders(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    id_format = models.CharField(default="",max_length=45)
    subtotal = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    shipping_fee = models.FloatField(default=0)
    service_fee = models.FloatField(default=0)
    online_payment_charge = models.FloatField(default=0)
    total = models.FloatField(default=0)
    items = models.IntegerField(default=0)
    account_id = models.CharField(max_length=120)
    store_id = models.CharField(max_length=20)
    order_status = models.CharField(max_length=45)
    date_created = models.DateTimeField(null=True)
    date_paid = models.DateTimeField(null=True)
    date_completed = models.DateTimeField(null=True)
    service_flag = models.IntegerField(default = 0)
    date_service = models.DateField(null = True)
    date_time_service = models.TimeField(null=True)
    service_instructions = models.TextField(null=True)
    fullname = models.CharField(max_length=120,default="")
    email_address = models.CharField(max_length=120,default="")
    phone = models.CharField(max_length=120,default="")
    profile_picture = models.CharField(max_length=120,default="")
    qr_code = models.ImageField(max_length=120, blank=True)
    personnel_discount_id = models.IntegerField(null=True)
    personnel_status = models.CharField(max_length=120,null=True)
    percentage_discount = models.FloatField(default=0)
    discounted_flag = models.IntegerField(default=0)
    total_personnel_discount = models.FloatField(default=0)
    voucher_discount = models.FloatField(default=0)
    shared_to = models.TextField(null = True,default="")

    class Meta:
        db_table = "emcdo_orders"

class Line_Items(models.Model):# list of products or an order
    id = models.BigAutoField(primary_key=True)
    product_id = models.CharField(max_length=45)
    variation_id = models.CharField(max_length=45,null=True)
    add_on_id = models.CharField(max_length=45,null=True)
    quantity = models.IntegerField()
    order_id = models.CharField(max_length=45)

    class Meta:
        db_table = "emcdo_line_items"


class System_User(models.Model):
    account_id = models.BigAutoField(primary_key=True)
    id_format = models.CharField(max_length=45,null=True)
    first_name = models.CharField(max_length=45,null=True)
    last_name = models.CharField(max_length=45,null=True)
    phone = models.CharField(max_length=45,null=True)
    email = models.CharField(max_length=45,null=True)
    user_name = models.CharField(max_length=45,null=True)
    password = models.BinaryField(null=True)
    role_id = models.IntegerField(default=0,null=True)
    department_id = models.IntegerField(default=0,null=True)
    role_name = models.CharField(max_length=45,null=True)
    department_name = models.CharField(max_length=45,null=True)
    date_created = models.DateTimeField(null=True)

    class Meta:
        db_table = "emcdo_system_user"


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    id_format = models.CharField(max_length=45)
    role_name = models.CharField(max_length=45)
    dashboard_view_access = models.IntegerField(default=0)
    report_view_access = models.IntegerField(default=0)
    merchant_pending_access = models.IntegerField(default=0)
    merchant_approved_flag = models.IntegerField(default=0)
    merchant_approved_view_access = models.IntegerField(default=0)
    merchant_suspend_access = models.IntegerField(default=0)
    create_merchant_access = models.IntegerField(default=0)
    suspended_access_flag = models.IntegerField(default=0)
    suspended_restore_access = models.IntegerField(default=0)
    suspended_delete_access = models.IntegerField(default=0)
    add_categories_access = models.IntegerField(default=0)
    add_sub_category_access = models.IntegerField(default=0)
    add_user_access = models.IntegerField(default=0)
    user_list_flag = models.IntegerField(default=0)
    edit_user_access = models.IntegerField(default=0) 
    archive_user_access = models.IntegerField(default=0)
    archived_user_flag = models.IntegerField(default=0)
    restore_archive_user_access = models.IntegerField(default=0)
    delete_archive_user_access = models.IntegerField(default=0)
    role_flag = models.IntegerField(default=0)
    edit_role_access = models.IntegerField(default=0)
    add_role_access = models.IntegerField(default=0)
    delete_role_access = models.IntegerField(default=0)
    department_flag = models.IntegerField(default=0)
    edit_department_access = models.IntegerField(default=0)
    add_department_acccess = models.IntegerField(default=0)
    delete_department_access = models.IntegerField(default=0)
    discounts_access = models.IntegerField(default=0)
    display_flag = models.IntegerField(default=1)


    class Meta:
        db_table = "emcdo_role"

class Discount_Personnel(models.Model):

    id = models.AutoField(primary_key=True)
    id_format = models.CharField(max_length=45)
    personnel_status = models.CharField(max_length=120)
    discount_percentage = models.FloatField(default=0)

    class Meta:
        db_table = "emcdo_discount_personnel"


class Department(models.Model): 
    id = models.AutoField(primary_key=True)
    id_format = models.CharField(max_length=45)
    department_name = models.CharField(max_length=120,null=True)
    description = models.TextField()

    class Meta:
        db_table = "emcdo_department"       

class Notifications(models.Model):
    id = models.BigAutoField(primary_key=True)
    consumer_id = models.IntegerField(null=True)
    consumer_id_format = models.CharField(max_length=45,null=True)
    requesting_share_order = models.IntegerField(null=True)
    requesting_discount = models.IntegerField(null=True)
    requesting_id_format = models.CharField(max_length=45,null=True)
    requesting_name =  models.CharField(max_length=45,null=True)
    requested_response = models.CharField(max_length=45,null=True)
    account_responded = models.IntegerField(null=True) # account responded to a request. it can be costumer, merchant or admin 
    account_responded_id_format = models.CharField(max_length=45,null=True)
    account_responded_name = models.CharField(max_length=45,null=True)
    order_id =  models.IntegerField(null=True)  
    order_id_format = models.CharField(max_length=45,null=True)
    merchant_id = models.IntegerField(null=True)
    merchant_id_format = models.CharField(max_length=45,null=True)
    content = models.TextField(null=True)
    image = models.CharField(max_length=50,null=True)
    notif_type = models.CharField(max_length=50)
    date_time = models.DateTimeField()
    url = models.CharField(max_length=120)
    read = models.IntegerField(default=0)

    class Meta:
        db_table = "emcdo_notification"  

class Personnel_Discount_Requests(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_format = models.CharField(max_length=45,null=True)
    consumer_id = models.IntegerField(null=True)
    consumer_id_format = models.CharField(max_length=45,null=True)
    order_id = models.IntegerField(null=True)
    order_id_format = models.CharField(max_length=45,null=True)
    personnel_discount_id = models.IntegerField(null=True)
    personnel_discount_id_format = models.CharField(max_length=45,null=True)
    personnel_status = models.CharField(max_length=45,null=True)
    store_id = models.IntegerField(null=True)
    store_id_format = models.CharField(max_length=45,null=True)
    file = models.CharField(max_length=120,null=True)

    class Meta:
        db_table = "emcdo_personnel_discount_requests"  
    
class Vouchers(models.Model):    
    id = models.BigAutoField(primary_key=True)
    id_format = models.CharField(max_length=45,null=True)
    voucher_name = models.CharField(max_length=120)
    store_id = models.IntegerField(null=True)
    store_id_format = models.CharField(max_length=45,null=True)
    reward_type = models.CharField(max_length=45,null=True) #Discount or Freebies/Gift and etc.
    voucher_type = models.CharField(max_length=45) #Shop or Product Voucher
    discount_type = models.CharField(max_length=45) #Fix amount ot Percentage
    discount_percentage = models.FloatField(null=True)
    fix_amount_discount = models.FloatField(null=True)
    minimum_spend = models.FloatField(null=True)
    product_list = models.TextField(null=True) # if product Vouchers
    date_start = models.DateField()
    time_start = models.TimeField(null=True)
    date_end = models.DateField()
    time_end = models.TimeField(null=True)
    usage_quantity = models.IntegerField(default=0)
    total_usage = models.IntegerField(default=0)
    status = models.CharField(max_length=120) #Ongoing or Expired

    class Meta:
        db_table = "emcdo_vouchers" 