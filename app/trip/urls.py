from django.urls import path, include
from rest_framework.routers import DefaultRouter

from trip import views

router = DefaultRouter()
router.register('trips', views.TripViewSet)

app_name = 'trip'

urlpatterns = [
    path('', include(router.urls))
]
