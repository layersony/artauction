from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import BuyerCheck, Interested, user_type, User, Art, Payment, Profile
from .forms import RegistrationForm, ArtAddForm, UserForm, ProfileForm
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
import pytz
timebamako = pytz.timezone('Africa/Bamako')
datetime_bamako = datetime.now(timebamako)


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

  for i in future:
    starting = i.startTime.timestamp()
    nowtime = datetime_bamako.timestamp()

    startingin = starting - nowtime
    if startingin < 0:
      Art.objects.filter(id=i.id).update(status='inprogress')

    else:
      print('bado')
  

  params = {
    'inprogress':inprogress,
    'future':future,
    'sold':sold
  }
  return render(request, 'index.html', params)

def artdetails(request, id):
  art = Art.objects.get(id=id)
  curr_pro = Profile.objects.get(username=request.user)
  winner = None

  try:
    if Interested.objects.get(art=art, buyercheck='bought'):
      winner = Interested.objects.get(art=art, buyercheck='bought') 
  except Interested.DoesNotExist:
    winner = None

  likedArt = False

  if Interested.objects.filter(art=art, buyer=curr_pro):
    likedArt = True

  params = {
    'art':art,
    'likedArt':likedArt,
    'winner':winner
  }
  return render(request, 'artdetails.html', params)

@login_required(login_url='loginpage')
def sellerProfile(request):
  type_obj = user_type.objects.get(user=request.user)
  if request.user.is_authenticated and type_obj.is_buyer:
    return redirect('buyerProfile')
  else:
    if request.method == 'POST':
      userform = UserForm(request.POST or None, instance=request.user)
      profileform = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
      if userform.is_valid() and profileform.is_valid():
        userform.save()
        profileform.save()
        messages.success(request, 'Profile updated successfully')
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

def addart(request):
  if request.method == 'POST':
    artaddform = ArtAddForm(request.POST, request.FILES)
    if artaddform.is_valid():
      print('nimekua valid hapa seller')
      artsave = artaddform.save(commit=False)
      artsave.owner = request.user
      artsave.save()
      return redirect('sellerProfile')

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

def biddingArea(request, id):
  art = Art.objects.get(id=id)
  inputlen = len(str(art.reservedPrice))

  participants = Interested.objects.filter(art=art)
  # allparticipants = []

  # for bidder in participants:
  #   allparticipants.append([bidder.buyer.nickname, bidder.bidprice])
  params = {
    'art':art,
    'inputlen':inputlen,
    'allparticipants':participants

  }
  return render(request, 'bidding.html', params)

def ajaxbidprice(request):
  price = request.POST.get('biddingPrice')
  artid = request.POST.get('artid')

  Art.update_price(artid, price)

  art = Art.objects.get(pk=artid)
  curr_pro = Profile.objects.get(username=request.user)
  print(art)
  if Interested.objects.filter(art=art, buyer=curr_pro).first():
    Interested.objects.filter(art=art, buyer=curr_pro).update(bidprice=price)
  else:
    Interested.objects.create(art=art, buyer=curr_pro, bidprice=price)

  participants = Interested.objects.filter(art=art)
  allparticipants = []
  
  for bidder in participants:
    allparticipants.append([bidder.buyer.nickname, bidder.bidprice])


  data = {
    'price':price,
    'artid':artid,
    'allparticipants':allparticipants
  }
  return JsonResponse(data)

def buyerProfile(request):
  type_obj = user_type.objects.get(user=request.user)
  if request.user.is_authenticated and type_obj.is_seller:
    return redirect('sellerProfile')
  else:
    if request.method == 'POST':
      userform = UserForm(request.POST or None, instance=request.user)
      profileform = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
      if userform.is_valid() and profileform.is_valid():
        userform.save()
        profileform.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('buyerProfile')


    curr_profile = Profile.objects.get(username = request.user)
    userform = UserForm(instance=request.user)
    profileform = ProfileForm(instance=request.user.profile)
    inprogress = Art.get_all_by_status('inprogress')
    likedimages = Interested.objects.filter(buyer=curr_profile)
    bought = Interested.objects.filter(buyer=curr_profile, buyercheck='bought')

    params = {
      'curr_profile':curr_profile,
      'userform': userform,
      'profileform': profileform,
      'inprogress':inprogress,
      'likedimages':likedimages,
      'bought':bought
    }
    return render(request, 'buyer/index.html', params)

def interested(request):
  buyerview = request.POST.get('interested')
  artid = request.POST.get('artid')

  art = Art.objects.get(id=artid)
  curr_pro = Profile.objects.get(username=request.user)
  addedsuccessful = None

  if Interested.objects.filter(art=art, buyer=curr_pro):
    Interested.objects.filter(art=art, buyer=curr_pro).delete()
    print('deleted')
    addedsuccessful = 0
  else:
    Interested.objects.create(art=art, buyer=curr_pro, buyercheck=buyerview)
    print('saved')
    addedsuccessful = 1

  
  data = {
    'success': 'Added to your Interest Collection',
    'addedsuccessful':addedsuccessful
  }
  return JsonResponse(data)

def auctionWin(request):
  artid = request.POST.get('artid')
  wonprice = request.POST.get('wonprice')

  try:
    is_sold = False
    is_bought = False

    thisArt = Art.objects.get(id=artid)
    winner = Interested.objects.get(art=thisArt, bidprice = wonprice)
    
    if winner.buyercheck == 'bought':
      print('Already Bought')
      is_bought = True
    else:
      Interested.objects.filter(art=thisArt, bidprice = wonprice).update(buyercheck='bought')
      print('Updated to Bought')
      is_bought = True

    if thisArt.status == 'sold':
      is_sold = True
      print('Already Sold')
    else:
      Art.objects.filter(id=artid).update(status='sold')
      print('Updated to Sold')
      is_sold = True

    data = {
      'is_sold':is_sold,
      'is_bought':is_bought
    }
    return JsonResponse(data)
  except Interested.DoesNotExist:
    Art.objects.filter(id=artid).update(status='nobidders')
    data = {
      'nobiddiers':'Sorry No Bidders for this Art'
    }
    return JsonResponse(data)