from django.contrib import admin
from .models import Document, InstitutionSettings

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display  = ['original_name', 'metric_id', 'extension', 'user', 'uploaded_at']
    list_filter   = ['extension']
    search_fields = ['original_name', 'metric_id', 'user__username']


@admin.register(InstitutionSettings)
class InstitutionSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'college_name', 'aqar_year', 'updated_at']
