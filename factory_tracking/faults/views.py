from django.shortcuts import render

def faults(request):
    context = {}
    return render(request, "faults/faults.html", context)
