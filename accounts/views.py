from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import Order, Customer, Product
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import OrderForm, CreateUserForm

# Create your views here.

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form':form
    }
    return render(request, 'accounts/register.html', context)

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

@login_required(login_url='login')
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
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()

    context ={
        'customer' : customer,
        'orders' : orders
    }

    return render(request, 'accounts/customer.html', context)

    
@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    context ={
        'products' : products
    }
    return render(request, 'accounts/products.html',context)

@login_required(login_url='login')
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
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html',context)

@login_required(login_url='login')
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    order.delete()
    return redirect('/')