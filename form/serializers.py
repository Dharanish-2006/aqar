from rest_framework import serializers
from .models import MetricResponse, Document, InstitutionSettings


class DocumentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model  = Document
        fields = ['id', 'metric_id', 'original_name', 'file_size', 'extension', 'uploaded_at', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class MetricResponseSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model  = MetricResponse
        fields = ['id', 'metric_id', 'metric_type', 'text', 'numeric_data', 'saved', 'updated_at', 'documents']
        read_only_fields = ['id', 'updated_at', 'documents']

    def validate_numeric_data(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Must be a JSON object.")
        for year, val in value.items():
            if val not in ('', None):
                try:
                    if float(val) < 0:
                        raise serializers.ValidationError(f"Negative value not allowed for {year}.")
                except (ValueError, TypeError):
                    raise serializers.ValidationError(f"Invalid number for {year}: {val}")
        return value


class DocumentUploadSerializer(serializers.Serializer):
    metric_id = serializers.CharField(max_length=20)
    file      = serializers.FileField()

    def validate_file(self, value):
        ALLOWED = ['pdf', 'docx', 'xlsx']
        MAX     = 10 * 1024 * 1024
        ext     = value.name.rsplit('.', 1)[-1].lower() if '.' in value.name else ''
        if ext not in ALLOWED:
            raise serializers.ValidationError(f"'.{ext}' not allowed. Use PDF, DOCX or XLSX.")
        if value.size > MAX:
            raise serializers.ValidationError("File exceeds 10 MB limit.")
        return value


class InstitutionSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model  = InstitutionSettings
        fields = ['college_name', 'aqar_year', 'updated_at']
        read_only_fields = ['updated_at']
