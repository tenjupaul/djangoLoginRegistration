from django.db import models
import datetime
import re
import bcrypt

today=datetime.datetime.now()

# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validation(self,postData):
        errors={}
        ifEmailExists=User.objects.filter(email=postData['email'])
        if len(postData['email'])<1:
            errors['email'] = "Email cannot be blank"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['invalidEmail']="Invalid Email Address!"
        elif len(ifEmailExists):
            errors['emailexist']= "User with email - "+postData['email']+" already exists!"
        if len(postData['first_name'])<1:
            errors['first_name']="First name cannot be blank"
        elif len(postData['first_name'])<2:
            errors['first_nameLen']="First name should have at least 2 characters"
        elif not str.isalpha(postData['first_name']):
            errors['first_nameNum']="First name cannot contain any numbers"
        if len(postData['last_name'])<1:
            errors['last_name']="Last name cannot be blank"
        elif len(postData['last_name'])<2:
            errors['last_nameLen']="Last name should have at least 2 characters"
        elif not str.isalpha(postData['last_name']):
            errors['last_nameNum']="Last name cannot contain any numbers"
        if len(postData['dob'])<1:
            errors['dob']="Date of Birth cannot be blank"
        else:
            dob=datetime.datetime.strptime(postData['dob'],'%Y-%m-%d')
            if dob>today:
                errors['dob_date']="Invalid Date of Birth"
        if len(postData['password'])<1:
            errors['password']="Password cannot be blank"
        elif len(postData['password'])<8:
            errors['passwordLen']="Password should be more than 8 characters"
        elif not re.search(r"[A-Z]+", postData['password']) or not re.search(r"[0-9]+", postData['password']):
            errors['passwordInvalid']="Password should have at least 1 uppercase letter and 1 numeric value."
        if len(postData['confirm_password'])<1:
            errors['conf_password']="Confirm Password cannot be blank"
        elif postData['confirm_password']!=postData['password']:
            errors['password_match']="Password and Password Confirmation should match"
        return errors

    def login_validation(self,postData):
        errors={}
        user = User.objects.filter(email=postData['loginemail'])
        if len(postData['loginemail'])<1 or len(postData['loginpassword'])<1:
            errors['emptyField']="Email and password fields cannot be empty"
        # print(user.values()[0]['password'])
        elif not len(user):
            print("not found")
            errors['noemail']="Invalid login!"
        elif not bcrypt.checkpw(postData['loginpassword'].encode(), user.values()[0]['password'].encode()):
            errors['failedAuth']="Invalid login!"
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=225)
    last_name=models.CharField(max_length=225)
    email=models.CharField(max_length=225)
    dob=models.DateField()
    password=models.CharField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()



