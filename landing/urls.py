
from os import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FAQViewSet, HeroViewSet, StepsViewSet

router = DefaultRouter()
router.register(r'hero', HeroViewSet, basename='hero')
router.register(r'faq', FAQViewSet, basename='faq')
router.register(r'steps', StepsViewSet, basename='steps')
urlpatterns = [
    path('', include(router.urls)),
    
]