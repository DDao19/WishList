# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import bcrypt
import re

NAME_REGEX = re.compile(r'^[ .a-zA-Z0-9\s]+$')

# Create your models here.
class UserManager(models.Manager):
    def validate_registration(self, form_data):
        errors = []

        if len(form_data['name']) < 3:
            errors.append("Name must be at least 3 characters.")
        if len(form_data['username']) < 3:
            errors.append("Username must be at least 3 characters.")
        #check if name and username is valid
        if not re.match(NAME_REGEX, form_data['name']):
            errors.append('Invalid Name.')
        if not re.match(NAME_REGEX, form_data['username']):
            errors.append('Invalid Username.')

        #check if password valid
        if len(form_data['password']) == 0:
            errors.append("Password is required.")
        if form_data['password'] != form_data['confirm_password']:
            errors.append("Password must match.")
        #DOH validation
        if len(form_data['doh']) == 0:
            errors.append('Must include date hired')
        else:
            user_doh = datetime.strptime(form_data['doh'], "%Y-%m-%d")
            current_date = datetime.now()
            if user_doh > current_date:
                errors.append("DOH cannot be current date")
        return errors

    def validate_login(self, form_data):
        errors = []
        if len(form_data['username']) == 0:
            errors.append("Enter username.")
        if len(form_data['password']) == 0:
            errors.append("Enter password.")
        if len(self.filter(username=form_data['username'])) > 0:
            user = self.filter(username=form_data['username'])[0]
            if not bcrypt.checkpw(form_data['password'].encode(), user.password.encode()):
                errors.append('Username or Password is incorrect.')
        else:
            errors.append('Username or Password is incorrect.')

        if errors:
            return errors
        return user


    def create_user(self, form_data):
        hashedpw = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt(6))
        return User.objects.create(
            name = form_data['name'],
            username = form_data['username'],
            password = hashedpw,
            date_hired = form_data['doh']
        )

class ProductManager(models.Manager):

    def validate_product(self, form_data):
        errors = []

        if len(form_data['item_product']) < 3:
            errors.append("Must be at least 3 characters.")

        return errors


class User(models.Model):
    name = models.CharField(max_length=40)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    date_hired = models.DateField()
    wish_list = models.ManyToManyField("Product", related_name="wish_list", default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return "{}, {}, {}, {}".format(self.name, self.alias, self.email, self.date_of_birth)

class Product(models.Model):
    item = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductManager()
