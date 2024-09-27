from django.shortcuts import render

# Create your views here.
# Получаем модель, зарегистрированную в конфиге проекта,
# в константе AUTH_USER_MODEL
# User = get_user_model()

# И в коде применяем значение переменной User,
# которое вернула функция get_user_model():
# result = User.objects.all()