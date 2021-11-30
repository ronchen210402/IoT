from django.urls import path, re_path

from .views import FibonacciView, LogsView

urlpatterns = [
    path('fibonacci', FibonacciView.as_view()),
    path('logs', LogsView.as_view()),
]
