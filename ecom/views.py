from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# views.py
from django.http import JsonResponse
from django.template.loader import render_to_string
from datetime import datetime
from Home.models import *





@login_required(login_url='SignIn')
def Products(request):
    product = Product.objects.all()
    if request.method == 'POST':
        product_name = request.POST['name']
        product_sub_name = request.POST.get('sub_name', '')
        category_id = request.POST['category']
        price = request.POST['price']
        product_BV = request.POST['bv']
        stock = request.POST['stock']
        stock_alert_value = request.POST['stock_alert']
        tax = request.POST['tax_name']
        tax_value_id = request.POST['tax_value']
        description = request.POST.get('description', '')

        try:

            category = ProductCategory.objects.get(id=category_id)
            tax_value = Tax.objects.get(id=tax_value_id)

            product = Product.objects.create(
                category=category,
                product_name=product_name,
                product_sub_name=product_sub_name,
                price=price,
                product_BV=product_BV,
                stock=stock,
                stock_alert_value=stock_alert_value,
                tax=tax,
                tax_value=tax_value,
                description=description
                 
            )
        except:
            messages.error(request,"Somthing Wrong...")
            return redirect(Products)
        try:
            if 'primary_image' in request.FILES:
                primary_image = request.FILES['primary_image']
                product.image_primary = primary_image
            
            if 'secondary_image1' in request.FILES:
                secondary_image1 = request.FILES['secondary_image1']
                product.image_s1 = secondary_image1
            
            if 'secondary_image2' in request.FILES:
                secondary_image2 = request.FILES['secondary_image2']
                product.image_s2 = secondary_image2
            product.save()
        except:
            messages.error(request,"Somthing Wrong...images are not saved....")
            return redirect(Products)

        messages.success(request,"Product Added Success")
        return redirect("Products")

    else:

        return render(request, 'dashboard/products.html', { 'food_category': ProductCategory.objects.all(),
                                                            'tax': Tax.objects.all(),
                                                            "product":product})
    


def ProductList(request):
    product = Product.objects.all()

    context = {
        "products":product
    }
    return render(request,"product_list.html",context)

def ProductSingle(request,pk):
    product = Product.objects.get(id = pk)
    context = {
        "product":product
    }
    return render(request,'productsingle.html',context)


@login_required(login_url='SignIn')
def Cart_Page(request):
    cart_items = Cart.objects.filter(user=request.user)
    # Initialize total price and total tax
    total_price = 0.0
    total_tax = 0.0
    bv = 0

    # Iterate through the cart items to calculate the totals
    for item in cart_items:
        total_price += item.total_price
        total_tax += item.quantity * item.product.tax_amount
        bv += item.total_bv

    # Pass the calculated totals to the context
    context = {
        'cart_items': cart_items,
        'total_price': round(total_price, 2),
        'total_tax': round(total_tax, 2),
        "total_price_defore_tax": round(total_price - total_tax,2),
        "total_items": cart_items.count(),
        "bv":bv
    }
    
    return render(request,"cart.html",context)


@login_required(login_url='SignIn')
def AddToCart(request,pk):
    product = Product.objects.get(id = pk)
    try:
        if Cart.objects.filter(product = product,user = request.user).exists():
            item = Cart.objects.get(product = product,user = request.user)
            item.quantity = item.quantity + 1
            item.save()
            item.total_price = product.price * item.quantity
            item.total_bv = item.total_bv + product.product_BV
            item.save()
        else:
            cartitem = Cart.objects.create(
                product = product,
                user = request.user,
                quantity = 1,
                total_price = product.price,
                total_bv = product.product_BV
            )
            cartitem.save()
            messages.success(request,"Product added to cart")
            return redirect("Cart_Page")

    except:
        messages.success(request,"Product added to cart")
        return redirect("Cart_Page")

    return redirect("Cart_Page")





def increase_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        cart_item = Cart.objects.get(id=item_id)
        cart_item.quantity += 1
        cart_item.total_price = cart_item.quantity * cart_item.product.price  # Assuming product has a price field
        cart_item.total_bv = cart_item.total_bv + cart_item.product.product_BV
        cart_item.save()

        # Recalculate the cart summary and return updated HTML
        cart_items = Cart.objects.filter(user=request.user)
        total_price = 0.0
        total_tax = 0.0
        bv = 0

        # Iterate through the cart items to calculate the totals
        for item in cart_items:
            total_price += item.total_price
            total_tax += item.quantity * item.product.tax_amount
            bv += item.total_bv

        # Pass the calculated totals to the context
        context = {
            'cart_items': cart_items,
            'total_price': round(total_price, 2),
            'total_tax': round(total_tax, 2),
            "total_price_defore_tax": round(total_price - total_tax,2),
            "total_items": cart_items.count(),
            "bv":bv
        }
        order_html = render_to_string('ajaxtemplates/cartitems.html', context)
        
        return JsonResponse({'order_html': order_html})

