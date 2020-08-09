from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import Order, Customer, Product
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import OrderForm, CreateUserForm
from .decorators import authenticared_user, allowed_users

# Create your views here.

def register(request):
    if request.user.is_authenticated:           #  Instead of using this method we can  
        return redirect('home')                 #  also use @authenticared_user Here to check that user is authenticated i.e. logged in here
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')

    context = {
        'form':form
    }
    return render(request, 'accounts/register.html', context)

@authenticared_user   #This method of checking is based on Decoratos like the inbuilt of @login_required...and we can use this for register functions also in views.py
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
    return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def userpage(request):
    context={

    }
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    
    total_orders = orders.count()

    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()

    context = {
        'orders' : orders,
        'customers' : customers,
        'total_orders' : total_orders,
        'delivered' : delivered,
        'pending' : pending,
    }

    return render(request, 'accounts/index.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()

    context ={
        'customer' : customer,
        'orders' : orders
    }

    return render(request, 'accounts/customer.html', context)

    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    context ={
        'products' : products
    }
    return render(request, 'accounts/products.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=5) #extra is here to add multiple orders a same time. Extra shows how much empty fields at a single time display
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer) # Here queryset=Order.objects.none() is used so that no saved orders are going to store in formset and they will now be displayed in the form of order_form.html
    #form = OrderForm(initial={'customer':customer})

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        #form = OrderForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context ={'formset' : formset}  #used formset here for multiple forms. Use *form* in context instead of formset and in order_form.html also to use a single form
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    formset = OrderForm(instance=order)
    if request.method == 'POST':
        formset = OrderForm(request.POST, instance=order)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset}
    return render(request, 'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    order.delete()
    return redirect('/')