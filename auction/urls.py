from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='home'),
  path('accounts/register/', views.signup, name='registrationpage'),
  path('accounts/login/', views.auth_login, name='loginpage'),
  path('logout/', views.logout_user, name='logout'),
  path('buyer/index', views.buyerindex, name='buyerindex'),
  path('seller/index', views.sellerindex, name='sellerindex')
]