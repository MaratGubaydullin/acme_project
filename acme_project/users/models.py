from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    bio = models.TextField('Биография', blank=True)





# Первым делом создаётся и регистрируется приложение users,
# а в нём описывается новый класс — кастомная модель пользователя;
# этот класс следует создать в самом начале работы над проектом,
# до того, как будут выполнены встроенные миграции.
# В новую модель пользователя сразу добавим поле bio.
