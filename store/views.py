from django.shortcuts import render
from django.http import JsonResponse
import datetime
from .models import *
import json


# Create your views here.

def store(request):
    # check if user is authenticated
    if request.user.is_authenticated:
        customer = request.user.customer
        # you either find or create an order
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order = {'get_cart_total':0,'get_cart_items':0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context={'products':products,'cartItems':cartItems}
    return render(request,'store/store.html',context)


def  cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        # you either find or create an order
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order = {'get_cart_total':0,'get_cart_items':0}
        cartItems = order['get_cart_items']
    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/cart.html',context)




def  checkout(request):
    # check if user is authenticated
    if request.user.is_authenticated:
        customer = request.user.customer
        # you either find or create an order
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/checkout.html',context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    # get the current customer
    customer = request.user.customer
    product = Product.objects.get(id=productId)

    # creat or get the order where the order is not complete
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    # check if user is authenticated
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id  
        # check if the total from the front end is equals to total from backend
        if total == order.get_cart_total: 
            order.complete = True
        order.save()
        print(order.shipping)

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shippingInfo']['address'],
                city=data['shippingInfo']['city'],
                county=data['shippingInfo']['county']
            )

    return JsonResponse('payment Complete', safe=False)

