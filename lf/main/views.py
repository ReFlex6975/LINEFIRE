from django.shortcuts import render
from django.http import HttpResponse

def mainpage(request):
    return render(request,'main/mainpage.html')
def index(request):
    return render(request,'main/index.html')
def about(request):
    return render(request,'main/about.html')

