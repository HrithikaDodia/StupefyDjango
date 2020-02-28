from django.contrib.auth.models import BaseUserManager


class TwoFAUserManager(BaseUserManager):
    use_in_migrations = True

    # def _create_user(self, username, email, authy_id, password,
    #                  **extra_fields):
    #     if not username:
    #         raise ValueError('The given username must be set')
    #     email = self.normalize_email(email)
    #     username = self.model.normalize_username(username)
    #     user = self.model(username=username, email=email,
    #                       authy_id=authy_id, **extra_fields)
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    def create_user(self, username, email=None, phonenumber=None, password=None):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email,
                       phonenumber=phonenumber, is_staff=False, is_superuser=False)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phonenumber, password):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email,
                          phonenumber=phonenumber,is_staff=True, is_superuser=True, is_admin=True)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user