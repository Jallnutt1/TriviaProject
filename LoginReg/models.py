from django.db import models
from datetime import datetime
import bcrypt
import re

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
        today = datetime.today()

        if not postData['first_name']:
            errors['first_name'] = "Must enter a first name"
        if not postData['last_name']:
            errors['last_name'] = "Must enter a last name"

        if not postData['birthday']:
            errors['birthday'] = "Must enter a birthday"
        else:
            birthday = datetime.strptime(postData['birthday'], '%Y-%m-%d')
            if today < birthday:
                errors['birthday'] = "Birthday must be in the past"
            elif (birthday.year + 13, birthday.month, birthday.day) > (today.year, today.month, today.day):
                errors['birthday'] = "You must be at least 13 years of age"

        if not postData['email']:
            errors['email'] = "Must enter an email"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Please enter a valid email"
        elif User.objects.filter(email=postData['email']).exists():
            errors['email'] = "Email already exists"

        if not postData['password']:
            errors['password'] = "Must enter a password"
        elif len(postData['password']) < 8:
            errors['password'] = "Password must be 8 characters"
        elif postData['password'] != postData['confirm']:
            errors['password'] = "Password and Confirm Password do not match"
        
        return errors

    def login_validator(self, postData):
        errors={}

        if postData['email'] and postData['password']:
            if not User.objects.filter(email=postData['email']).exists():
                errors['email'] = "Login attempt failed (email)"
            else:
                user = User.objects.get(email=postData['email'])
                # hashed_password = user.password
                if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                    errors['login'] = 'Login attempt failed (password)'   
        else:
            if not postData['email']:
                errors['email'] = "Please enter a valid email"
            if not postData['password']:
                errors['password'] = "Please enter a valid password"
                
        return errors

    def update_validator(self, postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
        today = datetime.today()
        update_user = User.objects.get(id=postData['user_id'])

        if not postData['first_name']:
            errors['first_name'] = "Must enter a first name"
        if not postData['last_name']:
            errors['last_name'] = "Must enter a last name"

        if not postData['birthday']:
            errors['birthday'] = "Must enter a birthday"
        else:
            birthday = datetime.strptime(postData['birthday'], '%Y-%m-%d')
            if today < birthday:
                errors['birthday'] = "Birthday must be in the past"
            elif (birthday.year + 13, birthday.month, birthday.day) > (today.year, today.month, today.day):
                errors['birthday'] = "You must be at least 13 years of age"

        if not postData['email']:
            errors['email'] = "Must enter an email"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Please enter a valid email"
        elif postData['email'] != update_user.email:
            if User.objects.filter(email=postData['email']).exists():
                errors['email'] = "Email already exists"
                print(postData['email'], update_user.email)

        return errors

    def password_change_validator(self, postData):
        errors={}

        if postData['current_password'] and postData['new_password'] and postData['confirm_password']:
            user=User.objects.get(id=postData['user_id'])
            user_current_password = user.password
            if not bcrypt.checkpw(postData['current_password'].encode(), user.password.encode()):
                errors['password'] = "Current password does not match"
            else:
                if len(postData['new_password']) < 8:
                    errors['password'] = "Password must be 8 characters"
                elif postData['new_password'] != postData['confirm_password']:
                    errors['password'] = "Password and Confirm Password do not match"
        else:
            errors['password'] = "All fields are required"
        
        return errors




class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    birthday=models.DateField(null=True, blank=True)
    email=models.CharField(max_length=255, blank=True)
    password=models.CharField(max_length=255, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