def decrease_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        cart_item = Cart.objects.get(id=item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.total_price = cart_item.quantity * cart_item.product.price
            cart_item.total_bv = cart_item.total_bv - cart_item.product.product_BV
            cart_item.save()

        # Recalculate the cart summary and return updated HTML
        # Recalculate the cart summary and return updated HTML
        cart_items = Cart.objects.filter(user=request.user)
        total_price = 0.0
        total_tax = 0.0
        bv = 0

        # Iterate through the cart items to calculate the totals
        for item in cart_items:
            total_price += item.total_price
            total_tax += item.quantity * item.product.tax_amount
            bv += item.total_bv

        # Pass the calculated totals to the context
        context = {
            'cart_items': cart_items,
            'total_price': round(total_price, 2),
            'total_tax': round(total_tax, 2),
            "total_price_defore_tax": round(total_price - total_tax,2),
            "total_items": cart_items.count(),
            "bv":bv
        }
        order_html = render_to_string('ajaxtemplates/cartitems.html', context)
        
        return JsonResponse({'order_html': order_html})

@login_required(login_url='SignIn')    
def deletefrom_cart(request,pk):
    try:
        Cart.objects.get(id = pk).delete()
        messages.success(request,"Product deleted from cart")
        return redirect("Cart_Page")
    except:
        messages.info(request,"Item Not deleted Somthing Wrong")
        return redirect("Cart_Page")
    
    
@login_required(login_url='SignIn')
def Place_Order_Start(request):
    user = request.user
    if Cart.objects.filter(user = user).count() > 0:
        cart_items = Cart.objects.filter(user = user)

        # creating delivery adderss
        if DeliveryAddress.objects.filter(user = request.user).exists():
            
            D_address = DeliveryAddress.objects.filter(user = request.user).last()
        else:
            D_address = DeliveryAddress.objects.create(
                user = user,
                first_name = user.first_name,
                house_house = user.address,
                Place  = user.village,
                City = user.village,
                district = user.district,
                state = "Kerala",
                phone_number = user.phone_number

            )
            D_address.save()

        total_price = 0.0
        total_tax = 0.0
        bv = 0
        for item in cart_items:  
            total_price += item.total_price
            total_tax += item.quantity * item.product.tax_amount
            bv += item.total_bv

        context = {
            'cart_items': cart_items,
            'total_price': round(total_price, 2),
            'total_tax': round(total_tax, 2),
            "total_price_defore_tax": round(total_price - total_tax,2),
            "total_items": cart_items.count(),
            "bv":bv,
            "D_address":D_address
        }
        return render(request,'place_order.html',context)
    else:
        messages.info(request,"Your cart is empty to place order !!")
        return redirect("Cart_Page")
    
@login_required(login_url='SignIn')   
def Paymentoptions(request,pk):
    order = Order.objects.get(id = pk)
    total_items = OrderItems.objects.filter(order = order).count()
    D_address = order.delivery_address

    context = {
        "order":order,
        "total_items":total_items,
        "D_address":D_address
    }
    return render(request,"paymentoptions.html",context)

@login_required(login_url='SignIn')
def Deleteoreder(request,pk):
    order = Order.objects.get(id = pk)
    if order.payment_status == True or order.order_status == True or order.order_completion == True:
        messages.info(request,'You cannot delete placed Order')
    else:
        order.delete()
        messages.success(request,"Order deleted")
    return redirect("myorders")

def generate_serial_number():
        current_time = datetime.now()
        serial_number = current_time.strftime("%Y%m%d%H%M%S")
        return serial_number


@login_required(login_url='SignIn')
def PlaceOrder(request):
    D_address = DeliveryAddress.objects.filter(user = request.user).last()
    cart_items = Cart.objects.filter(user = request.user)
    total_price = 0.0
    total_tax = 0.0
    bv = 0
    for item in cart_items:  
        total_price += item.total_price
        total_tax += item.quantity * item.product.tax_amount
        bv += item.total_bv

    order = Order.objects.create(
        order_numer = generate_serial_number(),
        user = request.user,
        order_amount = total_price,
        order_bv = bv,
        order_tax  = total_tax,
        delivery_address = D_address,
        delivery_history_address = str(D_address)

    )
    order.save()
    for item in cart_items:
        orderitem = OrderItems.objects.create(
            order = order,
            product = item.product,
            user = request.user,
            quantity = item.quantity,
            total_price = item.total_price,
            total_bv = item.total_bv
        )
        orderitem.save()
        item.delete()
    messages.info(request,'Order Created')

    return redirect("Paymentoptions",pk = order.id)


@login_required(login_url='SignIn')
def myorders(request):
    orders = Order.objects.filter(user = request.user)
    orderitems = OrderItems.objects.filter(user = request.user)

    print(orderitems,"------------------------------------------")

    context = {
        "orders":orders,
        "orderitems":orderitems
    }
    return render(request,'myorders.html',context)


@login_required(login_url='SignIn')
def MakeCashOnDelivery(request,pk):
    order = Order.objects.get(id = pk)
    order_items = OrderItems.objects.filter(order = order)
    order.order_completion = True
    order.payment_mode = "Cash On delivery"
    order.save()

    for i in order_items:
        i.order_progress = "Ordered"
        i.save()

    member = order.user 
    myBV = Business_Volume.objects.get(user = member)
    myBV.purchase_bv += order.order_bv
    myBV.save()

    order_BV = order.order_bv
    print(member,".................",order_BV)
    count = 0
    sponser = member.parent
    for i in range(5):
        count += 1
        try:
            bv_DB = Business_Volume.objects.get(user = sponser)
            if count == 1:
                print(count,"first refrel")
                bv_DB.bv_amount += (order.order_bv)*25/100
                bv_DB.save()
            elif count == 2:
                bv_DB.bv_amount += (order.order_bv)*12/100
                bv_DB.save()

            elif count == 3:
                bv_DB.bv_amount += (order.order_bv)*10/100
                bv_DB.save()

            elif count == 4:
                bv_DB.bv_amount += (order.order_bv)*6/100
                bv_DB.save()

            elif count == 5:
                bv_DB.bv_amount += (order.order_bv)*2/100
                bv_DB.save()

            else:
                break
        except:
            break
        sponser = sponser.parent

    try:
        parent = member.parent
        print(parent)
        if not parent:
            print("no parent admin......1234")
        
    except:
        print("no parent admin......")
    return redirect("OrderPlaced")


@login_required(login_url='SignIn')
def OrderPlaced(request):
    return render(request, 'orderplaced.html')


    

   