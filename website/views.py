from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

def home(request):
    records = Record.objects.all()
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
            'records': records
    })

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('website:home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered')
            return redirect('website:home')
    else:
        form = SignUpForm()
        return render(request, 'website/register.html', {
            'form': form
        })
    return render(request, 'website/register.html', {
            'form': form
        })


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        next_record = Record.objects.filter(pk__lt=customer_record.pk).order_by('-updated_at').first()
        return render(request, 'website/record.html', {
            'customer_record': customer_record,
            'next_record_pk': next_record.pk if next_record else None
        })
    else:
        messages.success(request, "You Must Be Logged In To View The Record")
        return redirect('website:home')
    

def delete_customer(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Records Deleted Successfully")
        return redirect('website:home')
    else:
        messages.success(request, "You Must Be Logged In To Do That")
        return redirect('website:home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Record Added")
                return redirect('website:home')
        return render(request, 'website/add_record.html', {
            'form': form
            })
    else:
        messages.success(request, "You Must Be Logged In To Do That")
        return redirect('website:home')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('website:home')
        return render(request, 'website/update_record.html', {
            'form': form
            })
    else:
        messages.success(request, "You Must Be Logged In To Do That")
        return redirect('website:home')