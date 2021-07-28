from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

Typecater = (
  ('LandScape', 'LandScape'),
  ('Portrait', 'Portrait')
)

Paymenttype = (
  ('M-pesa', 'M-pesa'),
  ('Bank', 'Bank')
)
Status = (
  ('inprogress','In-Progress'),
  ('futureselling','Future Selling'),
  ('sold', 'Sold')
)
BuyerCheck = (
  ('bought','bought'),
  ('interested','interested')
)

class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self): # go to profile
        return "/users/%i/" % (self.pk)
    def get_email(self):
        return self.email

class user_type(models.Model):
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_type_custom')

    def __str__(self):
        if self.is_buyer == True:
            return User.get_email(self.user) + " - is_buyer"
        else:
            return User.get_email(self.user) + " - is_seller"

class Art(models.Model):
  auctionimage = models.ImageField('Auction Image',upload_to='auctionimage/', null=False)
  title = models.CharField('Art Title',max_length=200)
  description = models.TextField('Art Inspiration')
  reservedPrice = models.IntegerField('Reserved Price (Ksh)',default=0) # this will be updated constantly
  buyingPrice = models.IntegerField('Buying Price (Ksh)', default=0)
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  typeCategory = models.CharField('Art Orienation', choices=Typecater, default='Portrait', null=True, max_length=50)
  startTime = models.DateTimeField('Auction StartTime', auto_now_add=False, auto_now=False, blank=True)
  EndTime =  models.DateTimeField('Auction EndTime', auto_now_add=False, auto_now=False, blank=True)
  createdTime =  models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
  status = models.CharField('Status', choices=Status, default='futureselling', null=True, max_length=50)

  def __str__(self):
    return f'{self.title} - Status - {self.status}'

  @classmethod
  def get_by_status(cls, reqUser, statusCode):
    allarts = cls.objects.filter(owner=reqUser)
    variousCodes = [arts for arts in allarts if arts.status == statusCode]
    return variousCodes

  @classmethod
  def get_all_by_status(cls, statusCode):
    return cls.objects.filter(status=statusCode)

  @classmethod
  def update_price(cls, id, price):
    cls.objects.filter(id=id).update(reservedPrice=price)

class Payment(models.Model):
  paymentType = models.CharField(max_length=200, choices=Paymenttype, default='M-pesa', null=True)
  accountNumber = models.IntegerField()

  def __str__(self):
    return self.paymentType

class Profile(models.Model):
  nickname = models.CharField(max_length=200, null=True, blank=True)
  username = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
  profilePic = models.ImageField(upload_to='userProfile/', default='userProfile/test.png')
  phone = models.IntegerField(null=True, blank=True)
  address = models.TextField()
  payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True)

  def __str__(self):
    return str(self.username)

  @receiver(post_save, sender=User)
  def create_user_profile(sender, instance, created, **kwargs):
    if created:
      Profile.objects.create(username=instance)

  @receiver(post_save, sender=User)
  def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# class Bid(models.Model):
#   art = models.ForeignKey(Art, on_delete=models.CASCADE)
#   buyer = models.ForeignKey(Profile, on_delete=models.CASCADE)
#   bidprice = models.IntegerField(default=0)

#   def __str__(self):
#     return f'{self.buyer} bidded on {self.art}'

class Interested(models.Model):
  art = models.ForeignKey(Art, on_delete=models.CASCADE)
  buyer = models.ForeignKey(Profile, on_delete=models.CASCADE)
  buyercheck = models.CharField(max_length=100, choices=BuyerCheck, null=True, blank=True)
  bidprice = models.IntegerField(default=0)


  def __str__(self):
    return f'{self.buyer} is Insterested in {self.art}'
