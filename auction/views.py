from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import user_type, User, Art, Payment, Profile
from .forms import RegistrationForm

def signup(request):
  if request.method == 'POST':
    regform = RegistrationForm(request.POST)
    if regform.is_valid():
      temail = request.POST.get('email')
      usertype = request.POST.get('usertype')
      regform.save()
      user = User.objects.get(email=temail)
      
      usert = None

      if usertype == 'student':
          usert = user_type(user=user,is_buyer=True)
      elif usertype == 'teacher':
          usert = user_type(user=user,is_seller=True)
            
      usert.save()
      return redirect('loginpage')
  
  form = RegistrationForm()
  params = {
    'form' : form
  }
  return render(request, 'registration/register.html', params)
    
def auth_login(request):
    if request.method == 'POST':
        email = request.POST.get('email') #Get email value from form
        password = request.POST.get('password') #Get password value from form
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            type_obj = user_type.objects.get(user=user)
            if user.is_authenticated and type_obj.is_buyer:
                return redirect('buyerindex') #Go to buyer home
            elif user.is_authenticated and type_obj.is_seller:
                return redirect('sellerindex') #Go to seller home
        else:
          # flash message username is incorrect
          return redirect('loginpage')
    return render(request, 'registration/login.html')

def logout_user(request):
  logout(request)
  return redirect('loginpage')

@login_required(login_url='loginpage')
def index(request): # landing page normal
  return render(request, 'index.html')

def sellerindex(request):
  return render(request, 'seller/index.html')

def buyerindex(request):
  return render(request, 'buyer/index.html')