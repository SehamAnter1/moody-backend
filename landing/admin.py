from django.contrib import admin

from .models import Hero, HeroImage

# Register your models here.
class HeroImagesInline(admin.TabularInline):
    model = HeroImage
    extra = 1

@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', )
    search_fields = ('title',)
    inlines = [HeroImagesInline]
    
