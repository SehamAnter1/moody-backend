from django.shortcuts import render
from rest_framework import viewsets
from .models import FAQ, Hero
from .serializers import FAQSerializer, HeroSerializer
# Create your views here.
class HeroViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer   
    
class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer    