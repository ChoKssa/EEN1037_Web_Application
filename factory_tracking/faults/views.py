from django.shortcuts import render, get_object_or_404
from .models import FaultCase, FaultNote, FaultNoteImage, FaultImage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from machinery.models import Machine, MachineStatus
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
    can_close = user.role in ['MANAGER', 'REPAIR'] and fault.status == 'OPEN'

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

    # Validate input
    if not machine_name or not description:
        return HttpResponseForbidden("Machine and description are required.")

    # Create fault
    try:
        machine = Machine.objects.get(name=machine_name)
        fault = FaultCase.objects.create(
            machine=machine,
            description=description,
            reported_by=user,
            status='OPEN',
            created_at=timezone.now()
        )

        for image in images:
            FaultImage.objects.create(
                image=image,
                fault_case=fault,
            )

        machine.status = MachineStatus.FAULT
        machine.save()

    except Machine.DoesNotExist:
        return HttpResponseForbidden("Invalid machine specified.")
    except Exception as e:
        print(f"Error creating fault: {str(e)}")
        return HttpResponseForbidden("Error occurred while creating fault.")

    return redirect("faults")


@require_POST
@login_required
def add_fault_note(request, fault_id):
    fault = get_object_or_404(FaultCase, id=fault_id)

    if request.user.role not in ['TECH', 'REPAIR', 'MANAGER']:
        return HttpResponseForbidden("Not allowed to add note.")

    if fault.status == 'CLOSED':
        return HttpResponseForbidden("Cannot add note to a closed fault.")

    content = request.POST.get("content")
    images = request.FILES.getlist("images")

    # Create fault note in db
    try:
        note = FaultNote.objects.create(
            fault_case=fault,
            author=request.user,
            content=content,
            created_at=timezone.now()
        )

        # Save images if any were uploaded
        for image in images:
            FaultNoteImage.objects.create(
                image=image,
                note=note,
            )

    except Exception as e:
        print(f"Error adding note: {str(e)}")
        return HttpResponseForbidden("Error occurred while adding note.")


    return redirect("fault_detail", fault_id=fault.id)


@require_POST
@login_required
def close_fault(request, fault_id):
    fault = get_object_or_404(FaultCase, id=fault_id)

    if request.user.role not in ["MANAGER", "REPAIR"]:
        return HttpResponseForbidden("Only managers can close faults.")

    # Close fault in db
    try:
        fault.status = 'CLOSED'
        # Create a closure note
        FaultNote.objects.create(
            fault_case=fault,
            author=request.user,
            content="Fault closed",
            created_at=timezone.now()
        )
        fault.closed_at = timezone.now()
        fault.save()

        if fault.machine.status == MachineStatus.FAULT:
            if fault.machine.faults.filter(status='OPEN').exists():
                fault.machine.status = MachineStatus.FAULT
            elif fault.machine.warnings.exists():
                fault.machine.status = MachineStatus.WARNING
            else:
                fault.machine.status = MachineStatus.OK
            fault.machine.save()

    except Exception as e:
        print(f"Error closing fault: {str(e)}")
        return HttpResponseForbidden("Error occurred while closing fault.")


    return redirect("fault_detail", fault_id=fault.id)
