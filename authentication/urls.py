from django.urls import path
from django.views.generic import RedirectView

app_name = "authentication"

urlpatterns = [
    path("login/", RedirectView.as_view(url="/", permanent=False), name="login"),
    path("logout/", RedirectView.as_view(url="/", permanent=False), name="logout"),
    path("signup/", RedirectView.as_view(url="/", permanent=False), name="signup"),
]
