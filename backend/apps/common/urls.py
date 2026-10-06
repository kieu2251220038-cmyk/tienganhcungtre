from django.urls import path

from . import views


urlpatterns = [
    path('health/', views.health_check, name='health-check'),
    path('health/db/', views.database_health_check, name='database-health-check'),
]