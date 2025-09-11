from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth import views


User = get_user_model()

# Create your views here.
class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html', {})
    def post(self, request):
        data = request.POST
        get_data = request.GET
        username = data.get('username').strip()
        password = data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_route = get_data.get('next')
            if next_route:
                return redirect(next_route)
            return redirect(settings.LOGIN_REDIRECT_URL)
        
        user_obj = User.objects.filter(username=username).exists()
        username_error = "Username does not exist."
        password_error = None

        if user_obj:
            username_error = None
            password_error = "Password is incorrect."

        context = {
            "username": username,
            "password": password,
            "username_error": username_error,
            "password_error": password_error,
        }
        return render(request, 'registration/login.html', context)

class LogoutView(views.LogoutView):
    pass

class PasswordResetView(views.PasswordResetView):
    success_url = reverse_lazy("accounts:password_reset_done")
    html_email_template_name = 'registration/password_reset_email.html'

class PasswordResetDoneView(views.PasswordResetDoneView):
    pass

class PasswordResetConfirmView(views.PasswordResetConfirmView):
    success_url = reverse_lazy("accounts:password_reset_complete")

class PasswordResetCompleteView(views.PasswordResetCompleteView):
    pass

class PasswordChangeView(views.PasswordChangeView):
    success_url = reverse_lazy("accounts:password_change_done")

class PasswordChangeDoneView(views.PasswordChangeDoneView):
    pass