from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *


def home(request):
    return render(request, 'home.html', context={
        'jewerlies': Jewerly.objects.all()[:4]
    })


def jewerly_details(request, pk):
    if request.method == 'POST':
        jewerly = get_object_or_404(Jewerly, pk=pk)
        current_user = CustomUser.objects.all().filter(user=request.user).first()
        cart = ShoppingCart.objects.all().filter(user=current_user, active=True).first()
        cart_item = CartItem.objects.create(jewerly=jewerly, quantity=1,
                                            cart=cart)
        cart_item.save()
        return redirect('cart')
    jewerly = get_object_or_404(Jewerly, pk=pk)
    return render(request, 'jewerly_details.html', context={
        'jewerly': jewerly
    })


def store(request):
    jewerlies = Jewerly.objects.all()
    type_choices = Jewerly.type_choices
    search_query = request.GET.get('search')
    if search_query:
        jewerlies = jewerlies.filter(name__icontains=search_query)

    type_filter = request.GET.get('type')
    if type_filter:
        jewerlies = jewerlies.filter(type=type_filter)

    exclusive_filter = request.GET.get('exclusive')
    if exclusive_filter == 'yes':
        jewerlies = jewerlies.filter(exclusive=True)
    elif exclusive_filter == 'no':
        jewerlies = jewerlies.filter(exclusive=False)

    return render(request, 'store.html', context={'jewerlies': jewerlies, 'type_choices': type_choices})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            current_user = CustomUser.objects.all().filter(user=form.get_user()).first()
            cart = ShoppingCart.objects.all().filter(user=current_user, active=True).first()
            if not cart:
                cart = ShoppingCart.objects.create(user=current_user, active=True)
                cart.save()
            return redirect('/')

    return render(request, 'login.html', {'form': BootstrapAuthenticationForm()})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'register.html', {'form': RegisterForm()})


def logout_view(request):
    logout(request)
    return redirect('/')


def cart_view(request):
    current_user = CustomUser.objects.all().filter(user=request.user).first()
    cart = ShoppingCart.objects.all().filter(user=current_user, active=True).first()
    cart_items = CartItem.objects.all().filter(cart=cart)
    total_price = 0
    for item in cart_items:
        total_price += item.get_total()

    if request.method == 'POST':
        cart.active = False
        cart.save()
        order = Order.objects.create(user=current_user, total=total_price, cart=cart)
        order.save()
        new_cart = ShoppingCart.objects.create(user=current_user, active=True)
        new_cart.save()
        return redirect('successful_order')

    return render(request, 'cart.html', context={
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price})


def faq_view(request):
    return render(request, 'faq.html')


def successful_order_view(request):
    return render(request, 'successful_order.html')


def my_orders_view(request):
    current_user = CustomUser.objects.filter(user=request.user).first()
    orders = Order.objects.filter(user=current_user)

    order_cart_items_map = {}

    for order in orders:
        cart_items = CartItem.objects.filter(cart=order.cart)
        order_cart_items_map[order] = cart_items

    return render(request, 'my_orders.html', context={
        'order_cart_items_map': order_cart_items_map
    })
