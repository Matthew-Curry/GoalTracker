'''Custom User model and manager'''

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

#redefine the user manager for a user model with no username
class UserManager(BaseUserManager):
    use_in_migrations = True

    #helper method to create user
    def _create_user(self, email, password, **extra_fields):
        #Create and save user with the given email and password
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    #the method to create regular user
    def create_user(self, email, password=None, **extra_fields):
        #create and save regular user with the given email and password
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    #method to create super user
    def create_superuser(self, email, password, **extra_fields):
        #create a super use with the given email and password
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        #verify has right credentials
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self._create_user(email, password, **extra_fields) 

#the custom user model, no user name instead email
class CustomUser(AbstractUser):
    #no username
    username = None
    #email field is unique
    email = models.EmailField(verbose_name = 'email address', unique = True)
    #the username field is email
    USERNAME_FIELD = 'email'
    #email is now automatically required as username
    REQUIRED_FIELDS = []
    #link the new manager to the model through 'objects'
    objects = UserManager()
