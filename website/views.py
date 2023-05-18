from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    #check to see if logging in
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In")
            return redirect('website:home')
        else:
            messages.success(request, "There was an error logging in, please try again.")
            return redirect('website:home')
    else:
        return render(request, 'website/home.html', {

    })

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('website:home')

def register_user(request):
    return render(request, 'website/register.html', {

    })