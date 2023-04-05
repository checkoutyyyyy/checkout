function ValidateEmail(inputText){
    var mailformat = /^\w+([\.-]\w+)*@\w+([\.-]\w+)*(\.\w{2,3})+$/;
    if(inputText.value.match(mailformat)){
        return true;
    }else{
        return false;
    }
}

function CurrencyConverter(amount){
    var formatter = new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'PHP',

    });
    return formatter.format(amount);
  }

function ismatch(p1,p2){
    retval = false
    if(p1 == p2){
        retval = true;
    }else{
        retval = false
    }
    return retval
  }

  function check_email(){
    var retval = 0

      var email = document.getElementById("email");
      if(email.value != "" ){
          if(ValidateEmail(email) == true ){
              document.getElementById("email_msg").innerHTML = "";
              retval = 1
              // nxtbtn.disabled = false;
          }else{
              document.getElementById("email_msg").innerHTML = "invalid format.";
              retval = 0
              // nxtbtn.disabled = true;
          }
       }else{
          document.getElementById("email_msg").innerHTML = "Please enter your Email";
          retval = 0
          // nxtbtn.disabled = true;
      }
      return retval
  }


function ValidatePhone(p) {
    var phoneRe =/^(09|\+639)\d{9}$/g
    var digits = p;
    return phoneRe.test(digits);
  }


function register_owner(){
    var fname = document.getElementById("fname")
    var lname = document.getElementById("lname")
    var user_name = document.getElementById("user_name")
    var pass1 = document.getElementById("password")
    var pass2 = document.getElementById("confirm_password")
    var phone1 = document.getElementById("phone_number")
    var other_phone = document.getElementById("phone_number2")
    var btn = document.getElementById("submit_btn")
    var email = document.getElementById("email")
    var address = document.getElementById("address")
    var flag = 0
    var match = 0
    if(fname.value != "" && lname.value != "" && user_name.value != "" && pass1.value != "" && pass2.value != "" && phone1.value != "" && email.value != "" && address.value != ""){

    }else{
        flag = flag + 1
    }
    if(email.value != ""){
        var validate_email = check_email()
                  if(validate_email == 1){
                      $.ajax({
                          url:"/check_email_seller",
                          type:"POST",
                          cache: false,
                          // async:true;
                          data:{csrfmiddlewaretoken: token,value:document.getElementById("email").value},
                          success: function(context) {
                              if(context.success == 1){
                                    document.getElementById("email_msg").innerHTML = " already been used!";
                                    btn.disabled = true;
                              }else{

                                    document.getElementById("email_msg").innerHTML = "";
                              }

                          }
                      });
                  }else{
                    flag = flag + 1
                    match = match + 1
                  }

    }else{
        flag = flag + 1
        document.getElementById("email_msg").innerHTML = "";
    }

    if(user_name.value != ""){
        $.ajax({
            url:"/check_username_seller",
            type:"POST",
            cache: false,
            // async:true;
            data:{csrfmiddlewaretoken: token,value:document.getElementById("user_name").value},
            success: function(context) {
                if(context.success == 1){
                    document.getElementById("username_msg").innerHTML = " already been used!";
                    btn.disabled = true;
                }else{

                    document.getElementById("username_msg").innerHTML = "";
                }

            }
        });

    }else{
        flag = flag + 1
        document.getElementById("username_msg").innerHTML = "";
    }
    if(phone1.value != ""){
        if(ValidatePhone(phone1.value) == false){
            flag = flag + 1
            document.getElementById("phone1_msg").innerHTML = " Invalid Format!";
        }else{
            document.getElementById("phone1_msg").innerHTML = "";
        }
    }else{
        flag = flag + 1
    }

    if(other_phone.value != ""){
        if(ValidatePhone(other_phone.value) == false){
            flag = flag + 1
            document.getElementById("phone2_msg").innerHTML = " Invalid Format!";
        }else{
            document.getElementById("phone2_msg").innerHTML = "";
        }
    }else{
        document.getElementById("phone2_msg").innerHTML = "";
    }
    var password = document.getElementById("password").value
    var lowerCaseLetters = /[a-z]/g;
    // var upperCaseLetters = /[A-Z]/g;
     // && password.match(upperCaseLetters)
    var numbers = /[0-9]/g;
    var special_character =  /[A-Z]/g;
    if(pass1.value != ""){
        if(password.match(lowerCaseLetters) && password.match(numbers) && password.length >= 8 && password.match(special_character)){
            if(pass1.value === pass2.value){

                document.getElementById("password_msg").innerHTML = "Passwords match!";
                document.getElementById("password_msg").style.color = "green";


            }else{
                document.getElementById("password_msg").innerHTML = "Passwords did not match!";
                document.getElementById("password_msg").style.color = "red";
                flag = flag + 1
            }
        }else{
            document.getElementById("password_msg").innerHTML = "Make sure it's at least 8 characters. Must include at least one number," + " a lowercase " + "and an uppercase letter.";
            document.getElementById("password_msg").style.color = "red";
            flag = flag + 1
        }
    }else{
        flag = flag + 1
    }



    if(flag != 0 || match != 0){
        btn.disabled = true;
    }else{
        btn.disabled = false;
    }
}

function register_consumer(){
    var fname = document.getElementById("fname")
    var lname = document.getElementById("lname")
    var user_name = document.getElementById("user_name")
    var pass1 = document.getElementById("password")
    var pass2 = document.getElementById("confirm_password")
    var phone1 = document.getElementById("phone_number")
    var other_phone = document.getElementById("phone_number2")
    var btn = document.getElementById("submit_btn")
    var email = document.getElementById("email")
    var address = document.getElementById("address")
    var flag = 0
    var match = 0
    if(fname.value != "" && lname.value != "" && user_name.value != "" && pass1.value != "" && pass2.value != "" && phone1.value != "" && email.value != "" && address.value != ""){

    }else{
        flag = flag + 1
    }
    if(email.value != ""){
        var validate_email = check_email()
                  if(validate_email == 1){
                      $.ajax({
                          url:"/check_email",
                          type:"POST",
                          cache: false,
                          // async:true;
                          data:{csrfmiddlewaretoken: token,value:document.getElementById("email").value},
                          success: function(context) {
                              if(context.success == 1){
                                    document.getElementById("email_msg").innerHTML = " already been used!";
                                    btn.disabled = true;
                              }else{

                                    document.getElementById("email_msg").innerHTML = "";
                              }

                          }
                      });
                  }else{
                    flag = flag + 1
                    match = match + 1
                  }

    }else{
        flag = flag + 1
        document.getElementById("email_msg").innerHTML = "";
    }

    if(user_name.value != ""){
        $.ajax({
            url:"/check_username",
            type:"POST",
            cache: false,
            // async:true;
            data:{csrfmiddlewaretoken: token,value:document.getElementById("user_name").value},
            success: function(context) {
                if(context.success == 1){
                    document.getElementById("username_msg").innerHTML = " already been used!";
                    btn.disabled = true;
                }else{

                    document.getElementById("username_msg").innerHTML = "";
                }

            }
        });

    }else{
        flag = flag + 1
        document.getElementById("username_msg").innerHTML = "";
    }
    if(phone1.value != ""){
        if(ValidatePhone(phone1.value) == false){
            flag = flag + 1
            document.getElementById("phone1_msg").innerHTML = " Invalid Format!";
        }else{
            document.getElementById("phone1_msg").innerHTML = "";
            $.ajax({
                url:"/check_phone",
                type:"POST",
                cache: false,
                // async:true;
                data:{csrfmiddlewaretoken: token,value:phone1.value},
                success: function(context) {
                    if(context.success == 1){
                        document.getElementById("phone1_msg").innerHTML = " already been used!";
                        btn.disabled = true;
                    }else{
                        document.getElementById("phone1_msg").innerHTML = "";
                    }

                }
            });
        }
    }else{
        document.getElementById("phone1_msg").innerHTML = "";
        flag = flag + 1
    }

    // if(other_phone.value != ""){
    //     if(ValidatePhone(other_phone.value) == false){
    //         flag = flag + 1
    //         document.getElementById("phone2_msg").innerHTML = " Invalid Format!";
    //     }else{
    //         document.getElementById("phone2_msg").innerHTML = "";
    //     }
    // }else{
    //     document.getElementById("phone2_msg").innerHTML = "";
    // }
    var password = document.getElementById("password").value
    // var lowerCaseLetters = /[a-z]/g;
    // var upperCaseLetters = /[A-Z]/g;
     // && password.match(upperCaseLetters)
    // var numbers = /[0-9]/g;
    // var special_character =  /[A-Z]/g;
    if(pass1.value != ""){
        if( password.length >= 8){
            if(pass1.value === pass2.value){

                document.getElementById("password_msg").innerHTML = "Passwords match!";
                document.getElementById("password_msg").style.color = "green";


            }else{
                document.getElementById("password_msg").innerHTML = "Passwords did not match!";
                document.getElementById("password_msg").style.color = "red";
                flag = flag + 1
            }
        }else{
            document.getElementById("password_msg").innerHTML = "Make sure it's at least 8 characters.";
            document.getElementById("password_msg").style.color = "red";
            flag = flag + 1
        }
    }else{
        flag = flag + 1
    }



    if(flag != 0 || match != 0){
        btn.disabled = true;
    }else{
        btn.disabled = false;
    }
}


