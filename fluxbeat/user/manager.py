from django.contrib.auth.base_user import BaseUserManager

class userManager(BaseUserManager):

    def create_user(self, email, password=None, **ext_fields):
        if not email:
            raise ValueError("Phone Number is required!")

        email=self.normalize_email(email)
        user = self.model(email=email, **ext_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **ext_fields):
        ext_fields.setdefault('is_staff', True)
        ext_fields.setdefault('is_superuser', True)
        ext_fields.setdefault('is_active', True)

        return self.create_user(email, password, **ext_fields)
