from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import ContactForm
import telegram
# reflex002@bk.ru
def mainpage(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Отправка email
            send_mail(
                f'Новая заявка от {name}',
                f'Почта: {email}\nСообщение: {message}',
                'reflex002@bk.ru',  # Замените на ваш email
                ['reflex002@bk.ru'],  # Замените на email получателя
                fail_silently=False,
            )

            return redirect('mainpage')
    else:
        form = ContactForm()

    return render(request, 'main/mainpage.html', {'form': form})


# def mainpage(request):
#     return render(request,'main/mainpage.html', {'title': 'Главная'})

def statistics(request):
    return render(request,'main/statistics.html', {'title': 'Статистика боёв'})
def polygons(request):
    return render(request,'main/polygons.html', {'title': 'Полигоны'})
def scenarios(request):
    return render(request,'main/scenarios.html', {'title': 'Сценарии'})
def cabinet(request):
    return render(request,'main/cabinet.html', {'title': 'Личный кабинет'})



