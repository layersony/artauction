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

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    def get_email(self):
        return self.email

class user_type(models.Model):
    is_teach = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        if self.is_student == True:
            return User.get_email(self.user) + " - is_student"
        else:
            return User.get_email(self.user) + " - is_teacher"

class Art(models.Model):
  auctionimage = models.ImageField(upload_to='auctionimage/', null=False)
  title = models.CharField(max_length=200)
  description = models.TextField()
  reservedPrice = models.IntegerField(default=0)
  buyingPrice = models.IntegerField(default=0)
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  typeCategory = models.CharField(choices=Typecater, default='Portrait', null=True, max_length=50)
  startTime = models.DateTimeField()
  EndTime = models.DateTimeField()
  createdTime = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title

class Payment(models.Model):
  paymentType = models.CharField(max_length=200, choices=Paymenttype, default='M-pesa', null=True)
  accountNumber = models.IntegerField()

  def __str__(self):
    return self.paymentType

class Profile(models.Model):
  username = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
  profilePic = models.ImageField(upload_to='userProfile/', default='userProfile/test.png')
  phone = models.IntegerField(null=True, blank=True)
  address = models.TextField()
  payment = models.ForeignKey(Payment, on_delete=models.CASCADE())

  def __str__(self):
    return self.username

  @receiver(post_save, sender=User)
  def create_user_profile(sender, instance, created, **kwargs):
    if created:
      Profile.objects.create(username=instance)

  @receiver(post_save, sender=User)
  def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()