# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return redirect(main)

def main(request):
    return render(request, 'qoutes/main.html')

def dashboard(request):
    if request.session.get('id') is None:
        return redirect(main)
    user = User.objects.get(id=request.session['id'])
    all_qoutes = Qoute.objects.exclude(followed_by__id=user.id).order_by('-id').all()
    fav_qoutes = Qoute.objects.filter(followed_by=user.id).order_by('-id').all()
    context = {
        'user': user,
        'all_qoutes': all_qoutes,
        'fav_qoutes': fav_qoutes,
    }
    return render(request, 'qoutes/dashboard.html', context)

def users(request, user_id):
    if request.session.get('id') is None:
        return redirect(main)   
    user = User.objects.get(id=user_id)
    qouteCount = user.posted_qoutes.count()
    usersQoutes = user.posted_qoutes.all()
    context = {
        'user': user,
        'qouteCount': qouteCount,
        'usersQoutes': usersQoutes,
    }
    return render(request, 'qoutes/users.html', context)

#qoute processses
def addQoute(request):
    if request.method == 'POST':
        errors = Qoute.objects.qouteValidator(request.POST)
        if errors:
            for e in errors:
                messages.error(request, e)
            return redirect(dashboard)
        Qoute.objects.create(qoute_by=request.POST['qoute_by'], message=request.POST['message'], posted_by=User.objects.get(id=request.session['id']))
        return redirect(dashboard)

def followQoute(request, qoute_id):
    if request.method == 'POST':
        current_qoute = Qoute.objects.get(id=qoute_id)
        current_user = User.objects.get(id=request.session['id'])
        current_qoute.followed_by.add(current_user)
        return redirect(dashboard)

def removeQoute(request, qoute_id):
    if request.method == 'POST':
        current_qoute = Qoute.objects.get(id=qoute_id)
        current_user = User.objects.get(id=request.session['id'])
        current_qoute.followed_by.remove(current_user)   
        return redirect(dashboard)     

#login-reg-logout managers
def register(request):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        if errors.get('password') is not None or errors['error']:
            if errors['error']:
                for error in errors['error']:
                    messages.error(request, error)
            if errors.get('password') is not None:
                for error in errors['password']:
                    messages.error(request, error)
            return redirect(index)
    hashed_password = User.objects.password_hasher(request.POST['password'])
    User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], birthday=request.POST['birthday'], password=hashed_password)
    request.session['id'] = User.objects.get(email=request.POST['email']).id
    return redirect(dashboard)

def login(request):
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])
        if user:
            if User.objects.password_checker(request.POST['password'], user[0].password):
                request.session['id'] = user[0].id
                return redirect(dashboard)
            else:
                return redirect(main)
        else:
            messages.warning(request, 'Email did not match password')
            return redirect(main)

def logout(request):
    del request.session['id']
    return redirect(main)