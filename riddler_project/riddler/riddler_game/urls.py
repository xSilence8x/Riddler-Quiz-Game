from django.urls import path
from .views import HomeView, UserRegisterView, UserLoginView, KvizView, InvalidateTokenView, CustomPasswordResetView, CustomPasswordResetConfirmView, CustomPasswordResetDoneView, CustomPasswordResetCompleteView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("kviz/", KvizView.as_view(), name="kviz"),
    path('neplatny-token/', InvalidateTokenView.as_view(), name='invalid_token'),
    path('obnovit-heslo/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('obnovit-heslo/hotovo/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/hotovo/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
