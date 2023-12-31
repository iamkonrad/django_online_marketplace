from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django_countries.fields import CountryField




class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username,email, password=None):
        if not email:
            raise ValueError('Please add email address!!!')

        if not username:
            raise ValueError('Please input your username')

        user = self.model(
            email=self.normalize_email(email),                                                                          #upper to lower case if needed
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username,email, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)


    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_superadmin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self,perm,ob=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True

    def get_role(self):
        user_role = None
        if self.role == 1:
            user_role = 'Vendor'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)
    profile_picture = models.ImageField(upload_to='media/users/profile_pictures',blank=True,null=True)
    cover_photo = models.ImageField(upload_to='media/users/cover_photos',blank=True,null=True)
    country= CountryField(blank_label='(select a country)')
    province = models.CharField(max_length=150,blank=True,null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    address_line_1 = models.CharField(max_length=150,blank=True,null=True)
    address_line_2 = models.CharField(max_length=150,blank=True,null=True)
    postcode = models.CharField(max_length=50,blank=True,null=True)
    longitude = models.CharField(max_length=30,blank=True,null=True)
    latitude = models.CharField(max_length=30,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def full_address(self):
        return f'{self.country}, {self.province},{self.address_line_1},{self.postcode}'
    def __str__(self):
        return self.user.email
