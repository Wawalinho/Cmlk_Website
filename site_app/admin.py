
from django.contrib import admin
from .models import Actualite

@admin.register(Actualite)
class ActualiteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_publication')
    search_fields = ('titre',)
    list_filter = ('date_publication',)

    
