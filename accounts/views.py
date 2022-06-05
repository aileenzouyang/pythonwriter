from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth

# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return render(request,'upload.html')
        else:
            message = "incorrect login information."
            return render(request,'login.html', {'message':message})
    else: 
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect("/")

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            message = "User already exists, please try a different username"
            return render(request,'register.html', {'message':message})
        elif (password1 != password2):
            message = "password not matching"
            return render(request,'register.html', {'message':message})
        elif User.objects.filter(email=email).exists():
            message = "the email is taken"
            return render(request,'register.html', {'message':message})
        else:
            user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
            user.save()
            print("user created")
            return render(request,'upload.html')
            
    else:
        return render(request,'register.html')