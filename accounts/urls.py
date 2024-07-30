from django.urls import path
from .views import RegisterAPIView

urlpatterns = [
    path("signup/", RegisterAPIView.as_view()),
]
