from django.shortcuts import render, get_object_or_404
# from .models import Fault
# from django.contrib.auth.decorators import login_required

# @login_required
def faults(request):
    context = {}
    return render(request, "faults/faults.html", context)

# @login_required
def fault_detail(request, id):
    # fault = get_object_or_404(Fault, pk=id)
    # return render(request, "faults/detail.html", {"fault": fault})
    return render(request, "faults/detail.html")
