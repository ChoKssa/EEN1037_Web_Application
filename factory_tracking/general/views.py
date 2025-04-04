from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from .models import ContactMessage


def index(request):
    context = {}
    return render(request, "general/index.html", context)


def contact(request):
    context = {}
    return render(request, "general/contact.html", context)


@require_POST
def submit_contact_form(request):
    ContactMessage.objects.create(
        name=request.POST.get("name"),
        email=request.POST.get("email"),
        message=request.POST.get("message")
    )

    messages.success(request, "Your message has been sent successfully. Our support team will get back to you shortly.")
    return redirect("contact")


def about(request):
    context = {}
    return render(request, "general/about.html", context)


def help(request):
    context = {}
    return render(request, "general/help.html", context)
