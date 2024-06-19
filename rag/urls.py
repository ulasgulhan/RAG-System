from django.urls import path
from .views import LlmView

urlpatterns = [
    path("llm/", LlmView.as_view(), name="llm-agent"),
]
