from collections import defaultdict
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme
from machinery.models import Machine, Warning, Collection
from users.models import UserRole
from collections import defaultdict
from django.db.models import Count
import json 



def login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        next_url = request.POST.get("next")

        if user is not None:
            auth_login(request, user)

            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)

            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "users/login.html")



def logout(request):
    auth_logout(request)
    return redirect("login")



@login_required
def dashboard(request):
    user = request.user
    role = user.role
    context = {"user_role": role}

    if role == UserRole.MANAGER:
        all_machines = Machine.objects.prefetch_related("collections")
        collections = Collection.objects.prefetch_related("machines")
        machines_by_collection = defaultdict(list)

        
        counts = json.dumps([
            Machine.objects.filter(status="OK").count(),
            Machine.objects.filter(status="FAULT").count(),
            Machine.objects.filter(status="WARNING").count()
        ])
        labels = json.dumps(["OK", "Fault", "Warning"])


        for machine in all_machines:
            for collection in machine.collections.all():
                machines_by_collection[collection.name].append(machine)
  

        context.update({
            "machines": all_machines,
            "fault_count": all_machines.filter(status="FAULT").count(),
            "ok_count": all_machines.filter(status="OK").count(),
            "warning_count": all_machines.filter(status="WARNING").count(),  
            "collections": collections,
            "machines_by_collection": machines_by_collection,
            "labels": labels,
            "counts": counts,
        })

    elif role in [UserRole.TECHNICIAN, UserRole.REPAIR]:
        assigned = Machine.objects.filter(assigned_users=user).prefetch_related("collections", "warnings")
        context.update({
            "assigned_machines": assigned,
            "assigned_count": assigned.count(),
        })

    else:
        context["message"] = "You have view-only access."

    return render(request, "users/dashboard.html", context)

@login_required
@require_POST
def export_data(request):
    context = {}
    # [TODO] create file to be exported
    # [TODO] return file to be downloaded


@login_required
def accounts(request):
    context = {}
    # [TODO] Fetch all users and their information and add them to the context (only for manager)
    return render(request, "users/accounts.html", context)


@login_required
@require_POST
def create_user(request):
    context = {}
    # [TODO] Handle user creation logic here

    # return render(request, "users/create_user.html", context)


@login_required
@require_POST
def update_user_role(request):
    context = {}
    # [TODO] Change user role


@login_required
@require_POST
def delete_user(request):
    context = {}
    # [TODO] Delete user account
