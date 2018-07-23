from django.shortcuts import render,HttpResponse, redirect
from django.contrib import messages
from .models import *


# Create your views here.
def index(request):
    if not request.session.keys():
        request.session['first_name']=""
        request.session['last_name']=""
        request.session['email']=""
        request.session['loginemail']=""
    if 'user_id' in request.session:
        return redirect('/quotes')
    else:
        return render(request,'login_registration/index.html')

def register(request):
    if request.method=='POST':
        errors=User.objects.user_validation(request.POST,'register')
        if len(errors):
            request.session['first_name']=request.POST['first_name']
            request.session['last_name']=request.POST['last_name']
            request.session['email']=request.POST['email']
            for key,value in errors.items():
                messages.error(request,value,extra_tags='register')
            return redirect('/')
        else:
            password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            register=User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'],password=password_hash)
            request.session['user_id']=register.id
            request.session['first_name']=register.first_name
            messages.success(request,"Successfully registered!")
            return redirect('/quotes')

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
            return redirect('/quotes')

def quotes(request):
    if 'user_id' in request.session:
        context={
            "quotes":Quote.objects.all()
        }
        return render(request, 'login_registration/quotes.html',context)
    else:
        return redirect('/')

def addQuote(request):
    if request.method=='POST':
        if 'user_id' in request.session:
            errors=Quote.objects.quote_validation(request.POST)
            if len(errors):
                for key,value in errors.items():
                    messages.error(request,value,extra_tags='quote')
                request.session['author'] = request.POST['author']
                request.session['quote'] = request.POST['quote']
            else:
                newQuote=Quote.objects.create(quote=request.POST['quote'],author=request.POST['author'],posted_by=User.objects.get(id=request.session['user_id']))
                if 'author' in request.session:  
                    del request.session['author']
                if 'quote' in request.session:  
                    del request.session['quote']
            return redirect('/quotes')
        else:
            return redirect('/')     

def likeQuote(request,id):
    if 'user_id' in request.session:
        quote=Quote.objects.get(id=id)
        likeQuote=quote.likes.add(User.objects.get(id=request.session['user_id']))
        return redirect('/quotes')
    else:
        return redirect('/')   

def myAccount(request,id):
    if 'user_id' in request.session:
        context={
            "user":User.objects.get(id=id)
        }
        return render(request,'login_registration/myaccount.html',context)
    else:
        return redirect('/')  

def displayUser(request,id):
    if 'user_id' in request.session:
        context={
            "user":User.objects.get(id=id)
        }
        return render(request,'login_registration/userquotes.html',context)
    else:
        return redirect('/')  

def deleteQuote(request,id):
    if 'user_id' in request.session:
        quote=Quote.objects.get(id=id)
        if quote.posted_by.id == request.session['user_id']:
            quote.delete()
            return redirect('/quotes')
        else:
            return HttpResponse("Permission denied!")
    else:
        return redirect('/')  

def updateUser(request,id):
    if request.method=='POST':
        errors=User.objects.user_validation(request.POST)
        user=User.objects.get(id=id)
        if user.email == request.POST['email']:
            del errors['emailexist']
        if 'user_id' in request.session:
            if len(errors):
                for key,value in errors.items():
                    messages.error(request,value)
            else:
                if user.id == request.session['user_id']:
                    user.first_name=request.POST['first_name']
                    user.last_name=request.POST['last_name']
                    user.email=request.POST['email']
                    user.save()
                    request.session['first_name']=user.first_name
                    messages.success(request, "Account updated!")
                else:
                    return HttpResponse("Permission denied!")
            return redirect('/myaccount/'+id)
        else:
            return redirect('/')  


def logout(request):
    request.session.clear()
    return redirect('/')