from django.shortcuts import render, get_object_or_404, redirect
from .models import Machine
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from users.models import UserRole, User

@login_required
def machines(request):
    user = request.user
    users = [user.username for user in User.objects.filter(role__in=[UserRole.TECHNICIAN, UserRole.REPAIR])]

    all_machines = list(
        Machine.objects.prefetch_related('collections', 'assigned_users', 'warnings').all()
    )

    assigned = []
    unassigned = []

    for machine in all_machines:
        if user in machine.assigned_users.all():
            assigned.append(machine)
        else:
            unassigned.append(machine)

    ordered_machines = assigned + unassigned

    machines = []
    for machine in ordered_machines:
        machines.append({
            "id": machine.id,
            "name": machine.name,
            "status": machine.status,
            "collection": ", ".join([c.name for c in machine.collections.all()]),
            "warnings": machine.warnings.count(),
            "technicians": [u.username for u in machine.assigned_users.filter(role=UserRole.TECHNICIAN)],
            "repairers": [u.username for u in machine.assigned_users.filter(role=UserRole.REPAIR)],
            "assignedTo": [u.role for u in machine.assigned_users.all()],
        })

    context = {
        "machines": machines,
        "user_role": user.role.lower(),
        "usernames": users if user.role == UserRole.MANAGER else [],
    }

    return render(request, "machinery/machines.html", context)


def machine_detail(request, machine_id):
    user = request.user
    machine = get_object_or_404(Machine, id=machine_id)
    faults = machine.faults.select_related("reported_by").all()

    context = {
        "machine": machine,
        "collections": machine.collections.all(),
        "faults": faults,
        "technicians": machine.assigned_users.filter(role=UserRole.TECHNICIAN),
        "repairers": machine.assigned_users.filter(role=UserRole.REPAIR),
        "warnings": machine.warnings.all(),
        "is_manager": user.role == UserRole.MANAGER,
        "can_add_warning": user.role in [UserRole.TECHNICIAN, UserRole.REPAIR, UserRole.MANAGER],
        "all_usernames": list(User.objects.values_list("username", flat=True)) if user.role == UserRole.MANAGER else [],
        "assigned_usernames": list(machine.assigned_users.values_list("username", flat=True)) if user.role == UserRole.MANAGER else [],
    }
    return render(request, "machinery/detail.html", context)


@login_required
@require_POST
def create_machine(request):
    if request.user.role != UserRole.MANAGER:
        return HttpResponseForbidden("You are not authorized to create a machine.")
    name = request.POST.get("name")
    status = request.POST.get("status")
    collections_raw = request.POST.get("collections", "")
    assigned_raw = request.POST.get("assigned", "")

    # [TODO] Add the new machine in database

    return redirect("machines")


@login_required
@require_POST
def edit_machine(request, machine_id):
    if request.user.role != UserRole.MANAGER:
        return HttpResponseForbidden("You are not authorized to update a machine.")
    name = request.POST.get("name")
    status = request.POST.get("status")
    collections_raw = request.POST.get("collections", "")
    assigned_raw = request.POST.get("assigned", "")

    # [TODO] Update the machine in database

    return redirect("machine_detail", machine_id=machine_id)


@require_POST
@login_required
def delete_machine(request, machine_id):
    if request.user.role != UserRole.MANAGER:
        return HttpResponseForbidden("Only managers can delete machines.")

    # [TODO] Delete the machine from the database
    return redirect("machines")


@login_required
@require_POST
def add_warning(request, machine_id):
    user = request.user
    if user.role not in [UserRole.MANAGER, UserRole.TECHNICIAN, UserRole.REPAIR]:
        return HttpResponseForbidden("You are not allowed to add warnings.")

    message = request.POST.get("message", "").strip()

    if message:
        # [TODO] Add warning to machine
        print(f"Adding warning to machine {machine_id}: {message}")


    return redirect("machine_detail", machine_id=machine_id)
