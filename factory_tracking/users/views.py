from django.shortcuts import render


def login(request):
    context = {}
    return render(request, "users/login.html", context)

def dashboard(request):
    context = {}
    return render(request, "users/dashboard.html", context)
