from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from .models import MetricResponse, Document, InstitutionSettings
from .serializers import *



class AllResponsesView(APIView):
    """GET /form/responses/  →  all saved responses for this user"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = MetricResponse.objects.filter(user=request.user).prefetch_related('documents')
        return Response(MetricResponseSerializer(qs, many=True, context={'request': request}).data)


class SaveResponseView(APIView):
    """POST /form/response/save/  →  create or update a metric response"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        metric_id = request.data.get('metric_id')
        if not metric_id:
            return Response({'error': 'metric_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        instance, created = MetricResponse.objects.get_or_create(
            user=request.user,
            metric_id=metric_id,
            defaults={'metric_type': request.data.get('metric_type', 'QlM')}
        )

        serializer = MetricResponseSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleResponseView(APIView):
    """
    GET    /form/response/<metric_id>/
    DELETE /form/response/<metric_id>/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, metric_id):
        obj = get_object_or_404(MetricResponse, user=request.user, metric_id=metric_id)
        return Response(MetricResponseSerializer(obj, context={'request': request}).data)

    def delete(self, request, metric_id):
        obj = get_object_or_404(MetricResponse, user=request.user, metric_id=metric_id)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class DocumentUploadView(APIView):
    """POST /form/document/upload/  →  upload a supporting file"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = DocumentUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        metric_id = serializer.validated_data['metric_id']
        file      = serializer.validated_data['file']
        ext       = file.name.rsplit('.', 1)[-1].lower()

        metric_response = MetricResponse.objects.filter(
            user=request.user, metric_id=metric_id
        ).first()

        doc = Document.objects.create(
            user=request.user,
            metric_response=metric_response,
            metric_id=metric_id,
            file=file,
            original_name=file.name,
            file_size=file.size,
            extension=ext,
        )
        return Response(DocumentSerializer(doc, context={'request': request}).data, status=status.HTTP_201_CREATED)


class DocumentListView(APIView):
    """GET /form/documents/<metric_id>/  →  list docs for one metric"""
    permission_classes = [IsAuthenticated]

    def get(self, request, metric_id):
        docs = Document.objects.filter(user=request.user, metric_id=metric_id)
        return Response(DocumentSerializer(docs, many=True, context={'request': request}).data)


class DocumentDeleteView(APIView):
    """DELETE /form/document/<doc_id>/  →  delete one document"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, doc_id):
        doc = get_object_or_404(Document, id=doc_id, user=request.user)
        doc.file.delete(save=False)   # remove the physical file too
        doc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class InstitutionSettingsView(APIView):
    """
    GET  /form/settings/
    POST /form/settings/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        obj, _ = InstitutionSettings.objects.get_or_create(user=request.user)
        return Response(InstitutionSettingsSerializer(obj).data)

    def post(self, request):
        obj, _ = InstitutionSettings.objects.get_or_create(user=request.user)
        serializer = InstitutionSettingsSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CompletionStatusView(APIView):
    """GET /form/completion/  →  which metric IDs are fully complete"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        responses = MetricResponse.objects.filter(user=request.user)
        completed = []

        for r in responses:
            if r.metric_type == 'QlM':
                words = len(r.text.split()) if r.text else 0
                if 100 <= words <= 200:
                    completed.append(r.metric_id)
            else:
                vals = [v for v in r.numeric_data.values() if v not in ('', None)]
                if vals:
                    completed.append(r.metric_id)

        return Response({
            'completed_metric_ids': completed,
            'total_completed': len(completed),
            'total_documents': Document.objects.filter(user=request.user).count(),
        })
