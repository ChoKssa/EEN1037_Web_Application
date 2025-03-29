from django.shortcuts import render, get_object_or_404
# from .models import Machine
# from django.contrib.auth.decorators import login_required

# @login_required
def machines(request):
    context = {}
    return render(request, "machinery/machines.html", context)

# @login_required
def machine_detail(request, id):
    # machine = get_object_or_404(Machine, pk=id)
    # return render(request, "machinery/detail.html", {"machine": machine})
    return render(request, "machinery/detail.html")
