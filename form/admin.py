from django.contrib import admin
from .models import MetricResponse, Document, InstitutionSettings


@admin.register(MetricResponse)
class MetricResponseAdmin(admin.ModelAdmin):
    list_display  = ['metric_id', 'metric_type', 'user', 'saved', 'updated_at']
    list_filter   = ['metric_type', 'saved']
    search_fields = ['metric_id', 'user__username']
    ordering      = ['metric_id']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display  = ['original_name', 'metric_id', 'extension', 'user', 'uploaded_at']
    list_filter   = ['extension']
    search_fields = ['original_name', 'metric_id', 'user__username']


@admin.register(InstitutionSettings)
class InstitutionSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'college_name', 'aqar_year', 'updated_at']
