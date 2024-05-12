from django.contrib.auth.views import LogoutView, PasswordChangeView, \
    LoginView, PasswordChangeDoneView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy

from users.forms import CustomLoginForm

from . import views
from .views import CustomPasswordResetView

app_name = 'users'

urlpatterns = [
    path('logout/', LogoutView.as_view(
        template_name='users/logged_out.html'), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('password_change/', PasswordChangeView.as_view(
        template_name='users/password_change_form.html',
        success_url=reverse_lazy('users:password_change_done')),
         name='password_change_form'),
    path('login/', LoginView.as_view(
        template_name='users/login.html',
        authentication_form=CustomLoginForm
        ),
         name='login'
         ),
    path('password_reset/', CustomPasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        success_url=reverse_lazy('users:password_reset_done')
    ),
         name='password_reset_form'
         ),
    path('password_change/done/', PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'),
         name='password_change_done'
         ),
    path('password_rest/done/', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'),
         name='password_reset_done'
         ),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy(
            'users:password_reset_complete')),
         name='password_reset_confirm'
         ),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),
         name='password_reset_complete'
         ),
]
