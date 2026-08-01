from django.urls import path

from .views import UpdateMarketsView

urlpatterns = [
    path("update/", UpdateMarketsView.as_view()),
]