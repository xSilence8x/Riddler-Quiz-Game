from django.urls import path
from .views import HomeView, UserRegisterView, UserLoginView, KvizView, InvalidateTokenView, CustomPasswordResetView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("kviz/", KvizView.as_view(), name="kviz"),
    path('invalid_token/', InvalidateTokenView.as_view(), name='invalid_token'),
    path('reset_password/', CustomPasswordResetView.as_view(), name='password_reset'),
    # path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "registration/password_reset_form.html"), name ='reset_password'),
    # path('reset_password/', ResetPasswordView.as_view(), name ='reset_password'),

    # path("otazka/", Otazka.as_view(), name="otazka"),
    # path("konec-kvizu/", Konec.as_view(), name="quiz_completed"),
]
