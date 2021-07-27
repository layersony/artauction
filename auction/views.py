from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import user_type, User, Art, Payment, Profile
from .forms import RegistrationForm, ArtAddForm, UserForm, ProfileForm
from django.contrib import messages


def signup(request):
  if request.method == 'POST':
    regform = RegistrationForm(request.POST)
    if regform.is_valid():
      temail = request.POST.get('email')
      usertype = request.POST.get('usertype')
      regform.save()
      user = User.objects.get(email=temail)
      
      usert = None

      if usertype == 'buyer':
          usert = user_type(user=user,is_buyer=True)
      elif usertype == 'seller':
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
                return redirect('buyerProfile') #Go to buyer home
            elif user.is_authenticated and type_obj.is_seller:
                return redirect('sellerProfile') #Go to seller home
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

def sellerProfile(request):
  if request.method == 'POST':
    userform = UserForm(request.POST or None, instance=request.user)
    profileform = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
    artaddform = ArtAddForm(request.POST, request.FILES)

    if userform.is_valid() and profileform.is_valid():
      userform.save()
      profileform.save()
      messages.success(request, 'Profile updated successfully')

    if artaddform.is_valid():
      artsave = artaddform.save(commit=False)
      artsave.owner = request.user
      artsave.save()

    return redirect('sellerProfile')

  curr_profile = Profile.objects.get(username = request.user)
  artaddform = ArtAddForm()
  userform = UserForm(instance=request.user)
  profileform = ProfileForm(instance=request.user.profile)
  inprogress = Art.get_by_status(request.user, 'inprogress')
  future = Art.get_by_status(request.user, 'futureselling')
  sold = Art.get_by_status(request.user, 'sold')

  params = {
    'curr_profile':curr_profile,
    'artaddform':artaddform,
    'userform': userform,
    'profileform': profileform,
    'inprogress':inprogress,
    'future':future,
    'sold':sold
  }
  return render(request, 'seller/index.html', params)

def buyerProfile(request):
  return render(request, 'buyer/index.html')
