from django.shortcuts import render

def machines(request):
    context = {}
    return render(request, "machinery/machines.html", context)
