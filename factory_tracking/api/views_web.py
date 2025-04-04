from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from users.models import UserRole
from .models import ApiKey
from .forms import ApiKeyForm

@login_required
def api_key_management_view(request):
    if request.user.role != UserRole.MANAGER:
        return HttpResponseForbidden("You do not have permission to access this page.")

    if request.method == "POST":
        form = ApiKeyForm(request.POST)
        if form.is_valid():
            api_key = form.save(commit=False)
            api_key.owner = request.user
            api_key.save()
            return redirect("manage_api_keys")
    else:
        form = ApiKeyForm()

    keys = ApiKey.objects.filter(owner=request.user)
    return render(request, "api/manage_api_keys.html", {
        "form": form,
        "api_keys": keys,
    })
