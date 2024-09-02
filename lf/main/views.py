from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from .decorators import manager_required
from .forms import ContactForm, ScenarioForm, ManagerRegistrationForm, PlayerRegistrationForm, SectionForm, \
    EquipmentForm
from .models import Polygon, Scenario, CustomUser, Section, Equipment
from django.contrib.auth.views import LoginView


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
                'reflex002@bk.ru',  # ваш email
                ['reflex002@bk.ru'],  # email получателя
                fail_silently=False,
            )

            return redirect('main:mainpage')
    else:
        form = ContactForm()

    is_admin = request.user.is_superuser
    is_manager = request.user.groups.filter(name='Менеджеры').exists() if request.user.is_authenticated else False

    return render(request, 'main/mainpage.html', {
        'form': form,
        'is_admin': is_admin,
        'is_manager': is_manager,
    })


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
    # Получаем текущего пользователя
    user = request.user

    # Проверяем тип пользователя
    if user.is_manager():
        user_type = 'manager'
    elif user.is_player():
        user_type = 'player'
    else:
        user_type = 'unknown'

    context = {
        'user': user,
        'user_type': user_type,
    }

    return redirect('main:player_profile', pk=user.pk)


class PolygonListView(ListView):
    model = Polygon
    template_name = 'polygon/polygon.html'


@method_decorator([login_required, user_passes_test(manager_required)], name='dispatch')
class PolygonDetailView(DetailView):
    model = Polygon
    template_name = 'polygon_detail.html'


@method_decorator([login_required, user_passes_test(manager_required)], name='dispatch')
class PolygonCreateView(CreateView):
    model = Polygon
    fields = ['title', 'description', 'image1', 'image2', 'image3', 'image4']
    template_name = 'polygon/polygon_form.html'
    success_url = reverse_lazy('main:polygons')


@method_decorator([login_required, user_passes_test(manager_required)], name='dispatch')
class PolygonUpdateView(UpdateView):
    model = Polygon
    fields = ['title', 'description', 'image1', 'image2', 'image3', 'image4']
    template_name = 'polygon/polygon_edit.html'
    success_url = reverse_lazy('main:polygons')


@method_decorator([login_required, user_passes_test(manager_required)], name='dispatch')
class PolygonDeleteView(DeleteView):
    model = Polygon
    template_name = 'polygon/polygon_confirm_delete.html'
    success_url = reverse_lazy('main:polygons')


# -----------------------------------------------------------------------------------
class ScenarioListView(ListView):
    model = Scenario
    template_name = 'scenarios/scenario_list.html'
    context_object_name = 'scenarios'  # Имя переменной для доступа к данным в шаблоне


@method_decorator([login_required, user_passes_test(manager_required)], name='dispatch')
class ScenarioCreateView(CreateView):
    model = Scenario
    form_class = ScenarioForm
    template_name = 'scenarios/scenario_form.html'
    success_url = reverse_lazy('main:scenario-list')


@method_decorator([login_required, user_passes_test(manager_required)], name='dispatch')
class ScenarioUpdateView(UpdateView):
    model = Scenario
    form_class = ScenarioForm
    template_name = 'scenarios/scenario_form.html'
    success_url = reverse_lazy('main:scenario-list')


@method_decorator([login_required, user_passes_test(manager_required)], name='dispatch')
class ScenarioDeleteView(DeleteView):
    model = Scenario
    template_name = 'scenarios/scenario_confirm_delete.html'
    success_url = reverse_lazy('main:scenario-list')


# -----------------------------------------------------------------------------------

User = get_user_model()


@login_required
def register_manager(request):
    if request.method == 'POST':
        form = ManagerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = ManagerRegistrationForm()
    return render(request, 'registration/register_manager.html', {'form': form})


@login_required
@user_passes_test(manager_required)
def register_player(request):
    if request.method == 'POST':
        form = PlayerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:player_list')
    else:
        form = PlayerRegistrationForm()
    return render(request, 'registration/register_player.html', {'form': form})


@login_required
@user_passes_test(manager_required)
def player_list(request):
    sort_by = request.GET.get('sort_by', 'username')
    search_query = request.GET.get('search', '').strip()

    if sort_by not in ['username', 'email', 'first_name', 'last_name']:
        sort_by = 'username'

    # Разделение поискового запроса на слова (чтобы поддерживать поиск по имени и фамилии)
    search_terms = search_query.split()

    # Создание Q объекта для объединения условий поиска
    query = Q(user_type='player')

    if len(search_terms) == 1:
        # Если только один термин, то ищем по всем полям
        query &= (Q(username__icontains=search_terms[0]) |
                  Q(email__icontains=search_terms[0]) |
                  Q(first_name__icontains=search_terms[0]) |
                  Q(last_name__icontains=search_terms[0]))
    elif len(search_terms) > 1:
        # Если два и более терминов, то пробуем искать как комбинацию имени и фамилии
        query &= (Q(first_name__icontains=search_terms[0], last_name__icontains=search_terms[1]) |
                  Q(last_name__icontains=search_terms[0], first_name__icontains=search_terms[1]))

    players = CustomUser.objects.filter(query).order_by(sort_by)

    return render(request, 'player_list.html', {
        'players': players,
        'sort_by': sort_by,
        'search_query': search_query,
    })


# -----------------------------------------------------------------------------------

def section_list(request):
    sections = Section.objects.all()
    return render(request, 'section/section_list.html', {'sections': sections})


@login_required
@user_passes_test(manager_required)
def add_section(request):
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.user = request.user
            section.save()
            return redirect('main:section_list')
    else:
        form = SectionForm()
    return render(request, 'section/add_section.html', {'form': form})


@login_required
@user_passes_test(manager_required)
def edit_section(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect('main:section_list')
    else:
        form = SectionForm(instance=section)
    return render(request, 'section/edit_section.html', {'form': form})


@login_required
@user_passes_test(manager_required)
def delete_section(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        section.delete()
        return redirect('main:section_list')
    return render(request, 'section/delete_section.html', {'section': section})


# -----------------------------------------------------------------------------------


@login_required
def player_profile(request, pk):
    player = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'player_profile.html', {'player': player})


@login_required
@user_passes_test(manager_required)
def delete_player(request, pk):
    player = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        player.delete()
        return redirect('main:player_list')


@login_required
@user_passes_test(manager_required)
def change_password(request, pk):
    # Получаем пользователя, чей пароль нужно изменить
    user = get_object_or_404(CustomUser, pk=pk)

    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            # Обновляем сессию, чтобы пользователь оставался авторизованным
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль был успешно изменен.')
            return redirect('main:player_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
    else:
        form = PasswordChangeForm(user)

    return render(request, 'main/change_password.html', {
        'form': form,
        'player': user
    })


# -----------------------------------------------------------------------------------


def equipment_list(request):
    equipment = Equipment.objects.all()
    return render(request, 'equipment/equipment_list.html', {'equipment': equipment})


@login_required
@user_passes_test(manager_required)
def add_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main:equipment_list')
    else:
        form = EquipmentForm()
    return render(request, 'equipment/add_equipment.html', {'form': form})


@login_required
@user_passes_test(manager_required)
def edit_equipment(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, request.FILES, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('main:equipment_list')
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'equipment/edit_equipment.html', {'form': form})


@login_required
@user_passes_test(manager_required)
def delete_equipment(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        equipment.delete()
        return redirect('main:equipment_list')
    return render(request, 'equipment/delete_equipment.html', {'equipment': equipment})
