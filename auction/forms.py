from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, user_type

class RegistrationForm(UserCreationForm):
  typeuser = (
    ('---', '---'),
    ('buyer', 'Buyer'),
    ('seller', 'Seller')
  )
  usertype = forms.ChoiceField(choices=typeuser, required=True)
  class Meta:
    model = User
    fields = ['email', 'usertype', 'password1', 'password2']  