function verify_admin(){
    var email = document.getElementById("email")
    var username = document.getElementById("username")
    var btn = document.getElementById("submit_btn")
    good = 0
    if(email.value != ""){
        if(ValidateEmail(email) == false ){
            good = good + 1
            document.getElementById("email_msg").innerHTML = "Invalid Format!";
        }else{
            document.getElementById("email_msg").innerHTML = "";
            $.ajax({
                url:"/check_email_admin",
                type:"POST",
                cache: false,
                // async:true;
                data:{csrfmiddlewaretoken: token,value:document.getElementById("email").value},
                success: function(context) {
                    if(context.success == 1){
                          document.getElementById("email_msg").innerHTML = " already been used!";
                          btn.disabled = true;
                    }else{
                          document.getElementById("email_msg").innerHTML = "";
                    }

                }
            });
        }
    } else{
        good = good + 1
        document.getElementById("email_msg").innerHTML = "";
    }

    if(username.value != ""){
        $.ajax({
            url:"/check_username_admin",
            type:"POST",
            cache: false,
            // async:true;
            data:{csrfmiddlewaretoken: token,value:document.getElementById("username").value},
            success: function(context) {
                if(context.success == 1){
                    document.getElementById("username_msg").innerHTML = " already been used!";
                    btn.disabled = true;
                }else{
                    document.getElementById("username_msg").innerHTML = "";
                }
            }
        });

    } else{
        good = good + 1
        document.getElementById("username_msg").innerHTML = "";
    }

    var password = document.getElementById("pass").value
    var pass2 = document.getElementById("pass2").value
    var lowerCaseLetters = /[a-z]/g;
    //var upperCaseLetters = /[A-Z]/g;
     // && password.match(upperCaseLetters)
    var numbers = /[0-9]/g;
    var special_character =  /[A-Z]/g;
    if(password != ""){
        if( password.match(lowerCaseLetters) && password.match(numbers) && password.length >= 8 && password.match(special_character)){
            if(password === pass2){
                document.getElementById("password_msg").innerHTML = "Passwords match!";
                document.getElementById("password_msg").style.color = "green";
            }else{
                document.getElementById("password_msg").innerHTML = "Passwords did not match!";
                document.getElementById("password_msg").style.color = "red";
                good = good + 1
            }
        }else{
            document.getElementById("password_msg").innerHTML = "Make sure it's at least 8 characters.";
            document.getElementById("password_msg").style.color = "red";
            good = good + 1
        }
    }else{
        good = good + 1
    }

    if(good != 0){
        btn.disabled = true;
    }else{
        btn.disabled = false;
    }

}
function register_merchant(){
    email = document.getElementById("email")
    phone = document.getElementById("phone_number")
    var btn = document.getElementById("submit_btn")
    good = 0
    if(email.value != ""){
        if(ValidateEmail(email) == false ){
            good = good + 1
            document.getElementById("email_msg").innerHTML = "Invalid Format!";
        }else{
            document.getElementById("email_msg").innerHTML = "";
            $.ajax({
                url:"/check_email_seller",
                type:"POST",
                cache: false,
                // async:true;
                data:{csrfmiddlewaretoken: token,value:document.getElementById("email").value},
                success: function(context) {
                    if(context.success == 1){
                          document.getElementById("email_msg").innerHTML = " already been used!";
                          btn.disabled = true;
                    }else{
                          document.getElementById("email_msg").innerHTML = "";
                    }

                }
            });
        }
    } else{
        good = good + 1
        document.getElementById("email_msg").innerHTML = "";
    }
    if(phone.value != ""){
        if(ValidatePhone(phone.value) == false ){
            good = good + 1
            document.getElementById("phone_msg").innerHTML = "Invalid Format!";
        }else{
            document.getElementById("phone_msg").innerHTML = "";
        }

    }else{
        good = good + 1
        document.getElementById("phone_msg").innerHTML = "";
    }

    // if(document.getElementById("username").value != ""){
    //     $.ajax({
    //         url:"/check_username_seller",
    //         type:"POST",
    //         cache: false,
    //         // async:true;
    //         data:{csrfmiddlewaretoken: token,value:document.getElementById("username").value},
    //         success: function(context) {
    //             if(context.success == 1){
    //                   document.getElementById("username_msg").innerHTML = " already been used!";
    //                   btn.disabled = true;
    //             }else{
    //                   document.getElementById("username_msg").innerHTML = "";
    //             }

    //         }
    //     });
    // }else{
    //     good = good + 1
    // }
    if(good != 0){
        btn.disabled = true;
    }else{
        btn.disabled = false;
    }
}

function store_validation(){
    email = document.getElementById("email")
    phone = document.getElementById("phonenumber")
    var btn = document.getElementById("submit_btn")
    good = 0
    if(email.value != ""){
        if(ValidateEmail(email) == false ){
            good = good + 1
            document.getElementById("email_msg").innerHTML = "Invalid Format!";
        }else{
            document.getElementById("email_msg").innerHTML = "";
        }
    } else{
        good = good + 1
        document.getElementById("email_msg").innerHTML = "";
    }
    if(phone.value != ""){
        if(ValidatePhone(phone.value) == false ){
            good = good + 1
            document.getElementById("phone_msg").innerHTML = "Invalid Format!";
        }else{
            document.getElementById("phone_msg").innerHTML = "";
        }

    }else{
        good = good + 1
        document.getElementById("phone_msg").innerHTML = "";
    }

    if(good != 0){
        btn.disabled = true;
    }else{
        btn.disabled = false;
    }
}


function openTab(tab) {
  var i;
  var x = document.getElementsByClassName("tab");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  document.getElementById(tab).style.display = "block";
}

function SelectImg(id){
  document.getElementById(id).click();
}

function SetVariantImage(imgid,classval,id) {
    var ele = document.getElementsByClassName(classval);

    for(i = 0; i < ele.length; i++) {
        if(ele[i].checked){
            var this_value = ele[i];
            document.getElementById(id).value = this_value.value;
            document.getElementById(imgid).src = "/Post_Media/" + this_value.value;

            break;

        }

    }
}
function bulk_edit_price(){
    var input_price = document.getElementsByClassName("input_price")

    for(var i = 0; i < input_price.length; i++){
        input_price[i].value = document.getElementById("price_edit").value;
    }
}

