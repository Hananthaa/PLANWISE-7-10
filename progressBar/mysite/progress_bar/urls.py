from django.urls import path
from progress_bar import views

urlpatterns = [
    path("", views.test, name="test"),
]