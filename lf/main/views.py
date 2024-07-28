from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm
import telegram




def mainpage(request):
    return render(request,'main/mainpage.html', {'title': 'Главная'})
def statistics(request):
    return render(request,'main/statistics.html', {'title': 'Статистика боёв'})
def polygons(request):
    return render(request,'main/polygons.html', {'title': 'Полигоны'})
def scenarios(request):
    return render(request,'main/scenarios.html', {'title': 'Сценарии'})
def cabinet(request):
    return render(request,'main/cabinet.html', {'title': 'Личный кабинет'})


def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Отправка email
            send_mail(
                'Contact Form Submission',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            # Отправка сообщения в Telegram
            bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
            bot.send_message(
                chat_id=settings.TELEGRAM_CHAT_ID,
                text=f"New contact form submission:\n\nName: {name}\nEmail: {email}\nMessage: {message}"
            )

            return HttpResponseRedirect('/')
    else:
        form = ContactForm()

    return render(request, 'main/mainpage.html', {'form': form})