function validate_add_ons(len){
   var retval  = 0;
   var radioButton = document.querySelector('input[name="add_ons_available_flag'+len+'"]:checked');
   if (radioButton) {
       //do nothing
   } else {
       retval = retval + 1
   }
   if (radioButton.value == "1") {
        if(document.getElementById("add_ons_stocks1").value != ""){
            //do nothing
        }else{
            retval = retval + 1
        }
    }

   if(document.getElementById("product_add_on1").value != ""){
     //do nothing
   }else{
     retval = retval + 1
   }
   if(document.getElementById("product_add_on_price1").value != ""){
     //do nothing
   }else{
     retval = retval + 1
   }
   return retval;
}

function getAddOns(){
    var retval = []
    var window = document.getElementsByClassName("window")
    if(document.getElementById("add_ons").style.display == "block"){
        for(var i = 0; i < window.length; i++){
            var num = i + 1
            var radioValue = ""
            var radioGroup = document.getElementsByName("add_ons_available_flag"+num+"");
            for (var j = 0; j < radioGroup.length; j++) {
                if (radioGroup[j].checked) {
                    radioValue = radioGroup[j].value;
                    break;
                }
            }
            retval.push(
                {
                    "product_name":document.getElementById("product_add_on"+num+"").value,
                    "price":document.getElementById("product_add_on_price"+num+"").value,
                    "status_type":radioValue,
                    "stocks":document.getElementById("add_ons_stocks"+num+"").value
                }
            )
        }
        if(retval.length > 0){
            document.getElementById("add_ons_item").value = JSON.stringify(retval);
        }
    }


}

function has_variants(){
    var variants = document.getElementsByClassName("opt_val")
    var retval = 0;
    if(variants.length > 0){
        retval = 1
    }
    return retval;
}

function has_variants1(product_id){
    var variants = document.getElementsByClassName("opt_val"+product_id+"")
    var retval = 0;
    if(variants.length > 0){
        retval = 1
    }
    return retval;
}


function variants_has_value(){
    var variants = document.getElementsByClassName("opt_val")
    var retval = 0;
    for(var i = 0; i < variants.length; i++){
        var this_value = variants[i]
        if(this_value.value == ""){
            retval = 1
            break;
        }
    }
    return retval;
}
function variants_has_value1(product_id){
    var variants = document.getElementsByClassName("opt_val"+product_id+"")
    var retval = 0;
    for(var j = 0; j < variants.length; j++){
        var this_value = variants[j]
        if(this_value.value == ""){
            retval = 1
            break;
        }
    }
    return retval;
}

function select_option(id1,id2){
    document.getElementById('opt_val'+id1+'').value = id2
}
function get_variant_price(token){
    if(variants_has_value() != 1){
        var variants = document.getElementsByClassName("opt_val")
        var temp = ""
        for(var i = 0; i < variants.length; i++){
            temp += variants[i].value + ","
        }
        $.ajax({
            url:"/get_variant_price",
            type:"POST",
            cache: false,
            // async:true;
            data:{csrfmiddlewaretoken: token,value:temp},
            success: function(context) {
                if(context.success == 1){
                    document.getElementById("price_val").innerHTML = CurrencyConverter(context.price);
                    document.getElementById("selling_price").value = context.price
                    if(context.has_image == 1){
                        document.getElementById("default_image").src = "/Post_Media/"+context.image+""
                    }
                }else{
                    alert("Error Variants");
                }

            }
        });
    }
}
function get_variant_price1(token,product_id){
    
    if(variants_has_value1(product_id) != 1){
        var variants = document.getElementsByClassName("opt_val"+product_id+"")
        var temp = ""
        for(var i = 0; i < variants.length; i++){
            temp += variants[i].value + ","
        }
        $.ajax({
            url:"/get_variant_price",
            type:"POST",
            cache: false,
            // async:true;
            data:{csrfmiddlewaretoken: token,value:temp},
            success: function(context) {
                if(context.success == 1){
                    document.getElementById("price_val").innerHTML = CurrencyConverter(context.price);
                    document.getElementById("selling_price"+product_id+"").value = context.price
                    if(context.has_image == 1){
                        document.getElementById("default_image").src = "/Post_Media/"+context.image+""
                    }
                }else{
                    alert("Error Variants");
                }

            }
        });
    }
}
function display_image(id){
    var image = document.getElementById("product_image"+id+"").src;
    document.getElementById("default_image").src = image
}

function select_to_update(id,key,value){
    document.getElementById("cart_obj"+id+"_"+key+"").value = value
}

function update_variation(token,id){
    var variants = document.getElementsByClassName("opt_val"+id+"")
    var temp = ""
    for(var i = 0; i < variants.length; i++){
        temp += variants[i].value + ","
    }
    $.ajax({
        url:"/update_variation",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,value:temp,id:id},
        success: function(context) {
            if(context.success == 1){
                document.getElementById("price_td"+id+"").innerHTML = CurrencyConverter(context.price);
                document.getElementById("total_td"+id+"").innerHTML = CurrencyConverter(context.total);
                document.getElementById("variation"+id+"").innerHTML = context.variation_name;
            }else{
                alert("Error Variants");
            }

        }
    });
}

