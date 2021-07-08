from .models import Account


class AccountAuth(object):

    def authenticate(self, username=None, password=None):
        try:
            user = Account.objects.get(email=username)
            if user.check_password(password):
                return user
        except Account.DoesNotExist:
            return None

    def get_user(self, id):
        try:
            user = Account.objects.get(pk=id)
            if user.is_active:
                return user
            return None
        except Account.DoesNotExist:
            return None