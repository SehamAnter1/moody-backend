from django.contrib import admin

from .models import FAQ, Hero, HeroImage, Steps

# Register your models here.
class HeroImagesInline(admin.TabularInline):
    model = HeroImage
    extra = 1

@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', )
    search_fields = ('title',)
    inlines = [HeroImagesInline]
    
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', )
    search_fields = ('question',)

@admin.register(Steps)

class StepsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', )
    search_fields = ('title',)