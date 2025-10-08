from users.models import ProfileUser
from rest_framework import serializers

class ProfileUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = ProfileUser
        fields = ['id', 'username', 'password', 'email', 'avatar']

    def create(self, validated_data):
        password = validated_data.pop('password')  #Достаем пароль
        user = ProfileUser.objects.create(**validated_data)  #Создаем без пароля
        user.set_password(password)  #Хэшируем и устанавливаем пароль
        user.save()  #Сохраняем
        return user

