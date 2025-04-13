from django.shortcuts import render, get_object_or_404, redirect
from .models import Machine, Collection, Warning, MachineStatus
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
        "user_role": user.role,
        "machine": machine,
        "collections": machine.collections.all(),
        "faults": faults,
        "technicians": machine.assigned_users.filter(role=UserRole.TECHNICIAN),
        "repairers": machine.assigned_users.filter(role=UserRole.REPAIR),
        "warnings": machine.warnings.all(),
        "is_manager": user.role == UserRole.MANAGER,
        "can_add_warning": user.role in [UserRole.TECHNICIAN, UserRole.MANAGER],
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
    machine = Machine.objects.create(name=name, status=status)

    # Add collections
    collection_names = [c.strip() for c in collections_raw.split(",") if c.strip()]
    collections = []

    for name in collection_names:
        collection, _ = Collection.objects.get_or_create(name=name)
        collections.append(collection)
    machine.collections.set(collections)

    # Add assigned users
    usernames = [u.strip() for u in assigned_raw.split(",") if u.strip()]
    users = User.objects.filter(username__in=usernames)
    machine.assigned_users.set(users)
    machine.save()

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

    machine = get_object_or_404(Machine, id=machine_id)
    machine.name = name
    machine.status = status

    collection_names = [c.strip() for c in collections_raw.split(",") if c.strip()]
    collections = []

    for name in collection_names:
        collection, _ = Collection.objects.get_or_create(name=name)
        collections.append(collection)
    machine.collections.set(collections)

    usernames = [u.strip() for u in assigned_raw.split(",") if u.strip()]
    users = User.objects.filter(username__in=usernames)
    machine.assigned_users.set(users)

    machine.save()

    return redirect("machine_detail", machine_id=machine_id)


@require_POST
@login_required
def delete_machine(request, machine_id):
    if request.user.role != UserRole.MANAGER:
        return HttpResponseForbidden("Only managers can delete machines.")

    machine = get_object_or_404(Machine, id=machine_id)
    machine.delete()
    return redirect("machines")


@login_required
@require_POST
def add_warning(request, machine_id):
    user = request.user
    if user.role not in [UserRole.MANAGER, UserRole.TECHNICIAN]:
        return HttpResponseForbidden("You are not allowed to add warnings.")

    message = request.POST.get("message", "").strip()

    if message:
        print(f"Adding warning to machine {machine_id}: {message}")

        machine = get_object_or_404(Machine, id=machine_id)
        # Prevent duplicate message for same machine (due to unique_together)
        if not Warning.objects.filter(machine=machine, message=message).exists():
            Warning.objects.create(
                machine=machine,
                message=message,
                added_by=user
            )

            if machine.status == MachineStatus.OK:
                machine.status = MachineStatus.WARNING
                machine.save()

    return redirect("machine_detail", machine_id=machine_id)


@login_required
@require_POST
def delete_warning(request, machine_id):
    user = request.user
    if user.role not in [UserRole.MANAGER, UserRole.TECHNICIAN, UserRole.REPAIR]:
        return HttpResponseForbidden("You are not allowed to delete warnings.")

    warning_id = request.POST.get("warning_id")
    warning = get_object_or_404(Warning, id=warning_id)

    if warning.machine.id == machine_id:
        warning.delete()

        # Check if there are any warnings left for the machine
        if not Warning.objects.filter(machine=warning.machine).exists():
            if warning.machine.faults.filter(status='OPEN').exists():
                warning.machine.status = MachineStatus.FAULT
            else:
                warning.machine.status = MachineStatus.OK
            warning.machine.save()
    else:
        return HttpResponseForbidden("Warning does not belong to this machine.")
    return redirect("machine_detail", machine_id=machine_id)
