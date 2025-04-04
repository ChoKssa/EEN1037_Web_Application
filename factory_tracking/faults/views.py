from django.shortcuts import render, get_object_or_404
from .models import FaultCase, FaultNote, FaultNoteImage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from machinery.models import Machine
from users.models import UserRole
from django.shortcuts import redirect
from django.utils import timezone

@login_required
def fault_list(request):
    user = request.user

    assigned_machines = user.assigned_machines.values_list('id', flat=True)

    assigned_faults = FaultCase.objects.filter(machine__id__in=assigned_machines)

    other_faults = FaultCase.objects.exclude(machine__id__in=assigned_machines)

    context = {
        "assigned_faults": assigned_faults,
        "other_faults": other_faults,
        "machine_names": list(Machine.objects.values_list("name", flat=True)),
        "user": request.user,
    }

    return render(request, "faults/faults.html", context)


@login_required
def fault_detail(request, fault_id):
    fault = get_object_or_404(FaultCase, id=fault_id)
    notes = fault.notes.select_related('author').prefetch_related('images').all()
    user = request.user

    can_add_note = user.role in ['TECH', 'REPAIR', 'MANAGER']
    can_close = user.role == 'MANAGER' and fault.status == 'OPEN'

    context = {
        "fault": fault,
        "notes": notes,
        "can_add_note": can_add_note,
        "can_close": can_close,
    }
    return render(request, "faults/detail.html", context)


@login_required
@require_POST
def create_fault(request):
    user = request.user
    if user.role not in [UserRole.MANAGER, UserRole.TECHNICIAN]:
        return HttpResponseForbidden("Only managers and technicians can report faults.")

    machine_name = request.POST.get("machine")
    description = request.POST.get("description")
    images = request.FILES.getlist("images")

    print(f"Machine Name: {machine_name}")
    print(f"Description: {description}")
    print(f"Images: {images}")

    # [TODO] Create fault in db

    return redirect("faults")


@require_POST
@login_required
def add_fault_note(request, fault_id):
    fault = get_object_or_404(FaultCase, id=fault_id)

    if request.user.role not in ['TECH', 'REPAIR', 'MANAGER']:
        return HttpResponseForbidden("Not allowed to add note.")

    content = request.POST.get("content")
    images = request.FILES.getlist("images")

    # [TODO] Create fault note in db

    return redirect("fault_detail", fault_id=fault.id)


@require_POST
@login_required
def close_fault(request, fault_id):
    fault = get_object_or_404(FaultCase, id=fault_id)

    if request.user.role != "MANAGER":
        return HttpResponseForbidden("Only managers can close faults.")

    # [TODO] Close fault (or set to Warning) in db

    return redirect("fault_detail", fault_id=fault.id)
