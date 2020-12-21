from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, UserManager


# ________________________Render Routes ___________________________
def index(request):
    return render(request, 'index.html')


def success(request):
    if "user_id" in request.session:
        new_user = User.objects.get(id=request.session["user_id"])
        context = {
            'user': new_user
        }
        return render(request, "success.html", context)
    else:
        return redirect('/')


# __________________________Action Routes___________________________
def register(request):
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).decode()  # create

        user = User()
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.password_hash = pw_hash
        user.save()
        request.session['user_id'] = User.objects.last().id
        return redirect("/success")


def login(request):
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')
        request.session['user_id'] = User.objects.last().id
    return redirect('/success')


# MAKE SURE to clear the seesion or "/success" will fail and anyone can enter the Dashboard
def logout(request):
    del request.session['user_id']
    return redirect('/')
