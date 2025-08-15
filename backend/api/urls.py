from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Model1ViewSet, Model2ViewSet, ContactViewSet, PublicAPIViewSet, AuthViewSet

router = DefaultRouter()
router.register(r'model1', Model1ViewSet, basename='model1')
router.register(r'model2', Model2ViewSet, basename='model2')
router.register(r'contact', ContactViewSet, basename='contact')
router.register(r'public', PublicAPIViewSet, basename='public')
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]
