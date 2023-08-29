from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib import auth
from django.shortcuts import render, redirect
from .selectors import get_referral_code
from .services import award_referee
from ..core.models import Referral


class LoginView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, "login.html", context)

    def post(self, request, *args, **kwargs):
        username = self.request.POST.get("username")
        password = self.request.POST.get("password")

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("core:portfolio")
        return render(request, "login.html")


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return redirect("authentication:login")


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, "signup.html", context)

    def post(self, request, *args, **kwargs):
        context = {}
        username = self.request.POST.get("username")
        referal_code = self.request.POST.get("code")
        password1 = self.request.POST.get("password1")
        password2 = self.request.POST.get("password2")

        if password1 != password2:
            return render(request, "signup.html", context)

        user = User.objects.create_user(username=username, password=password1)
        code_obj = get_referral_code(referal_code)
        if code_obj is not None:
            award_referee(referal_code)
            Referral.objects.create(inviter=code_obj.user, invitee=user, code=code_obj)
        return redirect("core:portfolio")
