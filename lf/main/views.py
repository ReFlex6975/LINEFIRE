from django.shortcuts import render
from django.http import HttpResponse

def mainpage(request):
    return render(request,'main/mainpage.html', {'title': 'Главная'})
def statistics(request):
    return render(request,'main/statistics.html', {'title': 'Статистика боёв'})
def polygons(request):
    return render(request,'main/polygons.html', {'title': 'Полигоны'})
def scenarios(request):
    return render(request,'main/scenarios.html', {'title': 'Сценарии'})
def about(request):
    return render(request,'main/about.html', {'title': 'Контакты'})
def cabinet(request):
    return render(request,'main/cabinet.html', {'title': 'Личный кабинет'})


