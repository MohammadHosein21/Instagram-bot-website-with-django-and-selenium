from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(email=request.POST['email'])
                return render(request, 'accounts/templates/signup.html',
                              {'error': 'Email Has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'],
                                                password=request.POST['password1'])
                auth.login(request, user)
                return redirect('login')
        else:
            return render(request, 'accounts/templates/signup.html', {'error': 'Password must match'})
    else:
        return render(request, 'accounts/templates/signup.html')


def login(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            username = User.objects.get(email=email.lower()).username
            user = auth.authenticate(username=username, password=request.POST['password'])
            if user is not None:
                auth.login(request, user)
                return redirect('signup')
            else:
                return render(request, 'accounts/templates/login.html', {'error': 'Email or Password is incorrect.'})
        except User.DoesNotExist:
            return render(request, 'accounts/templates/login.html', {'error': 'Email or Password is incorrect.'})
    else:
        return render(request, 'accounts/templates/login.html')
