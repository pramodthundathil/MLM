from django.shortcuts import render, redirect
from Home.models import *


def AdminDashView(request):
    return render(request,"dashboard/index.html")





