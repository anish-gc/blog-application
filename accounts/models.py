from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from accounts.manager import AccountManager
from utilities.models import BaseModel

# Create your models here.




class Account(AbstractBaseUser, BaseModel, PermissionsMixin):
    """
    Custom user account model that extends both AbstractBaseUser for authentication
    and BaseModel for common fields and behavior.
    """
    username = models.CharField(max_length=50,unique=True, blank=False, null=False,   help_text="Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.")
    
    address = models.CharField(max_length=255, blank=True, help_text="Address of the user (e.g., Tilottama-3, Yogikuti, Shantichowk, near futsal Brahmapath)")  
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = AccountManager()
    

    class Meta:
        db_table = "accounts"
        ordering = ['-created_at']
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        indexes = [
            models.Index(fields=['is_staff']), 
        ]
    def __str__(self):
        return self.username

  
  


    def user_designation(self):
        designation = 'staff'
        if self.is_superuser:
            designation = 'superUser'
        return designation    

