from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import user_type, User, Art, Payment, Profile
from .forms import RegistrationForm, ArtAddForm, UserForm, ProfileForm
from django.contrib import messages
from django.http import JsonResponse


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
  inprogress = Art.get_all_by_status('inprogress')
  future = Art.get_all_by_status('futureselling')
  sold = Art.get_all_by_status('sold')

  params = {
    'inprogress':inprogress,
    'future':future,
    'sold':sold
  }
  return render(request, 'index.html', params)

def artdetails(request, id):
  art = Art.objects.get(id=id)
  params = {
    'art':art
  }
  return render(request, 'artdetails.html', params)

@login_required(login_url='loginpage')
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

@login_required(login_url='loginpage')
def updateArt(request, id):
  art = Art.objects.get(id=id)
  if request.method == 'POST':
    artaddform = ArtAddForm(request.POST, request.FILES, instance=art)
    if artaddform.is_valid():
      artaddform.save()
      print('saved')
      return redirect('sellerProfile')

  artaddform = ArtAddForm(instance=art)

  params = {
    'artaddform':artaddform,
    'art':art
  }
  return render(request, 'seller/artupdate.html', params)

def deleteArt(request, id):
  art = Art.objects.get(id=id)
  if request.method == 'POST':
    art.delete()
    return redirect('sellerProfile')

  return render(request, 'seller/delete')

def buyerProfile(request):
  return render(request, 'buyer/index.html')

def biddingArea(request, id):
  art = Art.objects.get(id=id)
  inputlen = len(str(art.reservedPrice))
  params = {
    'art':art,
    'inputlen':inputlen
  }
  return render(request, 'bidding.html', params)

def ajaxbidprice(request):
  price = request.POST.get('biddingPrice')
  artid = request.POST.get('artid')

  Art.update_price(artid, price)

  data = {
    'price':price,
    'artid':artid
  }
  return JsonResponse(data)