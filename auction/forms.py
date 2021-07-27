from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, user_type, Art, Profile

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

class ArtAddForm(forms.ModelForm):
  class Meta:
    model = Art
    fields = '__all__'
    exclude = ['owner', 'createdTime']

class UserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ('email',)

class ProfileForm(forms.ModelForm):
    class Meta:
      model = Profile
      fields = '__all__'
      exclude = ['username',]
      