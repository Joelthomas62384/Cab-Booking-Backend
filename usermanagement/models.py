from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin , BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, mobile,  full_name, password=None, **kwargs):
        if not mobile:
            raise ValueError('Users must have a mobile number.')
       
        if not full_name:
            raise ValueError('Users must have a full name.')

        user = self.model(
            mobile=mobile,
            full_name=full_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, mobile,  full_name, password, **kwargs):
        user = self.create_user(
            mobile=mobile,
            full_name=full_name,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True , null=True)
    mobile = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = UserManager()
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = [ 'full_name']
    def __str__(self):
        return self.full_name
    
