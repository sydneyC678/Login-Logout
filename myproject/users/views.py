from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def home(request):
    return render(request, 'users/index.html')
def post(request):
    return render(request, 'users/post.html')
def signup(request):
    if request.method == "POST":
        #username = request.POST.get('username')
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username = username):
            messages.error(request, "Username already exists! Please enter a different one!")
            return redirect('home')
        if User.objects.filter(email = email):
            messages.error(request, "Email already associated with an account!")
            return redirect('home')
        if len(username)>10:
            messages.error(request,"Username must be under 10 characters!")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "Passwords do not match, please enter both again!")
        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname

        myuser.save()
        #messages.success(request, "Welcome to SheSpeaksTwenties!")

        #redirect user to the login page
        return redirect('signin')


    return render(request, 'users/signup.html')

def signin(request): 
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        #authenticate the user
        user = authenticate(username=username, password = pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, 'users/index.html', {'fname': fname})
        else:
            messages.error(request, "Add proper credentials")
            return redirect('home')




    return render(request, 'users/signin.html')

def signout(request):
    logout(request)
    messages.success(request,'Logged out successfully')
    return redirect('home')

#Date since membership started
def get_signup_date(username):
    try:
        user = User.objects.get(username=username)
        signup_date = user.date_joined
        return signup_date
    except User.DoesNotExist:
        return None
        
def profile(request):
    user = request.user
    signup_date = get_signup_date(user.username)
    return render(request, 'users/profile.html', {'user': user, 'signup_date': signup_date})


