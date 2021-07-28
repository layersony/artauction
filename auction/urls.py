from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
  path('', views.index, name='home'),
  path('accounts/register/', views.signup, name='registrationpage'),
  path('accounts/login/', views.auth_login, name='loginpage'),
  path('logout/', views.logout_user, name='logout'),
  path('buyer/index', views.buyerProfile, name='buyerProfile'),
  path('seller/index', views.sellerProfile, name='sellerProfile'),
  path('seller/addart/', views.addart, name='addart'),
  path('seller/updateart/<str:id>', views.updateArt, name='updateArt'),
  path('seller/delete/<str:id>', views.deleteArt, name='deleteArt'),
  path('artdetails/<str:id>', views.artdetails, name='artdetails'),
  path('bidding/<str:id>', views.biddingArea, name='bidding'),
  path('ajax/biddingprice/', views.ajaxbidprice, name='ajaxbidprice'),
  path('ajax/interested/', views.interested, name='interested'),
  path('ajax/auctionWin/', views.auctionWin, name='auctionWin'),
  path('buyer/checkout/<str:id>', views.checkout, name='checkout')
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  