from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.db.models import Q
from customer.forms import CustomerModelForm
from customer.models import Customer


# Create your views here.


def customers(request):
    page = request.GET.get('page',)
    customer_list = Customer.objects.all()
    paginator = Paginator(customer_list, 3)
    try:
        page_number = int(page)
    except (ValueError, TypeError):
        page_number = 1

    try:
        customer_page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        customer_page_obj = paginator.page(1)
    except EmptyPage:
        customer_page_obj = paginator.page(paginator.num_pages)

    search_query = request.GET.get('search')
    if search_query:
        customer_list = Customer.objects.filter(
            Q(full_name__icontains=search_query) | Q(address__icontains=search_query))
    # else:
    #     customer_list = Customer.objects.all()
    context = {
        'customer_page_obj': customer_page_obj,
        'customer_list': customer_list,
    }
    return render(request, 'customer/customer-list.html', context)


def add_customer(request):
    form = CustomerModelForm()
    if request.method == 'POST':
        form = CustomerModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customers')

    context = {
        'form': form,
    }

    return render(request, 'customer/add-customer.html', context)


def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if customer:
        customer.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            'Customer successfully deleted'
        )
        return redirect('customers')


def edit_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerModelForm(instance=customer)
    if request.method == 'POST':
        form = CustomerModelForm(instance=customer, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()

            return redirect('customers')
    context = {
        'form': form,
    }
    return render(request, 'customer/update-customer.html', context)
