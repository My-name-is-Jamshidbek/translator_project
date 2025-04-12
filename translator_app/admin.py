# translator_app/admin.py

from django.contrib import admin
from .models import Translation

@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ('uz_word', 'kh_word', 'description')
    search_fields = ('uz_word', 'kh_word', 'description')
