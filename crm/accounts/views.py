from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Customer, Order, Product
from .forms import OrderForm, CreateUserForm, UserSettingFrom
from .filters import OrderFilter
from .decorations import unauthenticated_user, allowed_users, admin_only

# Create your views here.

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, "Аккаунт успешно создан для " + username)

            form.save()

            return redirect('login')

    context = {
        'form':form,
    }
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, password=password, username=username)

    if request.method == "POST":
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Логин или пароль неверный')

    context = {

    }
    return render(request, 'accounts/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = Order.objects.all().count()
    delivered_orders = orders.filter(status='Доставлен').count()
    pending_orders = orders.filter(status='В ожидании').count()
    context = {
        'customers' : customers,
        'orders': orders,
        'total_orders': total_orders,
        'delivered_orders': delivered_orders,
        'pending_orders': pending_orders,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@admin_only
def products(request):
    products= Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'accounts/products.html', context)

@login_required(login_url='login')
@admin_only
def customer(request, pk):
    costumer = Customer.objects.get(id=pk)
    orders = costumer.order_set.all()
    total_orders = orders.count()

    myfilter = OrderFilter(request.GET, queryset=orders)
    orders = myfilter.qs

    context = {
        'costumer': costumer,
        'orders': orders,
        'total_orders': total_orders,
        'myfilter': myfilter,
    }

    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@admin_only
def created_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=6)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)

    if request.method == "POST":
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context ={
        "formset": formset,
    }
    return render(request, 'accounts/order_form.html',context)

@login_required(login_url='login')
@admin_only
def upgrade_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == "POST":
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context ={
        "form": form,
    }
    return render(request, 'accounts/order_form.html',context)

@login_required(login_url='login')
@admin_only
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context ={
        "order": order,
    }
    return render(request, 'accounts/delete.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.all().count()
    delivered_orders = orders.filter(status='Доставлен').count()
    pending_orders = orders.filter(status='В ожидании').count()

    context ={
        'orders':orders,
        'total_orders': total_orders,
        'delivered_orders': delivered_orders,
        'pending_orders': pending_orders,
    }
    return render(request, 'accounts/userpage.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def settingsUser(request):
    user = request.user.customer
    form = UserSettingFrom(instance=user)

    if request.method == "POST":
        form = UserSettingFrom(request.POST,request.FILES,instance=user)
        form.save()

    context = {
        'form':form,
    }
    return render(request, 'accounts/account_settings.html', context)