from django.db import models
from django.contrib.auth import models as auth_models


class UserManager(auth_models.UserManager):
    def by_phone(self, phone_number):
        return self.filter(phone_number=phone_number).first()
        # return self.get(phone_number=phone_number)

    def first_name_count(self, first_name):
        return self.filter(first_name=first_name).count()


class RefreshTokenModelManager(models.Manager):
    def by_user(self, user):
        return self.filter(user=user, is_valid=True).first()
        # return self.get(user=user, is_valid=True)

    def by_refresh(self, token):
        return self.select_related('user').filter(token=token, is_valid=True).first()
        # return self.get(user=user, token=token, is_valid=True)



class VerifyOTPManager(models.Manager):
    def by_code(self, code):
        return self.filter(code=code, is_used=False).first()

# .filter() - результатов много, queryset
# .get()    - результат один, None или more вызывают ошибки DoesNotExist и MultipleObjectsReturned соответственно

# .filter(phone_number__iexact=phone_number)    # Регистро-независимое сравнение:   WHERE LOWER(phone_number) = LOWER('+998901234567')
# .filter(phone_number=phone_number)            # Регистро-зависимое сравнение:     WHERE phone_number = '+998901234567'




