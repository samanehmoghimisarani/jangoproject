from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self,  username, name, family, email, phone, password):
        if not username:
            raise ValueError('User Must Have Fullname !')

        user = self.model(email=self.normalize_email(email), username=username, phone=phone, name=name, family=family)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,  username, name, family, email, phone, password):
        user = self.create_user(username, name, family, email, phone, password)
        user.is_admin = True
        user.is_assistant = True
        user.save(using=self._db)
        return user

    def create_assistant_user(self,  username, name, family, email, phone, password):
        user = self.create_user(username, name, family, email, phone, password)
        user.is_assistant = True
        user.save_base(using=self._db)
        return user

