# CBV import
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from django.urls import reverse_lazy

# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
from .forms import BirthdayForm
from .models import Birthday
# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown


# Добавляем миксин для тестирования пользователей, обращающихся к объекту.
class OnlyAuthorMixin(UserPassesTestMixin):

    # Определяем метод test_func() для миксина UserPassesTestMixin:
    def test_func(self):
        # Получаем текущий объект.
        object = self.get_object()
        # Метод вернёт True или False.
        # Если пользователь - автор объекта, то тест будет пройден.
        # Если нет, то будет вызвана ошибка 403.
        return object.author == self.request.user


class BirthdayListView(LoginRequiredMixin, ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 10


class BirthdayCreateView(LoginRequiredMixin, CreateView):
    model = Birthday
    form_class = BirthdayForm

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)


class BirthdayUpdateView(LoginRequiredMixin, OnlyAuthorMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayDeleteView(LoginRequiredMixin, OnlyAuthorMixin, DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(LoginRequiredMixin, OnlyAuthorMixin, DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        # Получим словарь с контекстом из родительского метода
        # get_context_data():
        context = super().get_context_data(**kwargs)
        # Дополним словарь новым ключом;
        # значением этого ключа будет вызов функции
        # calculate_birthday_countdown():
        context['birthday_countdown'] = calculate_birthday_countdown(
            # В качестве аргумента в функцию нужно передать дату рождения
            # начение поля birthday объекта модели.
            # Сам объект доступен в атрибуте self.object:
            self.object.birthday
        )
        # Возвращаем словарь контекста.
        return context
