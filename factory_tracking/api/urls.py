from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'machine', views.MachineViewSet)
router.register(r'warning', views.WarningViewSet)
router.register(r'faultcase', views.FaultCaseViewSet)
router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
