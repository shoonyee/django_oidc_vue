from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Model1ViewSet, Model2ViewSet, ContactViewSet, PublicAPIViewSet, AuthViewSet

router = DefaultRouter()
router.register(r'model1', Model1ViewSet)
router.register(r'model2', Model2ViewSet)
router.register(r'contact', ContactViewSet)
router.register(r'public', PublicAPIViewSet, basename='public')
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]
