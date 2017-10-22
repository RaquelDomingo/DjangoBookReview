from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Count
import re, bcrypt

name_regex = re.compile(r"^[a-zA-Z\-]+$")
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):

    def loginValidate(self, request):
        try:
            user = User.objects.get(email=request.POST['email'].strip().lower())
            password = request.POST['password'].encode()
            hashed_pw = user.pw_hash.encode()
            print user
            print password
            print hashed_pw

            if hashed_pw == bcrypt.hashpw(password, hashed_pw):
                return (True, user)

        except ObjectDoesNotExist:
            print("A user with that Email does not exist.")
            pass

        return (False, ["Incorrect Password/Email, or the User does not exist."])

    def regValidate(self, request):
        errors = []

        if User.objects.filter(email=request.POST['email'].strip().lower()):
            errors.append("A user with that Email Address already exists!  Please Log In.")

        if len(request.POST['first_name']) < 1 or len(request.POST['last_name']) < 1:
            errors.append("The First/Last Name fields cannot be blank! They must each have at least 1 character.")

        elif not name_regex.match(request.POST['first_name']) or not name_regex.match(request.POST['last_name']):
            errors.append("You may not include any numbers or special characters in First or Last name.")

        if not EMAIL_REGEX.match(request.POST['email']):
            errors.append("Please enter a valid Email!  (Example: email@email.com)")

        if len(request.POST['password']) < 8:
            errors.append('Your Password must contain 8 or more characters!')

        if request.POST['password'] != request.POST['confirm_pw']:
            errors.append('Your Password and Confirm Password must match!')

        if errors:
            return(False, errors)

        #Create the PW Hash if no errors
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print pw_hash

        #Create New User once the PW is hashed
        user = self.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'].strip().lower(), pw_hash=pw_hash)

        return (True, user)

    def fetch_user_info(self, id):
        print "fetched"
        return self.filter(id=id).annotate(total_reviews=Count('review'))[0]
        from ..book_reviews.models import Book
        user_id = int(user_id)
        try:
            user = self.get(id=user_id)
            print "got user"
            user_reviews = User.objects.filter(id=user_id).annotate(num=Count('user_review'))
            print user_reviews[0].num
            books = Book.objects.filter(book_reviews__review_user=user)
            print books
        
            response = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'total_reviews': user_reviews[0].num,
                'books': books,
            }
            return (True, response)
        except:
            errors = "There was a problem loading this user."
            return (False, errors)

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, null=False)
    pw_hash = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()