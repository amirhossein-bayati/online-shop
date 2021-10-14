from django.shortcuts import render
from django.http import HttpResponse

def homePage(request):
    return render(request, 'blog/parents/base.html')

