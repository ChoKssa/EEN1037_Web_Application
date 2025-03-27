from django.shortcuts import render


def index(request):
    context = {}
    return render(request, "general/index.html", context)

def contact(request):
    context = {}
    return render(request, "general/contact.html", context)

def about(request):
    context = {}
    return render(request, "general/about.html", context)

def help(request):
    context = {}
    return render(request, "general/help.html", context)
