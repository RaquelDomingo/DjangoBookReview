from django.shortcuts import render, redirect
from django.urls import reverse
# from django.core.urlresolvers import reverse
from django.contrib import messages
from models import User

# Create your views here.
def index(request):
    return redirect(reverse('users:index'))

def login(request):
    result = User.objects.loginValidate(request)

    if result[0] == False:
        show_messages(request, result[1])
        return redirect(reverse('users:index'))

    return log_in_user(request, result[1])

def register(request):
    result = User.objects.regValidate(request)

    if result[0] == False:
        show_messages(request, result[1])
        return redirect(reverse('users:index'))

    return log_in_user(request, result[1])

def success(request):
    if not 'user' in request.session:
        return redirect(reverse('users:index'))
    ##Success brings user to the Review section
    return redirect(reverse('reviews:index'))

def show_messages(request, message_list):
    for message in message_list:
        messages.add_message(request, messages.INFO, message)

def log_in_user(request, user):
    request.session['user'] = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }
    return redirect(reverse('users:success'))

def logout(request):
    request.session.clear()
    return redirect(reverse('users:index'))