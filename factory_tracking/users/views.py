from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme


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
    context = {}
    # [TODO] Fetch user/machines/faults information and add them to the context
    return render(request, "users/dashboard.html", context)


@login_required
def export_data(request):
    context = {}
    # [TODO] create file to be exported (https://github.com/ChoKssa/EEN1037_Web_Application/blob/main/doc/api_specifications.md#endpoint-get-apireportsformatcsvpdf-manager-only)


@login_required
def list_users(request):
    context = {}
    # [TODO] Fetch and display the list of users (https://github.com/ChoKssa/EEN1037_Web_Application/blob/main/doc/api_specifications.md#endpoint-get-apiusers-manager-only)
    # return render(request, "users/list_users.html", context)


@login_required
def create_user(request):
    context = {}
    if request.method == "POST":
        # [TODO] Handle user creation logic here (https://github.com/ChoKssa/EEN1037_Web_Application/blob/main/doc/api_specifications.md#endpoint-post-apiusers)
        pass

    # return render(request, "users/create_user.html", context)


@login_required
def update_user_role(request):
    context = {}

    if request.method == "PATCH":
        # [TODO] Change user role (https://github.com/ChoKssa/EEN1037_Web_Application/blob/main/doc/api_specifications.md#endpoint-put-apiusersid-manager-only)
        pass


@login_required
def delete_user(request):
    context = {}
    if request.method == "DELETE":
        # [TODO] Delete user account (https://github.com/ChoKssa/EEN1037_Web_Application/blob/main/doc/api_specifications.md#endpoint-delete-apiusersid-manager-only)
        pass
