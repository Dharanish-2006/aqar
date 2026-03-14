from django.contrib import admin
from .models import Document, InstitutionSettings


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display  = ['original_name', 'metric_id', 'extension', 'department', 'uploaded_at']
    list_filter   = ['extension', 'department']
    search_fields = ['original_name', 'metric_id', 'department__name']


@admin.register(InstitutionSettings)
class InstitutionSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'college_name', 'aqar_year', 'updated_at']