import json
from . models import *

def cookieCart(request):
    items =[]
    # if the cookie doesnt exist try catch
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
            cart={}
    order = {'get_cart_total':0,'get_cart_items':0}
    cartItems = order['get_cart_items']
    for i in cart:
        cartItems +=cart[i]["quantity"]
        # get the product
        product = Product.objects.get(id=i)
        total = (product.price * cart[i]["quantity"])

        order['get_cart_total'] += total
        order['get_cart_items'] += cart[i]["quantity"]

        item = {
            'product':{
                'id':product.id,
                'name':product.name,
                'price':product.price,
                'get_photo_url':product.get_photo_url,
            },
            'quantity':cart[i]["quantity"],
            'get_total':total
        }
        items.append(item)
        # if its a physical product
        if(product.digital == False):
            order['shipping'] = True

    
    return {'items':items,'order':order,'cartItems':cartItems}

def guestOrder(request,data):
        print('COOKIES', request.COOKIES)
        name = data['form']['name']
        email = data['form']['email']
        cookieData = cookieCart(request)
        items = cookieData['items']

        customer, created = Customers.objects.get_or_create(email=email)

        customer.name = name
        customer.save()

        order = Order.objects.create(
            customer=customer,
            complete=False
        )

        for item in items:
            product = Product.objects.get(id=item['product']['id'])

            orderitem = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity']
            )
    
        return customer,order

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # you either find or create an order
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        items = cookieData['items']
        order = cookieData['order']
    return {'items':items,'order':order,'cartItems':cartItems}