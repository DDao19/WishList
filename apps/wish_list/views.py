# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib import messages
from .models import User, Product

# Create your views here.
def flash_errors(errors, request):
    for error in errors:
        messages.error(request, error)

def current_user(request):
    return User.objects.get(id=request.session['user_id'])

def index(request):

    return render(request, 'wish_list/index.html')

def dashboard(request):
    if 'user_id' in request.session:
        logged_user = current_user(request)
        my_products = logged_user.products.all()
        other_products = Product.objects.exclude(id__in=my_products)
        others_wl = logged_user.wish_list.all()
        context = {
            'logged_user': logged_user,
            'my_products': my_products,
            'other_products': other_products,
            'others_wl': others_wl,

        }
        return render(request, 'wish_list/dashboard.html', context)

    return redirect(reverse('landing'))


def register(request):
    if request.method == "POST":
        errors = User.objects.validate_registration(request.POST)
        if not errors:
            user = User.objects.create_user(request.POST)
            request.session['user_id'] = user.id
            messages.success(request, "Successfully logged in!")
            return redirect(reverse('dashboard'))

        flash_errors(errors, request)

    return redirect(reverse('landing'))

def login(request):
    if request.method == "POST":
        result = User.objects.validate_login(request.POST)
        if type(result) == list:
            for err in result:
                messages.error(request, err)
            return redirect(reverse('landing'))
        request.session['user_id'] = result.id
        messages.success(request, "Successfully logged in!")
    return redirect(reverse('dashboard'))

def logout(request):
    if 'user_id' in request.session:
        request.session.pop('user_id')

    return redirect(reverse('landing'))
#---------------------------------------------------

def add(request):
    return render(request, 'wish_list/create.html')

def create(request):
    if request.method == "POST":
        errors = Product.objects.validate_product(request.POST)
        if not errors:
            Product.objects.create(item=request.POST['item_product'], poster=current_user(request))
            return redirect(reverse('dashboard'))

        flash_errors(errors, request)
    return redirect(reverse('dashboard'))

def add_wishlist(request, id):
    user = current_user(request)
    new_item = Product.objects.get(id=id)
    user.wish_list.add(new_item)
    return redirect(reverse('dashboard'))

def delete(request, id):
    Product.objects.get(id=id).delete()
    return redirect(reverse('dashboard'))

def remove(request, id):
    user = current_user(request)
    new_item = Product.objects.get(id=id)
    user.wish_list.remove(new_item)
    return redirect(reverse('dashboard'))

def user(request, id):
    user = User.objects.get(id=id)
    my_products = user.products.all()
    other_products = Product.objects.exclude(id__in=my_products)
    context = {
        'user': user,
        'my_products': my_products,
        'other_products': other_products,
        'others_wl': user.wish_list.all(),
    }
    return render(request, 'wish_list/users.html', context)