function add_to_cart(token,product_id){
    //We check the user login
    var has_login = 0;
    $.ajax({
        url:"/check_user_login",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,redirect_url:"/menu/"+product_id+""},
        success: function(context) {
            if(context.success == 1){
                has_login = 1;
                location.href = '/login';
            }else{
                var retval = {}
                if(has_variants() == 1){
                    if(variants_has_value() != 1){
                        var variants = document.getElementsByClassName("opt_val")
                        var temp = ""
                        for(var i = 0; i < variants.length; i++){
                            temp += variants[i].value + ","
                        }
                        retval = {
                            "product_id": product_id,
                            "price":document.getElementById("selling_price").value,
                            "quantity":document.getElementById("quantity").value,
                            "variation":temp,

                        }
                        $.ajax({
                            url:"/add_to_cart",
                            type:"POST",
                            cache: false,
                            // async:true;
                            data:{csrfmiddlewaretoken: token,value:JSON.stringify(retval)},
                            success: function(context) {
                                if(context.success == 1){
                                    var this_element = context.element
                                    if(context.already_in != 1) {
                                        if(context.count == 1){
                                            $("#scroll_style").empty();
                                            $("#scroll_style").addClass("header__cart-list-item");
                                            $("#scroll_style").addClass("scrollbar");
                                            $("#scroll_style").prepend(
                                                '<a class="header__cart-item" href="/view_cart#cart_section'+this_element.cart_id+'">'+
                                                '<img  src="/Post_Media/'+this_element.image+'" alt="" class="header__cart-img"/>'+
                                                '<div class="header__cart-item-info text-black">'+
                                                '<div class="header__cart-item-head">'+
                                                '<h5 class="header__cart-item-name">'+this_element.product_name+'</h5>'+
                                                '<div class="header__cart-item-price-wrap">'+
                                                ' <span class="header__cart-item-price">'+CurrencyConverter(this_element.total)+'</span>'+
                                                '<span class="header__cart-item-multiply">x</span>'+
                                                '<span class="header__cart-item-qnt">'+this_element.quantity+'</span>'+
                                                '</div></div>'+
                                                '<div class="header__cart-item-body">'+
                                                '<span class="header__cart-item-description"></span>'+
                                                '<span class="header__cart-item-remove"></span>'+
                                                '</div></div>'+
                                                '</a>');
                                                document.getElementById("cart_total_count").innerHTML =   1
                                                document.getElementById("cart_total_count").style.display = "block"
                                                document.getElementById("cart_footer").style.display = "block"
                                        }else{
                                            $("#scroll_style").prepend(
                                                '<a class="header__cart-item" href="/view_cart#cart_section'+this_element.cart_id+'">'+
                                                '<img  src="/Post_Media/'+this_element.image+'" alt="" class="header__cart-img"/>'+
                                                '<div class="header__cart-item-info text-black">'+
                                                '<div class="header__cart-item-head">'+
                                                '<h5 class="header__cart-item-name">'+this_element.product_name+'</h5>'+
                                                '<div class="header__cart-item-price-wrap">'+
                                                ' <span class="header__cart-item-price">'+CurrencyConverter(this_element.total)+'</span>'+
                                                '<span class="header__cart-item-multiply">x</span>'+
                                                '<span class="header__cart-item-qnt">'+this_element.quantity+'</span>'+
                                                '</div></div>'+
                                                '<div class="header__cart-item-body">'+
                                                '<span class="header__cart-item-description"></span>'+
                                                '<span class="header__cart-item-remove"></span>'+
                                                '</div></div>'+
                                                '</a>');
                                                var cart_total = parseInt(document.getElementById("cart_total_count").innerHTML);
                                                document.getElementById("cart_total_count").innerHTML = cart_total + 1
                                        }
                                        
                                       
                                    }
                                    Swal.fire(context.msg, '', 'success')
                                }else{
                                    Swal.fire(context.msg, '', 'error')
                                }

                            }
                        });


                    }else{
                        Swal.fire('Please choose a variant!', '', 'warning')
                    }
                }else{
                    retval = {
                        "product_id": product_id,
                        "price":document.getElementById("selling_price").value,
                        "quantity":document.getElementById("quantity").value,
                        "variation":"",
                    }
                    $.ajax({
                        url:"/add_to_cart",
                        type:"POST",
                        cache: false,
                        // async:true;
                        data:{csrfmiddlewaretoken: token,value:JSON.stringify(retval)},
                        success: function(context) {

                            if(context.success == 1){
                                var this_element = context.element
                                if(context.already_in != 1) {

                                    if(context.count == 1){
                                        $("#scroll_style").empty();
                                        $("#scroll_style").addClass("header__cart-list-item");
                                        $("#scroll_style").addClass("scrollbar");
                                        $("#scroll_style").prepend(
                                            '<a class="header__cart-item" href="/view_cart#cart_section'+this_element.cart_id+'">'+
                                            '<img  src="/Post_Media/'+this_element.image+'" alt="" class="header__cart-img"/>'+
                                            '<div class="header__cart-item-info text-black">'+
                                            '<div class="header__cart-item-head">'+
                                            '<h5 class="header__cart-item-name">'+this_element.product_name+'</h5>'+
                                            '<div class="header__cart-item-price-wrap">'+
                                            ' <span class="header__cart-item-price">'+CurrencyConverter(this_element.total)+'</span>'+
                                            '<span class="header__cart-item-multiply">x</span>'+
                                            '<span class="header__cart-item-qnt">'+this_element.quantity+'</span>'+
                                            '</div></div>'+
                                            '<div class="header__cart-item-body">'+
                                            '<span class="header__cart-item-description"></span>'+
                                            '<span class="header__cart-item-remove"></span>'+
                                            '</div></div>'+
                                            '</a>');
                                            document.getElementById("cart_total_count").innerHTML =  1
                                            document.getElementById("cart_total_count").style.display = "block"
                                            document.getElementById("cart_footer").style.display = "block"
                                    }else{
                                        $("#scroll_style").prepend(
                                            '<a class="header__cart-item" href="/view_cart#cart_section'+this_element.cart_id+'">'+
                                            '<img  src="/Post_Media/'+this_element.image+'" alt="" class="header__cart-img"/>'+
                                            '<div class="header__cart-item-info text-black">'+
                                            '<div class="header__cart-item-head">'+
                                            '<h5 class="header__cart-item-name">'+this_element.product_name+'</h5>'+
                                            '<div class="header__cart-item-price-wrap">'+
                                            ' <span class="header__cart-item-price">'+CurrencyConverter(this_element.total)+'</span>'+
                                            '<span class="header__cart-item-multiply">x</span>'+
                                            '<span class="header__cart-item-qnt">'+this_element.quantity+'</span>'+
                                            '</div></div>'+
                                            '<div class="header__cart-item-body">'+
                                            '<span class="header__cart-item-description"></span>'+
                                            '<span class="header__cart-item-remove"></span>'+
                                            '</div></div>'+
                                            '</a>');
                                            var cart_total = parseInt(document.getElementById("cart_total_count").innerHTML);
                                            document.getElementById("cart_total_count").innerHTML = cart_total + 1
                                    }
                                       

                                }
                                Swal.fire(context.msg, '', 'success')
                            }else{
                                Swal.fire(context.msg, '', 'error')
                            }
                        }
                    });
                }
                        }

                    }
    });

}

