import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import GameFile
from .forms import GameFileForm, EditGamerForm


def upload_file(request):
    if request.method == 'POST':
        form = GameFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('game:success')
    else:
        form = GameFileForm()
    return render(request, 'game/upload.html', {'form': form})


def edit_gamer_in_file(file_path, new_name, old_gamer_id):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Проходим по всем элементам Gamer и изменяем Name и GamerID
    for gamer in root.findall('Gamer'):
        if gamer.get('GamerID') == str(old_gamer_id):
            gamer.set('Name', new_name)
            gamer.set('GamerID', new_name)  # Заменяем GamerID на новое имя

        # Проходим по всем элементам Hit внутри каждого Gamer
        for hit in gamer.findall('Hit'):
            if hit.get('GamerID') == str(old_gamer_id):
                hit.set('GamerID', new_name)  # Заменяем GamerID в Hit на новое имя

    # Сохраняем изменения обратно в файл
    tree.write(file_path)
    return True


def edit_gamer_view(request, file_id):
    game_file = get_object_or_404(GameFile, pk=file_id)

    if request.method == 'POST':
        form = EditGamerForm(request.POST)
        if form.is_valid():
            new_name = form.cleaned_data['new_name']
            new_gamer_id = form.cleaned_data['gamer_id']
            edit_gamer_in_file(game_file.file.path, new_name, new_gamer_id)
            return redirect('game:success')
    else:
        form = EditGamerForm()

    return render(request, 'game/edit_gamer.html', {'form': form})


def success_view(request):
    return render(request, 'game/success.html')


def file_list_view(request):
    files = GameFile.objects.all()  # Получаем все файлы из базы данных
    return render(request, 'game/file_list.html', {'files': files})


def delete_file_view(request, file_id):
    file = get_object_or_404(GameFile, pk=file_id)
    file.delete()
    return redirect('game:file_list')


def file_stats_view(request, file_id):
    game_file = get_object_or_404(GameFile, pk=file_id)

    # Парсим XML-файл
    tree = ET.parse(game_file.file.path)
    root = tree.getroot()

    # Сбор статистики по каждому GamerID
    stats = {}

    for gamer in root.findall('.//Gamer'):  # Ищем все элементы Gamer
        shooter_id = gamer.get('GamerID')

        # Проверяем, есть ли GamerID в stats, если нет, то добавляем
        if shooter_id not in stats:
            stats[shooter_id] = {
                'name': gamer.get('Name'),
                'team_color': gamer.get('TeamColor'),
                'weapon_damage': gamer.get('WiaponDamage'),
                'fire_count': gamer.get('FireCount'),
                'frags': gamer.get('Frags'),
                'killed': gamer.get('Killed'),
                'medicine': gamer.get('Medicine'),
                'ammo': gamer.get('Ammo'),
                'damage': gamer.get('Damage'),
                'game_time': gamer.get('GameTime'),
                'total_hits': 0,
                'targets': {}
            }

        for hit in gamer.findall('Hit'):  # Ищем все элементы Hit внутри Gamer
            target_id = hit.get('GamerID')
            hits = int(hit.get('Hits'))

            # Суммируем общее количество попаданий для данного игрока
            stats[shooter_id]['total_hits'] += hits

            if hits > 0:  # Добавляем в targets только если hits > 0
                if target_id in stats[shooter_id]['targets']:
                    stats[shooter_id]['targets'][target_id] += hits
                else:
                    stats[shooter_id]['targets'][target_id] = hits

    return render(request, 'game/file_stats.html', {'stats': stats, 'file': game_file})