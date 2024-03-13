from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, phone_number=None, full_name=None, password=None, is_active=True, is_staff=False, is_superuser=False):
        if not email:
            raise ValueError('Users must have an email address!')
        if not password:
            raise ValueError('Users must have a password!')
        user_obj = self.model(email=self.normalize_email(email), phone_number=phone_number)
        user_obj.set_password(password)
        user_obj.full_name = full_name
        user_obj.is_active = is_active
        user_obj.is_staff = is_staff
        user_obj.is_superuser = is_superuser
        user_obj.save(using=self._db)
        return user_obj
    
    def create_superuser(self, email, phone_number=None, full_name=None, password=None):
        user = self.create_user(
            email=email,
            phone_number=phone_number,
            full_name=full_name,
            password=password,
            is_superuser=True,
            is_staff=True,
        )
        return user
    
    def create_staffuser(self, email, phone_number=None, full_name=None, password=None):
        user = self.create_user(
            email=email,
            phone_number=phone_number,
            full_name=full_name,
            password=password,
            is_staff=True,
        )
        return user