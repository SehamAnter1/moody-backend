
from os import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FAQViewSet, HeroViewSet, PrivacyPolicyViewSet, StepsViewSet, TermsOfServiceViewSet

router = DefaultRouter()
router.register(r'hero', HeroViewSet, basename='hero')
router.register(r'faq', FAQViewSet, basename='faq')
router.register(r'steps', StepsViewSet, basename='steps')
router.register(r'privacy-policy', PrivacyPolicyViewSet, basename='privacy-policy')
router.register(r'terms-of-service', TermsOfServiceViewSet, basename='terms-of-service')
urlpatterns = [
    path('', include(router.urls)),
    
]