function add_to_cart1(token,product_id){
    //We check the user login
    var has_login = 0;
    $.ajax({
        url:"/check_user_login",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,redirect_url:"/menu/"+product_id+""},
        success: function(context) {
            if(context.success == 1){
                has_login = 1;
                location.href = '/login';
            }else{
                var retval = {}
                if(has_variants1(product_id) == 1){
                    if(variants_has_value1(product_id) != 1){
                        var variants = document.getElementsByClassName("opt_val"+product_id+"")
                        var temp = ""
                        for(var i = 0; i < variants.length; i++){
                            temp += variants[i].value + ","
                        }
                        retval = {
                            "product_id": product_id,
                            "price":document.getElementById("selling_price"+product_id+"").value,
                            "quantity":document.getElementById("quantity"+product_id+"").value,
                            "variation":temp,

                        }
                        $.ajax({
                            url:"/add_to_cart",
                            type:"POST",
                            cache: false,
                            // async:true;
                            data:{csrfmiddlewaretoken: token,value:JSON.stringify(retval)},
                            success: function(context) {
                                if(context.success == 1){
                                    var this_element = context.element
                                    if(context.already_in != 1) {
                                        if(context.count == 1){
                                            $("#scroll_style").empty();
                                            $("#scroll_style").addClass("header__cart-list-item");
                                            $("#scroll_style").addClass("scrollbar");
                                            $("#scroll_style").prepend(
                                                '<a class="header__cart-item" href="/view_cart#cart_section'+this_element.cart_id+'">'+
                                                '<img  src="/Post_Media/'+this_element.image+'" alt="" class="header__cart-img"/>'+
                                                '<div class="header__cart-item-info text-black">'+
                                                '<div class="header__cart-item-head">'+
                                                '<h5 class="header__cart-item-name">'+this_element.product_name+'</h5>'+
                                                '<div class="header__cart-item-price-wrap">'+
                                                ' <span class="header__cart-item-price">'+CurrencyConverter(this_element.total)+'</span>'+
                                                '<span class="header__cart-item-multiply">x</span>'+
                                                '<span class="header__cart-item-qnt">'+this_element.quantity+'</span>'+
                                                '</div></div>'+
                                                '<div class="header__cart-item-body">'+
                                                '<span class="header__cart-item-description"></span>'+
                                                '<span class="header__cart-item-remove"></span>'+
                                                '</div></div>'+
                                                '</a>');
                                                document.getElementById("cart_total_count").innerHTML =   1
                                                document.getElementById("cart_total_count").style.display = "block"
                                                document.getElementById("cart_footer").style.display = "block"
                                                
                                        }else{
                                            $("#scroll_style").prepend(
                                                '<a class="header__cart-item" href="/view_cart#cart_section'+this_element.cart_id+'">'+
                                                '<img  src="/Post_Media/'+this_element.image+'" alt="" class="header__cart-img"/>'+
                                                '<div class="header__cart-item-info text-black">'+
                                                '<div class="header__cart-item-head">'+
                                                '<h5 class="header__cart-item-name">'+this_element.product_name+'</h5>'+
                                                '<div class="header__cart-item-price-wrap">'+
                                                ' <span class="header__cart-item-price">'+CurrencyConverter(this_element.total)+'</span>'+
                                                '<span class="header__cart-item-multiply">x</span>'+
                                                '<span class="header__cart-item-qnt">'+this_element.quantity+'</span>'+
                                                '</div></div>'+
                                                '<div class="header__cart-item-body">'+
                                                '<span class="header__cart-item-description"></span>'+
                                                '<span class="header__cart-item-remove"></span>'+
                                                '</div></div>'+
                                                '</a>');
                                                var cart_total = parseInt(document.getElementById("cart_total_count").innerHTML);
                                                document.getElementById("cart_total_count").innerHTML = cart_total + 1
                                        }
                                           
                                    }
                                    Swal.fire(context.msg, '', 'success')
                                }else{
                                    Swal.fire(context.msg, '', 'error')
                                }

                            }
                        });


                    }else{
                        Swal.fire('Please choose a variant!', '', 'warning')
                    }
                }else{
                    retval = {
                        "product_id": product_id,
                        "price":document.getElementById("selling_price"+product_id+"").value,
                        "quantity":document.getElementById("quantity"+product_id+"").value,
                        "variation":"",
                    }
                    $.ajax({
                        url:"/add_to_cart",
                        type:"POST",
                        cache: false,
                        // async:true;
                        data:{csrfmiddlewaretoken: token,value:JSON.stringify(retval)},
                        success: function(context) {

                            if(context.success == 1){
                                var this_element = context.element
                                if(context.already_in != 1) {
                                    if(context.count == 1){
                                        $("#scroll_style").empty();
                                        $("#scroll_style").addClass("header__cart-list-item");
                                        $("#scroll_style").addClass("scrollbar");
                                        $("#scroll_style").prepend(
                                            '<a class="header__cart-item" href="/view_cart#cart_section'+this_element.cart_id+'">'+
                                            '<img  src="/Post_Media/'+this_element.image+'" alt="" class="header__cart-img"/>'+
                                            '<div class="header__cart-item-info text-black">'+
                                            '<div class="header__cart-item-head">'+
                                            '<h5 class="header__cart-item-name">'+this_element.product_name+'</h5>'+
                                            '<div class="header__cart-item-price-wrap">'+
                                            ' <span class="header__cart-item-price">'+CurrencyConverter(this_element.total)+'</span>'+
                                            '<span class="header__cart-item-multiply">x</span>'+
                                            '<span class="header__cart-item-qnt">'+this_element.quantity+'</span>'+
                                            '</div></div>'+
                                            '<div class="header__cart-item-body">'+
                                            '<span class="header__cart-item-description"></span>'+
                                            '<span class="header__cart-item-remove"></span>'+
                                            '</div></div>'+
                                            '</a>');
                                            document.getElementById("cart_total_count").innerHTML =   1  
                                            document.getElementById("cart_total_count").style.display = "block"  
                                            document.getElementById("cart_footer").style.display = "block"
                                    }else{
                                        $("#scroll_style").prepend(
                                            '<a class="header__cart-item" href="/view_cart#cart_section'+this_element.cart_id+'">'+
                                            '<img  src="/Post_Media/'+this_element.image+'" alt="" class="header__cart-img"/>'+
                                            '<div class="header__cart-item-info text-black">'+
                                            '<div class="header__cart-item-head">'+
                                            '<h5 class="header__cart-item-name">'+this_element.product_name+'</h5>'+
                                            '<div class="header__cart-item-price-wrap">'+
                                            ' <span class="header__cart-item-price">'+CurrencyConverter(this_element.total)+'</span>'+
                                            '<span class="header__cart-item-multiply">x</span>'+
                                            '<span class="header__cart-item-qnt">'+this_element.quantity+'</span>'+
                                            '</div></div>'+
                                            '<div class="header__cart-item-body">'+
                                            '<span class="header__cart-item-description"></span>'+
                                            '<span class="header__cart-item-remove"></span>'+
                                            '</div></div>'+
                                            '</a>');
                                            var cart_total = parseInt(document.getElementById("cart_total_count").innerHTML);
                                            document.getElementById("cart_total_count").innerHTML = cart_total + 1
                                    }
                                       
                                }
                                Swal.fire(context.msg, '', 'success')
                            }else{
                                Swal.fire(context.msg, '', 'error')
                            }
                        }
                    });
                }
                        }

                    }
    });

}

function add_to_order(token,product_id,order_id){
    var retval = {}
    if(has_variants1(product_id) == 1){
        if(variants_has_value1(product_id) != 1){
            var variants = document.getElementsByClassName("opt_val"+product_id+"")
            var temp = ""
            for(var i = 0; i < variants.length; i++){
                temp += variants[i].value + ","
            }
            retval = {
                "product_id": product_id,
                "price":document.getElementById("selling_price"+product_id+"").value,
                "quantity":document.getElementById("quantity"+product_id+"").value,
                "variation":temp,

            }
            $.ajax({
                url:"/add_to_order",
                type:"POST",
                cache: false,
                // async:true;
                data:{csrfmiddlewaretoken: token,value:JSON.stringify(retval),order_id:order_id},
                success: function(context) {
                    if(context.success == 1){
                        Swal.fire(context.msg, '', 'success')
                    }else{
                        Swal.fire(context.msg, '', 'error')
                    }

                }
            });


        }else{
            Swal.fire('Please choose a variant!', '', 'warning')
        }
    }else{
        retval = {
            "product_id": product_id,
            "price":document.getElementById("selling_price"+product_id+"").value,
            "quantity":document.getElementById("quantity"+product_id+"").value,
            "variation":"",
        }
        $.ajax({
            url:"/add_to_order",
            type:"POST",
            cache: false,
            // async:true;
            data:{csrfmiddlewaretoken: token,value:JSON.stringify(retval),order_id:order_id},
            success: function(context) {
                if(context.success == 1){
                    Swal.fire(context.msg, '', 'success')
                }else{
                    Swal.fire(context.msg, '', 'error')
                }
            }
        });
    }
}

function quick_place_order(token,product_id){
    //We check the user login
    // $.ajax({
    //     url:"/check_user_login",
    //     type:"POST",
    //     cache: false,
    //     // async:true;
    //     data:{csrfmiddlewaretoken: token,redirect_url:"/menu/"+product_id+""},
    //     success: function(context) {
    //         if(context.success == 1){
    //             location.href = '/login';
    //         }else{
            var retval = {}
            if(has_variants() == 1){
                if(variants_has_value() != 1){
                    var variants = document.getElementsByClassName("opt_val")
                    var temp = ""
                    for(var i = 0; i < variants.length; i++){
                        temp += variants[i].value + ","
                    }
                    retval = {
                        "product_id": product_id,
                        "price":document.getElementById("selling_price"+product_id+"").value,
                        "quantity":document.getElementById("quantity"+product_id+"").value,
                        "variation":temp,

                    }
                    $.ajax({
                        url:"/quick_place_order",
                        type:"POST",
                        cache: false,
                        // async:true;
                        data:{csrfmiddlewaretoken: token,value:JSON.stringify(retval)},
                        success: function(context) {
                            sessionStorage.setItem("place_item", context.id);
                            var pathstr = "/view_cart#cart_section"+context.cart_key+""
                            location.href = pathstr;

                        }
                    });


                }else{
                    alert("Please choose a variant!")
                }
            }else{
                retval = {
                    "product_id": product_id,
                    "price":document.getElementById("selling_price"+product_id+"").value,
                    "quantity":document.getElementById("quantity"+product_id+"").value,
                    "variation":"",
                }
                $.ajax({
                    url:"/quick_place_order",
                    type:"POST",
                    cache: false,
                    // async:true;
                    data:{csrfmiddlewaretoken: token,value:JSON.stringify(retval)},
                    success: function(context) {
                        sessionStorage.setItem("place_item", context.id);
                        var pathstr = "/view_cart#cart_section"+context.cart_key+""
                        location.href = pathstr;
                    }
                });
            }


}

