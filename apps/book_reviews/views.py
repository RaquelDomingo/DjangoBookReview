from django.shortcuts import render, redirect
from django.urls import reverse
from models import Book, Author, Review
from ..login_reg.views import show_messages
from ..login_reg.models import User

# """
# Making a filter in order to generate a range in our templates. This is so we can create a for loop based on a number (rather than items in a list)
# """
from django.template import Library
register = Library()

def check_logged_in(request):
    # """
    # Use this function to return whether or not the user is logged in
    # """
    return 'user' in request.session

# """
# Registering a filter on this route in order to use it in our template to iterate over a range.
# This is so we can spit out star images.
# """
@register.filter
def index(request):
    if not check_logged_in(request):
        return render(request, 'login_reg/index.html')

    context = {
        'reviews' : Review.objects.fetch_recent(),
        'books' : Book.objects.all()
    }

    return render(request, 'book_reviews/index.html', context)

def new(request):
    if not check_logged_in(request):
        return redirect(reverse('users:index'))

    context = {
        'books' : Book.objects.all(),
        'authors' : Author.objects.all()
    }

    return render(request, 'book_reviews/new.html', context)

def create(request):
    if not check_logged_in(request):
        return redirect(reverse('users:index'))

    result = Review.objects.create_review(request.POST, request.session['user']['id'])

    if result[0] == True:
        return redirect(reverse('reviews:show', kwargs={'id': result[1].book.id }))
    else:
        print_messages(request, result[1])
        return redirect(reverse('reviews:new'))

@register.filter
def show(request, id):
    if not check_logged_in(request):
        return redirect(reverse('users:index'))

    book = Book.objects.get(id=id)
    return render(request, 'book_reviews/show.html', { 'book' : book })

@register.filter
def show_user(request, id):
    if not check_logged_in(request):
        return redirect(reverse('users:index'))

    user = User.objects.fetch_user_info(id)
    return render(request, 'book_reviews/show_user.html', { 'user' : user })

