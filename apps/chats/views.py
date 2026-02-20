from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q


from apps.master.auth.utils import login_required_jwt, logout_jwt, hash_password, verify_password, generate_token
from apps.master.utils.inputValidators import *

from apps.users.forms import *
from apps.users.models import *

# Create your views here.
@login_required_jwt
def index(request):
    return redirect('chats')

@login_required_jwt
def chats(request,user_id=None):
    current_user = request.authenticated_user
    form = SendMessageForm()

    # Sidebar conversations
    conversations = Conversation.objects.filter(
        Q(user1=current_user) | Q(user2=current_user)
    ).select_related('user1', 'user2')

    # print(conversations[0].user1.username,conversations[0].user2.username)

    # Determine selected chat user
    selected_user = None
    messages = []
    conversation = None

    if user_id:
        selected_user = get_object_or_404(User, id=user_id)
        conversation = get_or_create_conversation(current_user, selected_user)
        receiver = get_object_or_404(User, id=user_id)

        messages = Message.objects.filter(
            conversation=conversation
        ).select_related('sender').order_by('created_at')

    if request.method == "POST":
        form = SendMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.authenticated_user
            message.receiver = receiver
            message.conversation = conversation
            message.save()
            context={'msg':message}
            return render(request,'partials/chat-pills-p.html',context)

    context = {
        "conversations": conversations,
        "selected_user": selected_user,
        "chat_messages": messages,
        "form":form
    }
    return render(request, "chat.html", context)

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