function set_browse_img(token,id1,id2,imgid,product_id){
    var fileInput = document.getElementById(id1).files[0];
    var formData = new FormData();
    formData.append('file', fileInput);


    $.ajax({
        url:"/set_browse_img",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,value:JSON.stringify(formData),product_id:product_id},
        success: function(context) {
            if(context.success == 1){
                document.getElementById(id2).value = fileInput.value
                document.getElementById(imgid).src = "/Post_Media/" + fileInput.value
            }
        }
    });
}

function redirect_login(token){
    var currentUrl = window.location.href;
    $.ajax({
        url:"/redirect_login",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,current_url:currentUrl},
        success: function(context) {

            if(context.success == 1){
                location.href = "/login";
            }
        }
    });
}

function get_checkbox_len(name){
    var retval = 0
    var checkbox = document.getElementsByName(name)
    for (var i=0; i < checkbox.length; i++) {
        if(checkbox[i].checked == true){
            retval = retval + 1
        }
      }

      return retval;
}

function group_order_key(cart_key,this_id){
    var this_key = document.getElementById("group_order_key"+cart_key+"")
    var check_box = document.getElementById("emcdo_product"+this_id+"")
    if(check_box.checked == true){
        this_key.value += check_box.value + ","
    }else{
        var this_value = this_key.value
        this_key.value = this_value.replace(check_box.value + ",","")
    }


}
function unselect_key(){
    var check_box = document.getElementsByClassName("order_keys")
    for (var i=0; i < check_box.length; i++) {
        check_box[i].value = ""
    }
}

function select_all(){
    var select = document.getElementById("selectAll")
    var checkbox = document.getElementsByClassName("checkbox_cart")
    for(var i = 0; i < checkbox.length; i++){
        checkbox[i].click();
    }

}
function select_cart_obj(token){
    if(get_checkbox_len("emcdo_product") > 0){
        document.getElementById("checkout_btn").disabled = false;
        var retval = ""
        var checkbox = document.getElementsByName("emcdo_product")
        for (var i=0; i < checkbox.length; i++) {
            if(checkbox[i].checked == true){
                retval += checkbox[i].value + ","
            }
        }
        $.ajax({
            url:"/select_cart_obj",
            type:"POST",
            cache: false,
            // async:true;
            data:{csrfmiddlewaretoken: token,value:retval},
            success: function(context) {

                if(context.success == 1){

                    if(get_checkbox_len("emcdo_product") > 1){
                        document.getElementById("total_section").innerHTML = CurrencyConverter(context.total)
                        document.getElementById("no_item").innerHTML =  ""+get_checkbox_len("emcdo_product")+" Items";
                    }else{
                        document.getElementById("total_section").innerHTML = CurrencyConverter(context.total)
                        document.getElementById("no_item").innerHTML =  ""+get_checkbox_len("emcdo_product")+" Item";
                    }
                }
            }
        });
    }else{
        document.getElementById("total_section").innerHTML = CurrencyConverter(0)
        document.getElementById("checkout_btn").disabled = true;
        document.getElementById("no_item").innerHTML = "0 Item"
    }


}

function update_quatity(token,this_id){
    this_value = document.getElementById("product-qty"+this_id+"")
    if(this_value.value != ""){
        $.ajax({
            url:"/update_quatity",
            type:"POST",
            cache: false,
            // async:true;
            data:{csrfmiddlewaretoken: token,value:this_value.value,id:this_id},
            success: function(context) {

                if(context.success == 1){
                    document.getElementById("total_td"+this_id+"").innerHTML = CurrencyConverter(context.total)
                }
            }
        });
    }

}

function plus_update_quatity(token,this_value,this_id){

    $.ajax({
        url:"/update_quatity",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,value:this_value,id:this_id},
        success: function(context) {

            if(context.success == 1){
                document.getElementById("total_td"+this_id+"").innerHTML = CurrencyConverter(context.total)
                var this_checkbox = document.getElementById("emcdo_product"+this_id+"")
                if(this_checkbox.checked == true){
                    var current_total = document.getElementById("total_section").innerHTML
                    var current_total1 = current_total.replace(/[₱ , ]/g,"")
                    document.getElementById("total_section").innerHTML = CurrencyConverter(parseFloat(current_total1) + parseFloat(context.price))
                }

            }
        }
    });
}

function minus_update_quatity(token,this_value,this_id){

    $.ajax({
        url:"/update_quatity",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,value:this_value,id:this_id},
        success: function(context) {

            if(context.success == 1){
                document.getElementById("total_td"+this_id+"").innerHTML = CurrencyConverter(context.total)
                var this_checkbox = document.getElementById("emcdo_product"+this_id+"")
                if(this_checkbox.checked == true){
                    var current_total = document.getElementById("total_section").innerHTML
                    var current_total1 = current_total.replace(/[₱ , ]/g,"")
                    document.getElementById("total_section").innerHTML = CurrencyConverter(parseFloat(current_total1) - parseFloat(context.price))
                }

            }
        }
    });
}

function quick_checkout(token,id){
    var retval = []
    retval.push({
        "value":id + ","
    })

    $.ajax({
        url:"/quick_checkout",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,value:JSON.stringify(retval)},
        success: function(context) {

            if(context.success == 1){
                var pathstr = "/checkout"
                location.href = pathstr;
            }
        }
    });

}

function checkout_items(token){
    var cart_keys = document.getElementsByClassName("order_keys")
    var retval = ''
    for(var i = 0; i < cart_keys.length; i++){
        if(cart_keys[i].value != ""){
            retval += cart_keys[i].value + "|"
        }


    }

    $.ajax({
        url:"/checkout_items",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,value:retval},
        success: function(context) {
            if(context.success == 1){
                var pathstr = "/checkout"
                location.href = pathstr;
            }
        }
    });

}

function validate_order(){
    var service_fields = document.getElementsByClassName("service_fields")
    var flag = 0
    for(var i = 0; i < service_fields.length; i++){
        if(service_fields[i].value == ""){
            flag = 1
            break;
        }
    }
    if(flag != 0){
        document.getElementById("placeOrder_btn").disabled = true;
    }else{
        document.getElementById("placeOrder_btn").disabled = false;
    }
}

function verify_login(){
    var fields = document.getElementsByClassName("login_fields")
    var flag = 0
    for(var i = 0; i < fields.length; i++){
        if(fields[i].value == ""){
            flag = 1
            break;
        }
    }
    if(flag != 0){
        document.getElementById("login_btn").disabled = true;
    }else{
        document.getElementById("login_btn").disabled = false;
    }
}

function login(token){
    var userid = document.getElementById("userid")
    var pass = document.getElementById("password")
    $.ajax({
        url:"/quick_login",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,userid:userid.value,password:pass.value},
        success: function(context) {
            if(context.success == 1){
                document.getElementById("login-messages").innerHTML = ""
                checkout_items(token)
                console.log(context.success)

            }else{
                document.getElementById("login-messages").innerHTML = context.error_msg
            }
        }
    });
}
function login1(token){
    var userid = document.getElementById("userid")
    var pass = document.getElementById("password")
    $.ajax({
        url:"/quick_login",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,userid:userid.value,password:pass.value},
        success: function(context) {
            if(context.success == 1){
                document.getElementById("login-messages").innerHTML = ""
                document.getElementById("placeOrder_btn").setAttribute("type", "submit");
                console.log(document.getElementById("placeOrder_btn"))
                document.getElementById("placeOrder_btn").click();
            }else{
                document.getElementById("login-messages").innerHTML = context.error_msg
            }
        }
    });
}

