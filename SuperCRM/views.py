from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout


def acc_signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/crm')
        else:
            return render(request, 'index.html', {'error': "Invalid username or password"})
    else:
        return render(request, 'signin.html')


def acc_logout(request):
    logout(request)
    return redirect('/')
