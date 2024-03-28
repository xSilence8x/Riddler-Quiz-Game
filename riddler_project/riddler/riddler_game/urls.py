from django.urls import path
from .views import HomeView, UserRegisterView, UserLoginView, KvizView, InvalidateTokenView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("kviz/", KvizView.as_view(), name="kviz"),
    path('invalid_token/', InvalidateTokenView.as_view(), name='invalid_token'),
    # path("otazka/", Otazka.as_view(), name="otazka"),
    # path("konec-kvizu/", Konec.as_view(), name="quiz_completed"),
]