function verify_order_info(){
    var fields = document.getElementsByClassName("info")
    var flag = 0
    if(document.getElementById("emailadd").value != ""){
        if(ValidateEmail(document.getElementById("emailadd")) == true){
            //good
            document.getElementById("email_msg").innerHTML = ""
        }else{
            flag = 1
            document.getElementById("email_msg").innerHTML = "Invalid Email Address!"
        }
    }else{
        flag = 1
        document.getElementById("email_msg").innerHTML = ""
    }

    if(document.getElementById("fname").value != ""){
        //good
    }else{
        flag = 1
    }

    if(document.getElementById("phone").value != ""){
        if(ValidatePhone(document.getElementById("phone").value) == true){
            //good
            document.getElementById("phone_msg").innerHTML = ""
        }else{
            flag = 1
            document.getElementById("phone_msg").innerHTML = "Invalid Phone Number!"
        }
    }else{
        flag = 1
        document.getElementById("phone_msg").innerHTML = ""
    }

    if(flag != 0){
        document.getElementById("info_btn").disabled = true;
    }else{
        document.getElementById("info_btn").disabled = false;
    }
}


function get_cart_total(token){

    $.ajax({
        url:"/get_cart_total",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token},
        success: function(context) {
            var count = document.getElementById("cart_total_count")
            if (parseInt(context.count) > 0){
                count.innerHTML = context.count;
                count.style.display = "inline";
            }else{
                count.innerHTML = context.count;
                count.style.display = "none";
            }
        }
    });

}
function convertHex(hex,opacity){
    hex = hex.replace('#','');
    r = parseInt(hex.substring(0,2), 16);
    g = parseInt(hex.substring(2,4), 16);
    b = parseInt(hex.substring(4,6), 16);

    result = 'rgba('+r+','+g+','+b+','+opacity/100+')';
    return result;
}

function check_available_product(token){
    $.ajax({
        url:"/check_available_product",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token},
        success: function(context) {
            var retval = context.retval
            var my_array = retval.split(",")
            for(var i = 0; i < my_array.length; i++){
                if(document.getElementById("available_msg_section"+my_array[i]+"")){
                    $("#cart_section"+my_array[i]+" *").prop('disabled',true);
                    document.getElementById("available_msg_section"+my_array[i]+"").display = "none";
                    document.getElementById("available_msg"+my_array[i]+"").innerHTML = "SOLD OUT";
                }

            }
        }
    });
}

function check_quantity(token){
    $.ajax({
        url:"/check_quantity",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token},
        success: function(context) {
            var retval = context.retval
            var my_array = retval.split(",")
            var msg = context.msg
            var my_array1 = msg.split(",")
            for(var i = 0; i < my_array.length; i++){
                if(document.getElementById("available_msg_section"+my_array[i]+"")){
                    document.getElementById("emcdo_product"+my_array[i]+"").disabled = true;
                    document.getElementById("available_msg_section"+my_array[i]+"").style.display = "block";
                    document.getElementById("available_msg"+my_array[i]+"").innerHTML = my_array1[i];
                }
            }
        }
    });
}

function check_variations(token){
    $.ajax({
        url:"/check_variations",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token},
        success: function(context) {
            console.log()
            var retval = context.retval
            var my_array = retval.split(",")
            var msg = context.msg
            var my_array1 = msg.split(",")
            for(var i = 0; i < my_array.length; i++){
                if(document.getElementById("available_msg_section"+my_array[i]+"")){
                    document.getElementById("emcdo_product"+my_array[i]+"").disabled = true;
                    document.getElementById("available_msg_section"+my_array[i]+"").style.display = "block";;
                    document.getElementById("available_msg"+my_array[i]+"").innerHTML = my_array1[i];
                }
            }
        }
    });
}

function disable_cart_variation(token){
    $.ajax({
        url:"/disable_cart_variation",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token},
        success: function(context) {
            console.log()
            var retval = context.retval
            var my_array = retval.split(",")

            for(var i = 0; i < my_array.length; i++){
                if(document.getElementById("attr_option"+my_array[i]+"")){
                    document.getElementById("attr_option"+my_array[i]+"").disabled = true;
                    $("#attr_option"+my_array[i]+"").css('background', convertHex('#404c57',50));
                }
            }
        }
    });
}

function disable_product_variation(token,id){

    $.ajax({
        url:"/disable_product_variation",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,value:id},
        success: function(context) {
            console.log()
            var retval = context.retval
            var my_array = retval.split(",")

            for(var i = 0; i < my_array.length; i++){
                if(document.getElementById("attr_option"+my_array[i]+"")){
                    document.getElementById("attr_option"+my_array[i]+"").disabled = true;
                    $("#attr_option"+my_array[i]+"").css('background', convertHex('#404c57',50));
                }
            }
        }
    });

}

function available_switch(token,id){
    var switch_btn = document.getElementById("product_avail_flag"+id+"")
    if(switch_btn.checked == true){
        $.ajax({
            url:"/available_switch",
            type:"POST",
            cache: false,
            // async:true;
            data:{csrfmiddlewaretoken: token,this_id:id,value:1},

        });
    }else{
        $.ajax({
            url:"/available_switch",
            type:"POST",
            cache: false,
            // async:true;
            data:{csrfmiddlewaretoken: token,this_id:id,value:0},

        });

    }


}

function disable_product(token,id){
    $.ajax({
        url:"/disable_product",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,value:id},
        success: function(context) {

            if(context.success == 1){
                $("#menus *").prop('disabled',true);
                document.getElementById("sold_out_content").style.display = "block";
                document.getElementById("sold_out_msg").innerHTML = "SOLD OUT";

            }
        }
    });
}

function drag_order(id){
    sessionStorage.setItem("order_drag",id)
}
function drag_order_status(token,id,col_id){
    $.ajax({
        url:"/drag_order_status",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,this_id:id,this_col:col_id},
        success: function(context) {
            if(context.paid == 1){
                document.getElementById("order_status"+context.order_id+"").innerHTML = "Paid";
                document.getElementById("order_status"+context.order_id+"").style.color = "green";
            }
        }
    });
}
function selected_option(this_value,this_class){
    var this_list = this_value.split(",")
    var btn = document.getElementsByClassName(this_class)
    for(var i = 0; i < btn.length; i++){
        if(this_list.includes(btn[i].value) == true){
            btn[i].classList.add('selected-variation');
            btn[i].click()
            break;
        }
    }
}
function request_share_order(token){
    var order_id = document.getElementById("share_order_id")
    $.ajax({
        url:"/request_share_order",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,value:order_id.value},
        success: function(context) {
            if(context.success == 1){
                document.getElementById("share_msg").innerHTML = context.msg
            }else{
                document.getElementById("share_msg").innerHTML = ""
                $("#exampleModalCenterTitle .close").click()
                Swal.fire(context.msg, '', 'success')

            }

        }
    });
}

function allow_share_order(token,notif_id) {
    Swal.fire({
        title: 'Do you want to accept the share order?',
        icon: 'question',
        showDenyButton: true,
        showCancelButton: false,
        confirmButtonText: 'Yes',
        denyButtonText: "No",
    }

    ).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            $.ajax({
                url:"/accept_request",
                type:"POST",
                cache: false,
                // async:true;
                data:{csrfmiddlewaretoken: token,this_id:notif_id},
                success: function(context) {
                    if(context.success == 1){
                        Swal.fire(context.msg, '', 'success')
                    }else{
                        Swal.fire(context.msg, '', 'error')
                    }
                }
            });
        } else if (result.isDenied) {
            $.ajax({
                url:"/denied_request",
                type:"POST",
                cache: false,
                // async:true;
                data:{csrfmiddlewaretoken: token,this_id:notif_id},
                success: function(context) {
                    if(context.success == 1){
                        Swal.fire(context.msg, '', 'info')
                    }else{
                        Swal.fire(context.msg, '', 'error')
                    }
                }
            });
        }
    })
}
function share_order_accessable(url){
    Swal.fire({
        title: 'Do you want to proceed?',
        icon: 'question',
        showDenyButton: true,
        showCancelButton: false,
        confirmButtonText: 'Yes',
        denyButtonText: "No",
    }

    ).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            window.location.href = url;
        } else if (result.isDenied) {
            Swal.fire('Decline', '', 'info')
        }
    })
}

function openTab(url){
  window.open(url);
}
function share_order_access_denied(){
    Swal.fire({
        icon: 'error',
        title: 'Share order',
        text: 'Your request order was denied',
    })
}


