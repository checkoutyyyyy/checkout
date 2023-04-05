from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, Functions, EmercadoUtil, password, Merchant, PhoneFunction ,AdminFunctions
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

     path('index', views.IndexPage, name='index'),

     path('', views.EmercadoPage, name='emercado'),
     path('login', views.LoginPage, name='login'),
     path("login_verification/<str:token>/", views.Login_Verification_Page, name='login_verification'),
     path('dine', views.DinePage, name='dine'),
     path('loading_spinner', views.loading_spinner, name='loading_spinner'),

     path('signup', views.SignupPage, name='signup'),
     path("check_email", views.check_email),
     path("check_username", views.check_username),
     path("run_script", Functions.run_script),

     path('store/<str:id>', views.StorePage, name='store'),
     path('store/<str:id>/add_item/order=<str:order_id>', Functions.add_item_to_order, ),
     path('menu/<str:id>', views.MenuPage, name='menu'),
     path('error_page', views.Error_Page, name='error_page'),
     path('featured_items', views.Featured_Items, name='featured_items'),
     path('tracking', views.TrackingPage, name='tracking'),
     path('coupons', views.CouponsPage, name='coupons'),
     path('rewards', views.RewardsPage, name='rewards'),
     path('my_purchases', views.MyPurchase_Page, name='my_purchases'),
     path('request_share_order', Functions.request_share_order, ),
     path('view_cart', views.Cart_Items_Page, name='cart_items'),
     path('remove_cart_item', Functions.remove_cart_item),
     path('notifications', views.Notification_Page, name='notifications'),
     path('remove_notif', Functions.remove_notif),
     

    path('unread_notifications', Functions.unread_notifications),
    path('read_notifications', Functions.read_notifications),
    path('unread_notifications_merchant', Functions.unread_notifications_merchant),
    path('read_notifications_merchant', Functions.read_notifications_merchant),
    path('store_feature', views.Store_Feature_Page, name="store_feature"),
    path('user_profile', views.User_Profile_Page, name="user_profile"),

     path('add_to_order_modal', views.Add_To_Order_ModalPage, name='add_to_order_modal'),
     
     path('shared_order/<str:id>', views.Display_Share_OrderPage, name='display_share_order'),
     path('accept_request', Functions.accept_request),
     path('denied_request', Functions.denied_request),
     path('request_shared_order/<str:id>', views.request_shared_order, name="logout"),
     path('logout', views.LogoutPage, name="logout"),


    #admin
     path('admin_login',AdminFunctions.Admin_LoginPage),
     path('admin_dashboard', AdminFunctions.Admin_Dashboard),
     path('reports', AdminFunctions.Reports),
     path('discounted_personnel', AdminFunctions.Discounted_Personnel_Page),
     path('view_shop_vouchers', AdminFunctions.View_ShopVoucher_Page),
     path('view_product_vouchers', AdminFunctions.View_ProductVoucher_Page),
     path('add_discount_personnel', AdminFunctions.add_discount_personnel),
     path('personnel_discount/request=<str:id>', Merchant.Discount_Requests),
     path('check_personnel_status', AdminFunctions.check_personnel_status),
     path('edit_discount_personnel', AdminFunctions.edit_discount_personnel),
     path('delete_discount_personnel', AdminFunctions.delete_discount_personnel),
     path('administrator/create_merchants', AdminFunctions.Create_Merchants),
     path('administrator/approved_merchants',AdminFunctions.Approved_Merchants),
     path('administrator/pending_merchants',AdminFunctions.Pending_Merchants),
     path('administrator/suspended_merchants',AdminFunctions.Suspended_Merchants),

     path('admin_category', AdminFunctions.Admin_Category),
     path('sub-category', AdminFunctions.Admin_SubCategory),

     path('admin_view_user', AdminFunctions.Admin_View_User),
     path('admin_add_user', AdminFunctions.Admin_Add_User),
     path('admin_user/<str:id>', AdminFunctions.Admin_Edit_User),
     path('admin_archived_user', AdminFunctions.Admin_Archived_User),

     path('role_settings', AdminFunctions.Role_Settings),
     path('addrole_settings', AdminFunctions.Add_Role_Settings),
     path('editrole_settings/<str:id>', AdminFunctions.Edit_Role_Settings),
     path('viewrole_settings/<str:id>', AdminFunctions.View_Role_Settings),

     path('department_settings', AdminFunctions.Department_Settings),
     path('view_department_settings', AdminFunctions.View_Department_Settings),
     path('edit_department_settings', AdminFunctions.Edit_Department_Settings),
     path('check_username_admin', AdminFunctions.check_username_admin),
     path('check_email_admin', AdminFunctions.check_email_admin),


    # consumer
    path('password_reset', password.Forgot_Password, name="password_reset"),
    path('password_reset_sent', password.Forgot_Password_Sent,
         name="password_reset_sent"),
    path('password_reset_confirm/<str:token>/',
         password.Forgot_Password_Confirm, name="password_reset_confirm"),
    path('password_reset_complete', password.Forgot_Password_Complete,
         name="password_reset_complete"),


    # merchant
    
    path('add_product_vouchers', Merchant.add_product_vouchers),
    path('edit_variant_price', Merchant.edit_variant_price),
    path('varaint_available_switch', Merchant.varaint_available_switch),
    path('edit_variant_stocks', Merchant.edit_variant_stocks),
    path('delete_variant', Merchant.delete_variant),
    path('add_shop_vouchers', Merchant.add_shop_vouchers),
    path('merchant/password_reset', password.Merchant_Forgot_Password,
         name="merchant/password_reset"),
    path('merchant/password_reset_sent', password.Merchant_Forgot_Password_Sent,
         name="merchant/password_reset_sent"),
    path('merchant/password_reset_confirm/<str:token>/',
         password.Merchant_Forgot_Password_Confirm, name="merchant/password_reset_confirm"),
    path('merchant/password_reset_complete', password.Merchant_Forgot_Password_Complete,
         name="merchant/password_reset_complete"),

     
     path('accept_discount_request', Merchant.accept_discount_request, ),
     path('reject_discount_request', Merchant.reject_discount_request, ),
     path('register_as_seller', Functions.owner_signup, name='store_signup'),
     path("check_email_seller", Merchant.check_email),
     path("check_username_seller", Merchant.check_username),
     path("check_email", views.check_email),
     path("check_username", views.check_username),
     path("merchant/login", Functions.merchant_login),
     path("seller/dashboard", Functions.dashboard),
     path("seller/add_new_store", Functions.add_new_store),
     path("page_not_found", Functions.page_not_found),
     path("set_browse_img", EmercadoUtil.set_browse_img),

     path("seller/profile", Functions.profile),
     path("get_variant_price", Functions.get_variant_price),
     path("add_to_cart", Functions.add_to_cart),   
     path("add_to_order", Functions.add_to_order),
     path("check_user_login", Functions.check_user_login),
     path("checkout", Functions.Checkout),
     path("quick_place_order", Functions.quick_place_order),
     path("redirect_login", Functions.redirect_login),
     path("select_cart_obj", Functions.select_cart_obj),
     path("update_quatity", Functions.update_quatity),
     path("check_phone", Functions.check_phone),
     path("quick_checkout", Functions.quick_checkout),
     path("checkout_items", Functions.checkout_items),
     path("checkout_all", Functions.checkout_all),
     path("update_variation", Functions.update_variation),
     path("user/purchase", Functions.order_list),
     path("user/purchase/key=<str:id>", Functions.anonymous_order_list),
     path("get_cart_total", Functions.get_cart_total),
     path("check_available_product", Functions.check_available_product),
     path("check_quantity", Functions.check_quantity),
     path("check_variations", Functions.check_variations),
     path("disable_cart_variation", Functions.disable_cart_variation),
     path("disable_product_variation", Functions.disable_product_variation),
     path("available_switch", Functions.available_switch),
     path("disable_product", Functions.disable_product),
     path("drag_order_status", Functions.drag_order_status),



     path("seller/my_store/<str:id>/add_new_item", Functions.add_new_item),
     path("seller/setup_variations/product_id=<str:id>",
          Functions.setup_variations),

     path("seller/profile", Functions.profile),
     path("get_variant_price", Functions.get_variant_price),
     path("add_to_cart", Functions.add_to_cart),
     path("check_user_login", Functions.check_user_login),
     path("checkout/shop_id=<str:id>", Functions.Checkout),
     path("quick_place_order", Functions.quick_place_order),
     path("redirect_login", Functions.redirect_login),
     path("select_cart_obj", Functions.select_cart_obj),
     path("update_quatity", Functions.update_quatity),
     path("check_phone", Functions.check_phone),
     path("quick_login", Functions.quick_login),



     path("seller/my_store/add_new_item", Functions.add_new_item),
     path("remove_order_item", Functions.remove_order_item),
     path("seller/my_store/product_addons", Functions.product_addons),
     path("seller/my_store/product_archive", Functions.product_archive),
     path("seller/my_store/product_list", Functions.product_list),
     path("seller/my_store/discounted_product", Functions.discounted_product),
     path("request_discount", Functions.request_discount),
     path("requested_discounts", Functions.Requested_Discounts),
     path("seller/setup_variations/product_id=<str:id>",
          Functions.setup_variations),
     path("seller/my_store/product_id=<str:id>/product_details",
          Functions.product_details),
     path("seller/my_store/<str:id>/archive_item", Functions.archive_item),
     path("seller/my_store/<str:id>/restore_item", Functions.restore_item),

     path('seller/my_store/notifications', Functions.Store_Notification_Page),

     path("seller/my_store/order_details/<str:id>", Functions.order_details),

     path("seller/orders/orders_list/pick_up_list", Functions.Order_Pick_Up_List),
     path("seller/orders/orders_list/pick_up_tile", Functions.Order_Pick_Up_Tile),

     path("seller/orders/orders_list/dine_in_list", Functions.Order_Dine_In_List),
     path("seller/orders/orders_list/dine_in_tile", Functions.Order_Dine_In_Tile),

     path("seller/orders/orders_list/delivery_list",Functions.Order_Delivery_List),
     path("seller/orders/orders_list/delivery_tile",Functions.Order_Delivery_Tile),

     path("seller/product_vouchers",Functions.Product_Vouchers),
     path("seller/shop_vouchers",Functions.Shop_Vouchers),

     path("seller/store_reports", Functions.StoreReports),
     
     path("seller/add_staff", Functions.Add_Staff),
     path("seller/view_staff", Functions.View_Staff),
     path("seller/edit_staff", Functions.Edit_Staff),


     path('logout_seller', Functions.Logout, name="Logout"),
     path('send_email', EmercadoUtil.send_email, ),


     # merchant
     path("merchant/register", Merchant.Merchant_Register),
     path('register_successful', Merchant.Merchant_Register_Successful),

     # login using phonenumber
     path("login_phonenum", PhoneFunction.LoginPage_PhoneNumber),
     path("login_verify_code", PhoneFunction.VerificationPage_CodeNumber),
     # forgot number
     path('login_forgot_number', PhoneFunction.Login_Forgot_Number,
          name="login_forgot_number"),
     path('login_forgot_number_sent', PhoneFunction.Login_Forgot_Number_Sent,
          name="login_forgot_number_sent"),
     path("login_forgot_number_reset/<token>/",
          PhoneFunction.Login_Forgot_Number_Reset, name="login_forgot_number_reset"),
     path("login_forgot_number_done", PhoneFunction.Login_Forgot_Number_Done,
          name="login_forgot_number_done"),
     path("login_forgot_number_code", PhoneFunction.Login_Forgot_Number_Code,
          name="login_forgot_number_code"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
