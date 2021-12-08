from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from .models import User
from django.contrib import messages

def login_reg(request):
    return render(request, 'login_reg.html')

def register(request):
    errors = User.objects.reg_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        return redirect('/')

    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        User.objects.create(first_name = first_name, last_name = last_name, email = email, pw_hash = pw_hash)

        return redirect('/')

def login(request):
    user = User.objects.filter(email = request.POST['login_email'])

    if user:
        logged_user = user[0]

        if bcrypt.checkpw(request.POST['login_pw'].encode(), logged_user.pw_hash.encode()):
            request.session['user_id'] = logged_user.id

            return redirect('/groups')

    return redirect('/')

# def success(request):
#     if 'user_id' not in request.session:
#         return redirect('/')

#     user_pull = User.objects.filter(id = request.session['user_id'])
#     user = user_pull[0]

#     context = {
#         'user': user
#     }

#     return render(request, 'success.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')