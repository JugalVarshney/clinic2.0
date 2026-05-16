from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DoctorViewSet, DrugViewSet, PrescriptionViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'drugs', DrugViewSet)
router.register(r'prescriptions', PrescriptionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]