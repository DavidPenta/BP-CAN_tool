from CAN_tool_app.forms import AuthForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from CAN_tool_app.models import UserPreferences


def login_request(request):
    if request.method == "POST":
        form = AuthForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            UserPreferences.objects.get_or_create(user=username)
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('cars')
            else:
                messages.error(request, "Neplatné používaťelské meno aleno heslo.")
        else:
            messages.error(request, "Neplatné používaťelské meno aleno heslo.")

    if request.user.is_authenticated:
        return redirect('cars')

    form = AuthForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Odhlásenie bolo úspešné")
    return redirect('login')
