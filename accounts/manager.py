from django.contrib.auth.models import  BaseUserManager


class AccountManager(BaseUserManager):
    """Custom manager for Account model."""
    
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username must be provided")
      
        user = self.model(username=username,  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
  

        return self.create_user(username, password, **extra_fields)

