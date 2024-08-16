from django.contrib.auth.views import LoginView

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator

from .forms import ContactForm, RegisterForm, PolygonForm, ScenarioForm
import telegram

from .models import Buyer, Polygon, Scenario


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


def statistics(request):
    return render(request, 'main/statistics.html', {'title': 'Статистика боёв'})


def polygons(request):
    polygons_list = Polygon.objects.all()
    return render(request, 'main/polygon.html', {'polygons': polygons_list})


def scenarios(request):
    return render(request, 'main/scenarios.html', {'title': 'Сценарии'})


def cabinet(request):
    return render(request, 'main/cabinet.html', {'title': 'Личный кабинет'})


@login_required
def profile_view(request):
    buyer = Buyer.objects.get(username=request.user.username)  # Получение текущего пользователя из модели Buyer

    return render(request, 'main/profile.html', {'buyer': buyer})


class RegisterView(CreateView):
    model = Buyer
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("main:profile")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# class LoginView(LoginView):
#     template_name = 'main/registration/login.html'


class PolygonListView(ListView):
    model = Polygon
    template_name = 'polygon/polygon.html'


class PolygonDetailView(DetailView):
    model = Polygon
    template_name = 'polygon_detail.html'


@method_decorator(login_required, name='dispatch')
class PolygonCreateView(CreateView):
    model = Polygon
    fields = ['title', 'description', 'image1', 'image2', 'image3', 'image4']
    template_name = 'polygon/polygon_form.html'
    success_url = reverse_lazy('main:polygons')


@method_decorator(login_required, name='dispatch')
class PolygonUpdateView(UpdateView):
    model = Polygon
    fields = ['title', 'description', 'image1', 'image2', 'image3', 'image4']
    template_name = 'polygon/polygon_edit.html'
    success_url = reverse_lazy('main:polygons')


@method_decorator(login_required, name='dispatch')
class PolygonDeleteView(DeleteView):
    model = Polygon
    template_name = 'polygon/polygon_confirm_delete.html'
    success_url = reverse_lazy('main:polygons')


# -----------------------------------------------------------------------------------

class ScenarioListView(ListView):
    model = Scenario
    template_name = 'scenarios/scenario_list.html'  # Путь к шаблону
    context_object_name = 'scenarios'  # Имя переменной для доступа к данным в шаблоне


class ScenarioCreateView(CreateView):
    model = Scenario
    form_class = ScenarioForm
    template_name = 'scenarios/scenario_form.html'
    success_url = reverse_lazy('main:scenario-list')


class ScenarioUpdateView(UpdateView):
    model = Scenario
    form_class = ScenarioForm
    template_name = 'scenarios/scenario_form.html'
    success_url = reverse_lazy('main:scenario-list')


class ScenarioDeleteView(DeleteView):
    model = Scenario
    template_name = 'scenarios/scenario_confirm_delete.html'
    success_url = reverse_lazy('main:scenario-list')
