from collections import defaultdict
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme
from machinery.models import Machine, Collection
from users.models import UserRole
from collections import defaultdict
import json
from django.http import HttpResponseForbidden
from django.contrib.auth.hashers import make_password
from .export import export_csv, export_pdf
from django.http import HttpResponse



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
        User = get_user_model()
        users = User.objects.all().values('id', 'email', 'username', 'role')


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
            "users": users,
            "roles": UserRole.choices,
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
    if request.user.role != UserRole.MANAGER:
        return HttpResponseForbidden("Only managers can export data.")
    export_type = request.POST.get("type")
    machines = Machine.objects.all().select_related().prefetch_related("collections")

    if export_type == "csv":
        return export_csv(machines)
    elif export_type == "pdf":
        return export_pdf(machines)
    else:
        return HttpResponse("Invalid export type", status=400)



@login_required
@require_POST
def create_user_or_edit(request):
    if request.user.role != UserRole.MANAGER:
        return HttpResponseForbidden("Only managers can manage users.")

    User = get_user_model()
    user_id = request.POST.get("user_id")
    email = request.POST.get("email")
    username = request.POST.get("username")
    password = request.POST.get("password")
    role = request.POST.get("role")

    if not username or role not in UserRole.values:
        return HttpResponseForbidden("Invalid data provided.")

    if user_id:
        try:
            user = User.objects.get(id=user_id)
            user.username = username
            user.email = email
            user.role = role
            user.save()
        except User.DoesNotExist:
            return HttpResponseForbidden("User not found.")
    else:
        if not password:
            return HttpResponseForbidden("Password is required for new users.")
        if User.objects.filter(username=username).exists():
            return HttpResponseForbidden("Username already exists.")
        else:
            User.objects.create(
                username=username,
                email=email,
                password=make_password(password),
                role=role
            )
    return redirect("dashboard")


@require_POST
@login_required
def delete_user(request):
    if request.user.role != UserRole.MANAGER:
        return HttpResponseForbidden("Only managers can delete users.")

    User = get_user_model()
    user_id = request.POST.get("user_id")

    try:
        user = User.objects.get(id=user_id)
        user.delete()
    except User.DoesNotExist:
        return HttpResponseForbidden("User not found.")

    return redirect("dashboard")