function read_notifications(token){
    $.ajax({
        url:"/read_notifications",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,},
        success: function(context) {
            if(context.success == 1){
                if(document.getElementById("notif_count")){
                    document.getElementById("notif_count").style.display = "none";
                }
            }
        }
    });

}

function read_notifications_merchant(token){
    $.ajax({
        url:"/read_notifications_merchant",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,},
        success: function(context) {
            if(context.success == 1){
                if(document.getElementById("notif_count")){
                    document.getElementById("notif_count").style.display = "none";
                }
            }
        }
    });

}

function unread_notifications(token){
    $.ajax({
        url:"/unread_notifications",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,},
        success: function(context) {
            if(context.success == 1){
                if(document.getElementById("notif_count")){
                    if(context.count != 0){
                        document.getElementById("notif_count").innerHTML = context.count
                    }else{
                        document.getElementById("notif_count").style.display = "none";
                    }

                }
            }
        }
    });

}

function unread_notifications_merchant(token){
    $.ajax({
        url:"/unread_notifications_merchant",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,},
        success: function(context) {
            if(context.success == 1){
                if(document.getElementById("notif_count")){
                    if(context.count != 0){
                        document.getElementById("notif_count").innerHTML = context.count
                    }else{
                        document.getElementById("notif_count").style.display = "none";
                    }

                }
            }
        }
    });

}

function remove_cart_item(token,id){

    $.ajax({
        url:"/remove_cart_item",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,this_id:id},
        success: function(context) {
            if(context.success == 1){
                document.getElementById("item_block"+id+"").remove()
                if(document.getElementById("cart_item"+id+"")){
                    document.getElementById("cart_item"+id+"").remove()
                }
                var block = document.getElementsByClassName("block"+context.cart_key+"")
                if(block.length == 0){
                    document.getElementById("store_section"+context.cart_key+"").remove()
                }
                var cart_count = document.getElementById("cart_total_count").innerHTML;
                document.getElementById("cart_total_count").innerHTML = parseInt(cart_count) - 1
                $("#exampleModalCenter"+id+" .close").click()
                Swal.fire(context.msg, '', 'success')
            }else{
                Swal.fire(context.msg, '', 'error')
            }
        }
    });

}

function add_discount_personnel(token){
    var status = document.getElementById("personnel_status")
    var discount = document.getElementById("discount_percentage")
    $.ajax({
        url:"/add_discount_personnel",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,status:status.value,discount:discount.value},
        success: function(context) {
            if(context.success == 1){
                location.reload();
            }else{
                location.reload();
            }
        }
    });
}
function verify_personnel_discount(){
    var add_personnel = document.getElementsByClassName("add_personnel")
    var flag = 0
    for(var i = 0; i < add_personnel.length; i++){
        if(add_personnel[i].value == ""){
            flag += 1
        }
    }
    if(flag != 0 ){
        document.getElementById("add_personnel").disabled = true;
    }else{
        document.getElementById("add_personnel").disabled = false;
    }
}

function edit_discount_personnel(token,this_id){

    var discount = document.getElementById("edit_discount"+this_id+"")
    $.ajax({
        url:"/edit_discount_personnel",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,discount:discount.value,this_id:this_id},
        success: function() {
            location.reload();
        }
    });
}


function delete_discount_personnel(token,this_id){
    $.ajax({
        url:"/delete_discount_personnel",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,this_id:this_id},
        success: function() {
            location.reload();
        }
    });

}



function check_personnel_status(token){
    $.ajax({
        url:"/check_personnel_status",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,value:document.getElementById("personnel_status").value},
        success: function(context) {
            if(context.success == 1){
                alert(context.msg)
                document.getElementById("add_personnel").disabled = true;
                document.getElementById("personnel_status").value = ""
            }
        }
    });
}

function request_discount(order_id){
    var form = document.getElementById("purchase_form");
    var formData = new FormData(form);
    var fileInput = document.getElementById('discount_file'+order_id+'');
    var e = document.getElementById("discount_personnel"+order_id+"");
    var discount_id = e.options[e.selectedIndex].value;
    formData.append('myfile', fileInput.files[0]);
    formData.append('order_id', order_id);
    formData.append('discount_id', discount_id);
    $.ajax({
        type: 'POST',
        url: '/request_discount',
        dataType: "json",
        //data: {csrfmiddlewaretoken: token,form_data:formData,order_id:order_id,discount_id:discount_id},
        data:formData,
        processData: false,
        contentType: false,
        success: function(context) {
            if(context.success == 1){
                $("#discount_request"+order_id+" .close").click()
                Swal.fire(context.msg, '', 'success')
            }
        },

    });

}


function accept_discount_request(token,this_id){

    $.ajax({
        url:"/accept_discount_request",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,this_id:this_id},
        success: function(context) {
            if(context.success == 1){
                window.close();
            }
        }
    });
}

function reject_discount_request(token,this_id){

    $.ajax({
        url:"/reject_discount_request",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,this_id:this_id},
        success: function(context) {
            if(context.success == 1){
                window.close();
            }
        }
    });
}

function verify_discount_request(id){
    var this_class = document.getElementsByClassName("discount_fields"+id+"")
    var flag = 0
    for(var i = 0; i < this_class.length; i++){
        if(this_class[i].value == ""){
            flag += 1
        }
    }
    if(flag != 0){
        document.getElementById("discount_btn"+id+"").disabled = true;
    }else{
        document.getElementById("discount_btn"+id+"").disabled = false;
    }
}

function requested_discounts(token){

    $.ajax({
        url:"/requested_discounts",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token},
        success: function(context) {
            if(context.success == 1){
                var retval = context.retval
                var this_list = retval.split(",")
                for(var i = 0; i < this_list.length; i++){
                    if(document.getElementsByClassName("discount_fields"+this_list[i]+"")){
                        document.getElementById("discount_msg"+this_list[i]+"").innerHTML = "You have already requested."
                        var this_fields = document.getElementsByClassName("discount_fields"+this_list[i]+"")
                        for(var j = 0; j < this_list.length; j++){
                            this_fields[j].disabled = true;
                        }  
                    }
                }
            }
        }
    });

}

function remove_order_item(token,this_id){

    $.ajax({
        url:"/remove_order_item",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,this_id:this_id},
        success: function(context) {
            if(context.success == 1){
                var order_item = document.getElementsByClassName("order_items")
                document.getElementById("order_item"+this_id+"").remove()
                if(order_item.length == 0){
                    location.href = '/view_cart';
                }else{
                    var store_order_item = document.getElementsByClassName("order_items"+context.store_id+"")
                    if(store_order_item.length == 0){
                        var section1 = document.getElementsByClassName("store_section"+context.store_id+"")
                        // for(var i = 0; i < section1.length; i++){
                        //     section1[i].remove()
             
                        // }
                        $( ".store_section"+context.store_id+"" ).remove();
                    }
                    Swal.fire("Removed!", '', 'success')
                }
            }
        }
    });

}

function edit_variant_price(token,id){
    $.ajax({
        url:"/edit_variant_price",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,this_id:id,value:document.getElementById("price"+id+"").value},
        success: function() {
            
        }
    });
}

function varaint_available_switch(token,id,value){

    $.ajax({
        url:"/varaint_available_switch",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,this_id:id,value:value},
        success: function() {
            
        }
    });

}

function edit_variant_stocks(token,id){
    $.ajax({
        url:"/edit_variant_stocks",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,this_id:id,value:document.getElementById("variant_stocks"+id+"").value},
        success: function() {
            
        }
    });
}

function delete_variant(token,id){
    $.ajax({
        url:"/delete_variant",
        type:"POST",
        cache: false,
        // async:true;
        data:{csrfmiddlewaretoken: token,this_id:id},
        success: function(context) {
            $( "#variant_tr"+context.id+"" ).remove();
        }
    });
}

