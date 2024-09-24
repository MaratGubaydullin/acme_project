from django.shortcuts import get_object_or_404, redirect, render


# Импортируем класс BirthdayForm, чтобы создать экземпляр формы.
from .forms import BirthdayForm
from .models import Birthday
# Импортируем из utils.py функцию для подсчёта дней.
from .utils import calculate_birthday_countdown


def birthday(request, pk=None):
    # Если в запросе указан pk (если получен запрос на редактирование объекта):
    if pk is not None:
        # Получаем объект модели или выбрасываем 404 ошибку.
        instance = get_object_or_404(Birthday, pk=pk)
    # Если в запросе не указан pk
    # (если получен запрос к странице создания записи):
    else:
        # Связывать форму с объектом не нужно, установим значение None.
        instance = None
    # Передаём в форму либо данные из запроса, либо None.
    # В случае редактирования прикрепляем объект модели.
    form = BirthdayForm(
        request.POST or None,
        files=request.FILES or None,
        instance=instance
    )
    # Создаём словарь контекста сразу после инициализации формы.
    context = {'form': form}
    # Если форма валидна...
    if form.is_valid():
        # ...вызовем функцию подсчёта дней:
        form.save()  # сохранить данные из формы в БД
        birthday_countdown = calculate_birthday_countdown(
            # ...и передаём в неё дату из словаря cleaned_data.
            form.cleaned_data['birthday']
        )
        # Обновляем словарь контекста: добавляем в него новый элемент.
        context.update({'birthday_countdown': birthday_countdown})
    return render(request, 'birthday/birthday.html', context)


def delete_birthday(request, pk):
    # Получаем объект модели или выбрасываем 404 ошибку.
    instance = get_object_or_404(Birthday, pk=pk)
    # В форму передаём только объект модели;
    # передавать в форму параметры запроса не нужно.
    form = BirthdayForm(instance=instance)
    context = {'form': form}
    # Если был получен POST-запрос...
    if request.method == 'POST':
        # ...удаляем объект:
        instance.delete()
        # ...и переадресовываем пользователя на страницу со списком записей.
        return redirect('birthday:list')
    # Если был получен GET-запрос — отображаем форму.
    return render(request, 'birthday/birthday.html', context)


def birthday_list(request):
    # Получаем все объекты модели Birthday из БД.
    birthdays = Birthday.objects.all()
    # Передаём их в контекст шаблона.
    context = {'birthdays': birthdays}
    return render(request, 'birthday/birthday_list.html', context)


# ПОДРОБНЕЕ
# def birthday(request):
#     # Если есть параметры GET-запроса...
#     if request.GET:
#         # ...передаём параметры запроса в конструктор класса формы.
#         form = BirthdayForm()  # Создаём экземпляр класса формы.
#         # Если данные валидны...
#         if form.is_valid():
#             # ...то считаем, сколько дней осталось до дня рождения.
#             # Пока функции для подсчёта дней нет — поставим pass:
#             pass
#     # Если нет параметров GET-запроса.
#     else:
#         # То просто создаём пустую форму.
#         form = BirthdayForm()
#     # Передаём форму в словарь контекста с ключем form:
#     context = {'form': form}
#     # Указываем нужный шаблон и передаём в него словарь контекста.
#     return render(request, 'birthday/birthday.html', context)
