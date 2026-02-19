from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


from apps.master.auth.utils import login_required_jwt, logout_jwt, hash_password, verify_password, generate_token
from apps.master.utils.inputValidators import *

from apps.users.forms import *
from apps.users.models import *

# Create your views here.
@login_required_jwt
def index(request):
    users = User.objects.exclude(id=request.authenticated_user.id)

    messages = [
        {"sender": request.authenticated_user, "content": "Hey there 👋"},
        {"sender": users.first() if users else request.authenticated_user, "content": "Hello!"},
        {"sender": request.authenticated_user, "content": "This UI looks clean 😎"},
    ]

    return render(request, "chat.html", {
        "users": users,
        "chat_messages": messages
    })
    # return render(request,'index.html')

def login(request):
    if request.method=="POST":
        try:
            username_ = validateUsername(request.POST.get('username'))
            password = request.POST.get('password')

            getUser = User.objects.get(username=username_)

            if not verify_password(password, getUser.password):
                messages.error(request, "Incorrect Email or Password")
                return redirect('login')

            if getUser:
                getUser.save()
                token = generate_token(getUser)
                
                request.session['access_token'] = token
                return redirect('index')
            else:
                raise ValidationError("Incorrect Username or Password. Please Try Again.")

        except ValidationError as e:
            messages.error(request,message=e)
            return redirect('login')
        
    return render(request,'login.html')

def register(request):
    if request.method=="POST":
        try:
            username_ = validateUsername(request.POST.get('username'))
            if User.objects.filter(username=username_).exists():
                raise ValidationError('Username already Exists')
            email_ = is_valid_email(request.POST.get('email'))
            password_ = hash_password(validatePassword(match_password(request.POST['password'],request.POST['confirm_password'])))
            User.objects.create(username=username_,email=email_,password=password_)
            messages.success(request,"User Created")
            return redirect('login')
        except ValidationError as e:
            messages.error(request,message=e)
            return redirect('register')
        
    return render(request,'register.html')



def logout(request):
    messages.success(request,'Logged Out.')
    request.session.flush()
    return redirect('login')