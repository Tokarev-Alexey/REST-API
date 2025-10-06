from rest_framework.authtoken.models import Token


def create_token(oblect):
    Token.objects.create(user=oblect)