from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import Order, Customer
from django.forms import inlineformset_factory

from .forms import OrderForm
from django.forms import inlineformset_factory

# Create your views here.

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
        'pending' : pending
    }

    return render(request, 'accounts/index.html', context)

def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()

    context ={
        'customer' : customer,
        'orders' : orders
    }

    return render(request, 'accounts/customer.html', context)

    
def products(request):
    products = Product.objects.all()
    context ={
        'products' : products
    }
    return render(request, 'accounts/products.html',context)

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

def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    order.delete()
    return redirect('/')