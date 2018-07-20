from django.shortcuts import render,HttpResponse, redirect
from django.contrib import messages
from .models import *


# Create your views here.
def index(request):
    if not request.session.keys():
        request.session['first_name']=""
        request.session['last_name']=""
        request.session['email']=""
        request.session['dob']=""
        request.session['loginemail']=""
        request.session['registerError']=False
        request.session['loginError']=False
    return render(request,'login_registration/index.html')

def register(request):
    if request.method=='POST':
        errors=User.objects.register_validation(request.POST)
        if len(errors):
            request.session['first_name']=request.POST['first_name']
            request.session['last_name']=request.POST['last_name']
            request.session['email']=request.POST['email']
            request.session['dob']=request.POST['dob']
            for key,value in errors.items():
                messages.error(request,value,extra_tags='register')
            return redirect('/')
        else:
            password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            register=User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], dob=request.POST['dob'],password=password_hash)
            messages.success(request,"Successfully registered!")
            return redirect('/success')

def login(request):
    if request.method=='POST':
        authSuccess=False
        errors=User.objects.login_validation(request.POST)
        if len(errors):
            request.session['loginemail']=request.POST['loginemail']
            for key,value in errors.items():
                messages.error(request,value,extra_tags='login')
            return redirect('/')
        else:
            user=User.objects.get(email=request.POST['loginemail'])
            request.session['user_id']=user.id
            request.session['first_name']=user.first_name
            messages.success(request,"Successfully logged in!")
            return redirect('/success')

def success(request):
    if 'user_id' in request.session:
        return render(request, 'login_registration/success.html')
    else:
        return redirect('/')