from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

# Here BaseUsermanager means we customized or extends our default User Model In this class we create a user and give permission for access..
class MyAccountManager(BaseUserManager):
    # This function is for normal user.
    def create_user(self, first_name, last_name, username, email, password=None):   # Here we create a user .And we have to pass all Uername_field and required_fiels and use this default function name ..
        if not email:                                                               
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')
        
        user = self.model(
            email = self.normalize_email(email),             # normalize_email() means when we enter email then it convert or normalize in small letters.
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user
    

    # This function is for Admin user.
    def create_superuser(self, first_name, last_name, email, username, password):   # Here we assign the permission to the user.
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name, 
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)                 # Here we define the customized field we want it.
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50)

    #required
    date_joined     = models.DateTimeField(auto_now_add=True)     # Here is some necessary field weneed to define.
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)         
    is_staff        = models.BooleanField(default=False)          # Returns True if the user is allowed to have access to the admin site.
    is_active       = models.BooleanField(default=False)          # Returns True if the user account is currently active.
    is_superadmin   = models.BooleanField(default=False)

    USERNAME_FIELD  = 'email'                                     # Here we define that we want to login the user with the email.
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']     # A list of field names will be prompted fro when ceating a user.

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):                                     # Returns True if the user has the named permission. If obj is provided, 
        # "Does the user have permissions to view the app `app_label`?"     # the permission needs to be checked against a specific object instance.
        # Simplest possible answer: Yes, always                             
        return self.is_admin                                                
    
    def has_module_perms(self, add_label):                                  # Returns True if the user has permission to access models in the given app.
        # "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff               
        return True
    

                              # This is all presnt in documentation when we need to customize our dajngo auhentication becoz
                              # it provide only username and password field only but we need to secure more and we want that our user 
                              # login with email .
                              # After defining here register in settings.py file under WSGI_Application 'app_name.Model_name
                              # and register in admin.py file also.