# CBV import
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView)

from django.urls import reverse_lazy

# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
from .forms import BirthdayForm
from .models import Birthday
# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown


class BirthdayListView(ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 10


class BirthdayCreateView(CreateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayUpdateView(UpdateView):
    model = Birthday
    form_class = BirthdayForm


class BirthdayDeleteView(DeleteView):
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(DetailView):
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
