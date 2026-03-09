from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from .models import (
    InstitutionSettings, Document,
    Metric_1_1, Metric_1_1_3, Metric_1_2_1, Metric_1_2_2_1_2_3,
    Metric_1_3_2, Metric_1_3_3,
    Metric_2_1, Metric_2_2, Metric_2_3, Metric_2_1_1, Metric_2_1_2,
    Metric_2_4_1_2_4_3, Metric_2_6_3,
    Metric_3_1, Metric_3_2, Metric_2_4_2_3_1_2_3_3_1,
    Metric_3_1_1_3_1_3, Metric_3_2_2, Metric_3_3_2, Metric_3_3_3,
    Metric_3_4_2, Metric_3_4_3_3_4_4, Metric_3_5_1, Metric_3_5_2,
    Metric_4_1_3, Metric_4_1_4_4_4_1, Metric_4_2_2_4_2_3,
    Metric_5_1_1_5_1_2, Metric_5_1_3, Metric_5_1_4,
    Metric_5_2_1, Metric_5_2_2, Metric_5_2_3, Metric_5_3_1, Metric_5_3_3,
    Metric_6_2_3, Metric_6_3_2, Metric_6_3_3, Metric_6_3_4,
    Metric_6_4_2, Metric_6_5_3,
)
from .serializers import (
    DocumentSerializer, DocumentUploadSerializer, InstitutionSettingsSerializer,
    Metric_1_1_Serializer, Metric_1_1_3_Serializer, Metric_1_2_1_Serializer,
    Metric_1_2_2_Serializer, Metric_1_3_2_Serializer, Metric_1_3_3_Serializer,
    Metric_2_1_Serializer, Metric_2_2_Serializer, Metric_2_3_Serializer,
    Metric_2_1_1_Serializer, Metric_2_1_2_Serializer, Metric_2_4_1_Serializer,
    Metric_2_6_3_Serializer,
    Metric_3_1_Serializer, Metric_3_2_Serializer, Metric_2_4_2_Serializer,
    Metric_3_1_1_Serializer, Metric_3_2_2_Serializer, Metric_3_3_2_Serializer,
    Metric_3_3_3_Serializer, Metric_3_4_2_Serializer, Metric_3_4_3_Serializer,
    Metric_3_5_1_Serializer, Metric_3_5_2_Serializer,
    Metric_4_1_3_Serializer, Metric_4_1_4_Serializer, Metric_4_2_2_Serializer,
    Metric_5_1_1_Serializer, Metric_5_1_3_Serializer, Metric_5_1_4_Serializer,
    Metric_5_2_1_Serializer, Metric_5_2_2_Serializer, Metric_5_2_3_Serializer,
    Metric_5_3_1_Serializer, Metric_5_3_3_Serializer,
    Metric_6_2_3_Serializer, Metric_6_3_2_Serializer, Metric_6_3_3_Serializer,
    Metric_6_3_4_Serializer, Metric_6_4_2_Serializer, Metric_6_5_3_Serializer,
)


# ── Generic base view ─────────────────────────────────────────────────────────
# All 41 metric endpoints share the same logic:
#   GET  /form/<slug>/       → list all rows for this user
#   POST /form/<slug>/       → create a new row
#   PUT  /form/<slug>/<id>/  → update a row
#   DELETE /form/<slug>/<id>/ → delete a row
#
# The frontend sends rows one at a time via POST (add) or PUT (edit).
# Bulk replace: POST /form/<slug>/bulk/ replaces ALL rows for this user.

class MetricView(APIView):
    permission_classes = [IsAuthenticated]
    model      = None   # set in subclass
    serializer = None   # set in subclass

    def get(self, request):
        qs = self.model.objects.filter(user=request.user)
        return Response(self.serializer(qs, many=True).data)

    def post(self, request):
        # Bulk replace: {"rows": [...]} replaces everything for this user
        if 'rows' in request.data:
            return self._bulk_replace(request)
        # Single row create
        s = self.serializer(data=request.data)
        if s.is_valid():
            s.save(user=request.user)
            return Response(s.data, status=201)
        return Response(s.errors, status=400)

    def _bulk_replace(self, request):
        rows = request.data.get('rows', [])
        if not isinstance(rows, list):
            return Response({'error': 'rows must be an array'}, status=400)

        # Delete all existing rows for this user then recreate
        self.model.objects.filter(user=request.user).delete()
        created = []
        errors  = []
        for i, row in enumerate(rows):
            # Strip frontend-only _id key before saving
            row_data = {k: v for k, v in row.items() if k != '_id'}
            s = self.serializer(data=row_data)
            if s.is_valid():
                obj = s.save(user=request.user)
                created.append(self.serializer(obj).data)
            else:
                errors.append({'row': i, 'errors': s.errors})

        if errors:
            return Response({'created': created, 'errors': errors}, status=207)
        return Response(created, status=201)


class MetricDetailView(APIView):
    permission_classes = [IsAuthenticated]
    model      = None
    serializer = None

    def put(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk, user=request.user)
        s = self.serializer(obj, data=request.data, partial=True)
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response(s.errors, status=400)

    def delete(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk, user=request.user)
        obj.delete()
        return Response(status=204)


# ── All-metrics summary (used by frontend on login) ───────────────────────────

# Maps metric_id → (Model, Serializer) for the bulk fetch endpoint
METRIC_REGISTRY = {
    '1.1':   (Metric_1_1,                Metric_1_1_Serializer),
    '1.1.3': (Metric_1_1_3,              Metric_1_1_3_Serializer),
    '1.2.1': (Metric_1_2_1,              Metric_1_2_1_Serializer),
    '1.2.2': (Metric_1_2_2_1_2_3,        Metric_1_2_2_Serializer),
    '1.3.2': (Metric_1_3_2,              Metric_1_3_2_Serializer),
    '1.3.3': (Metric_1_3_3,              Metric_1_3_3_Serializer),
    '2.1':   (Metric_2_1,                Metric_2_1_Serializer),
    '2.2':   (Metric_2_2,                Metric_2_2_Serializer),
    '2.3':   (Metric_2_3,                Metric_2_3_Serializer),
    '2.1.1': (Metric_2_1_1,              Metric_2_1_1_Serializer),
    '2.1.2': (Metric_2_1_2,              Metric_2_1_2_Serializer),
    '2.4.1': (Metric_2_4_1_2_4_3,        Metric_2_4_1_Serializer),
    '2.6.3': (Metric_2_6_3,              Metric_2_6_3_Serializer),
    '3.1':   (Metric_3_1,                Metric_3_1_Serializer),
    '3.2':   (Metric_3_2,                Metric_3_2_Serializer),
    '2.4.2': (Metric_2_4_2_3_1_2_3_3_1, Metric_2_4_2_Serializer),
    '3.1.1': (Metric_3_1_1_3_1_3,        Metric_3_1_1_Serializer),
    '3.2.2': (Metric_3_2_2,              Metric_3_2_2_Serializer),
    '3.3.2': (Metric_3_3_2,              Metric_3_3_2_Serializer),
    '3.3.3': (Metric_3_3_3,              Metric_3_3_3_Serializer),
    '3.4.2': (Metric_3_4_2,              Metric_3_4_2_Serializer),
    '3.4.3': (Metric_3_4_3_3_4_4,        Metric_3_4_3_Serializer),
    '3.5.1': (Metric_3_5_1,              Metric_3_5_1_Serializer),
    '3.5.2': (Metric_3_5_2,              Metric_3_5_2_Serializer),
    '4.1.3': (Metric_4_1_3,              Metric_4_1_3_Serializer),
    '4.1.4': (Metric_4_1_4_4_4_1,        Metric_4_1_4_Serializer),
    '4.2.2': (Metric_4_2_2_4_2_3,        Metric_4_2_2_Serializer),
    '5.1.1': (Metric_5_1_1_5_1_2,        Metric_5_1_1_Serializer),
    '5.1.3': (Metric_5_1_3,              Metric_5_1_3_Serializer),
    '5.1.4': (Metric_5_1_4,              Metric_5_1_4_Serializer),
    '5.2.1': (Metric_5_2_1,              Metric_5_2_1_Serializer),
    '5.2.2': (Metric_5_2_2,              Metric_5_2_2_Serializer),
    '5.2.3': (Metric_5_2_3,              Metric_5_2_3_Serializer),
    '5.3.1': (Metric_5_3_1,              Metric_5_3_1_Serializer),
    '5.3.3': (Metric_5_3_3,              Metric_5_3_3_Serializer),
    '6.2.3': (Metric_6_2_3,              Metric_6_2_3_Serializer),
    '6.3.2': (Metric_6_3_2,              Metric_6_3_2_Serializer),
    '6.3.3': (Metric_6_3_3,              Metric_6_3_3_Serializer),
    '6.3.4': (Metric_6_3_4,              Metric_6_3_4_Serializer),
    '6.4.2': (Metric_6_4_2,              Metric_6_4_2_Serializer),
    '6.5.3': (Metric_6_5_3,              Metric_6_5_3_Serializer),
}


class AllResponsesView(APIView):
    """
    GET /form/responses/
    Returns all rows for all 41 metrics in one shot.
    Shape: { "1.1": [...rows], "1.1.3": [...rows], ... }
    Frontend uses this to hydrate ResponseContext on login.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = {}
        for metric_id, (Model, Ser) in METRIC_REGISTRY.items():
            qs = Model.objects.filter(user=request.user)
            result[metric_id] = Ser(qs, many=True).data
        return Response(result)


# ── Criterion 1 ───────────────────────────────────────────────────────────────

class Metric_1_1_View(MetricView):
    model = Metric_1_1; serializer = Metric_1_1_Serializer

class Metric_1_1_DetailView(MetricDetailView):
    model = Metric_1_1; serializer = Metric_1_1_Serializer

class Metric_1_1_3_View(MetricView):
    model = Metric_1_1_3; serializer = Metric_1_1_3_Serializer

class Metric_1_1_3_DetailView(MetricDetailView):
    model = Metric_1_1_3; serializer = Metric_1_1_3_Serializer

class Metric_1_2_1_View(MetricView):
    model = Metric_1_2_1; serializer = Metric_1_2_1_Serializer

class Metric_1_2_1_DetailView(MetricDetailView):
    model = Metric_1_2_1; serializer = Metric_1_2_1_Serializer

class Metric_1_2_2_View(MetricView):
    model = Metric_1_2_2_1_2_3; serializer = Metric_1_2_2_Serializer

class Metric_1_2_2_DetailView(MetricDetailView):
    model = Metric_1_2_2_1_2_3; serializer = Metric_1_2_2_Serializer

class Metric_1_3_2_View(MetricView):
    model = Metric_1_3_2; serializer = Metric_1_3_2_Serializer

class Metric_1_3_2_DetailView(MetricDetailView):
    model = Metric_1_3_2; serializer = Metric_1_3_2_Serializer

class Metric_1_3_3_View(MetricView):
    model = Metric_1_3_3; serializer = Metric_1_3_3_Serializer

class Metric_1_3_3_DetailView(MetricDetailView):
    model = Metric_1_3_3; serializer = Metric_1_3_3_Serializer


# ── Criterion 2 ───────────────────────────────────────────────────────────────

class Metric_2_1_View(MetricView):
    model = Metric_2_1; serializer = Metric_2_1_Serializer

class Metric_2_1_DetailView(MetricDetailView):
    model = Metric_2_1; serializer = Metric_2_1_Serializer

class Metric_2_2_View(MetricView):
    model = Metric_2_2; serializer = Metric_2_2_Serializer

class Metric_2_2_DetailView(MetricDetailView):
    model = Metric_2_2; serializer = Metric_2_2_Serializer

class Metric_2_3_View(MetricView):
    model = Metric_2_3; serializer = Metric_2_3_Serializer

class Metric_2_3_DetailView(MetricDetailView):
    model = Metric_2_3; serializer = Metric_2_3_Serializer

class Metric_2_1_1_View(MetricView):
    model = Metric_2_1_1; serializer = Metric_2_1_1_Serializer

class Metric_2_1_1_DetailView(MetricDetailView):
    model = Metric_2_1_1; serializer = Metric_2_1_1_Serializer

class Metric_2_1_2_View(MetricView):
    model = Metric_2_1_2; serializer = Metric_2_1_2_Serializer

class Metric_2_1_2_DetailView(MetricDetailView):
    model = Metric_2_1_2; serializer = Metric_2_1_2_Serializer

class Metric_2_4_1_View(MetricView):
    model = Metric_2_4_1_2_4_3; serializer = Metric_2_4_1_Serializer

class Metric_2_4_1_DetailView(MetricDetailView):
    model = Metric_2_4_1_2_4_3; serializer = Metric_2_4_1_Serializer

class Metric_2_6_3_View(MetricView):
    model = Metric_2_6_3; serializer = Metric_2_6_3_Serializer

class Metric_2_6_3_DetailView(MetricDetailView):
    model = Metric_2_6_3; serializer = Metric_2_6_3_Serializer


# ── Criterion 3 ───────────────────────────────────────────────────────────────

class Metric_3_1_View(MetricView):
    model = Metric_3_1; serializer = Metric_3_1_Serializer

class Metric_3_1_DetailView(MetricDetailView):
    model = Metric_3_1; serializer = Metric_3_1_Serializer

class Metric_3_2_View(MetricView):
    model = Metric_3_2; serializer = Metric_3_2_Serializer

class Metric_3_2_DetailView(MetricDetailView):
    model = Metric_3_2; serializer = Metric_3_2_Serializer

class Metric_2_4_2_View(MetricView):
    model = Metric_2_4_2_3_1_2_3_3_1; serializer = Metric_2_4_2_Serializer

class Metric_2_4_2_DetailView(MetricDetailView):
    model = Metric_2_4_2_3_1_2_3_3_1; serializer = Metric_2_4_2_Serializer

class Metric_3_1_1_View(MetricView):
    model = Metric_3_1_1_3_1_3; serializer = Metric_3_1_1_Serializer

class Metric_3_1_1_DetailView(MetricDetailView):
    model = Metric_3_1_1_3_1_3; serializer = Metric_3_1_1_Serializer

class Metric_3_2_2_View(MetricView):
    model = Metric_3_2_2; serializer = Metric_3_2_2_Serializer

class Metric_3_2_2_DetailView(MetricDetailView):
    model = Metric_3_2_2; serializer = Metric_3_2_2_Serializer

class Metric_3_3_2_View(MetricView):
    model = Metric_3_3_2; serializer = Metric_3_3_2_Serializer

class Metric_3_3_2_DetailView(MetricDetailView):
    model = Metric_3_3_2; serializer = Metric_3_3_2_Serializer

class Metric_3_3_3_View(MetricView):
    model = Metric_3_3_3; serializer = Metric_3_3_3_Serializer

class Metric_3_3_3_DetailView(MetricDetailView):
    model = Metric_3_3_3; serializer = Metric_3_3_3_Serializer

class Metric_3_4_2_View(MetricView):
    model = Metric_3_4_2; serializer = Metric_3_4_2_Serializer

class Metric_3_4_2_DetailView(MetricDetailView):
    model = Metric_3_4_2; serializer = Metric_3_4_2_Serializer

class Metric_3_4_3_View(MetricView):
    model = Metric_3_4_3_3_4_4; serializer = Metric_3_4_3_Serializer

class Metric_3_4_3_DetailView(MetricDetailView):
    model = Metric_3_4_3_3_4_4; serializer = Metric_3_4_3_Serializer

class Metric_3_5_1_View(MetricView):
    model = Metric_3_5_1; serializer = Metric_3_5_1_Serializer

class Metric_3_5_1_DetailView(MetricDetailView):
    model = Metric_3_5_1; serializer = Metric_3_5_1_Serializer

class Metric_3_5_2_View(MetricView):
    model = Metric_3_5_2; serializer = Metric_3_5_2_Serializer

class Metric_3_5_2_DetailView(MetricDetailView):
    model = Metric_3_5_2; serializer = Metric_3_5_2_Serializer


# ── Criterion 4 ───────────────────────────────────────────────────────────────

class Metric_4_1_3_View(MetricView):
    model = Metric_4_1_3; serializer = Metric_4_1_3_Serializer

class Metric_4_1_3_DetailView(MetricDetailView):
    model = Metric_4_1_3; serializer = Metric_4_1_3_Serializer

class Metric_4_1_4_View(MetricView):
    model = Metric_4_1_4_4_4_1; serializer = Metric_4_1_4_Serializer

class Metric_4_1_4_DetailView(MetricDetailView):
    model = Metric_4_1_4_4_4_1; serializer = Metric_4_1_4_Serializer

class Metric_4_2_2_View(MetricView):
    model = Metric_4_2_2_4_2_3; serializer = Metric_4_2_2_Serializer

class Metric_4_2_2_DetailView(MetricDetailView):
    model = Metric_4_2_2_4_2_3; serializer = Metric_4_2_2_Serializer


# ── Criterion 5 ───────────────────────────────────────────────────────────────

class Metric_5_1_1_View(MetricView):
    model = Metric_5_1_1_5_1_2; serializer = Metric_5_1_1_Serializer

class Metric_5_1_1_DetailView(MetricDetailView):
    model = Metric_5_1_1_5_1_2; serializer = Metric_5_1_1_Serializer

class Metric_5_1_3_View(MetricView):
    model = Metric_5_1_3; serializer = Metric_5_1_3_Serializer

class Metric_5_1_3_DetailView(MetricDetailView):
    model = Metric_5_1_3; serializer = Metric_5_1_3_Serializer

class Metric_5_1_4_View(MetricView):
    model = Metric_5_1_4; serializer = Metric_5_1_4_Serializer

class Metric_5_1_4_DetailView(MetricDetailView):
    model = Metric_5_1_4; serializer = Metric_5_1_4_Serializer

class Metric_5_2_1_View(MetricView):
    model = Metric_5_2_1; serializer = Metric_5_2_1_Serializer

class Metric_5_2_1_DetailView(MetricDetailView):
    model = Metric_5_2_1; serializer = Metric_5_2_1_Serializer

class Metric_5_2_2_View(MetricView):
    model = Metric_5_2_2; serializer = Metric_5_2_2_Serializer

class Metric_5_2_2_DetailView(MetricDetailView):
    model = Metric_5_2_2; serializer = Metric_5_2_2_Serializer

class Metric_5_2_3_View(MetricView):
    model = Metric_5_2_3; serializer = Metric_5_2_3_Serializer

class Metric_5_2_3_DetailView(MetricDetailView):
    model = Metric_5_2_3; serializer = Metric_5_2_3_Serializer

class Metric_5_3_1_View(MetricView):
    model = Metric_5_3_1; serializer = Metric_5_3_1_Serializer

class Metric_5_3_1_DetailView(MetricDetailView):
    model = Metric_5_3_1; serializer = Metric_5_3_1_Serializer

class Metric_5_3_3_View(MetricView):
    model = Metric_5_3_3; serializer = Metric_5_3_3_Serializer

class Metric_5_3_3_DetailView(MetricDetailView):
    model = Metric_5_3_3; serializer = Metric_5_3_3_Serializer


# ── Criterion 6 ───────────────────────────────────────────────────────────────

class Metric_6_2_3_View(MetricView):
    model = Metric_6_2_3; serializer = Metric_6_2_3_Serializer

class Metric_6_2_3_DetailView(MetricDetailView):
    model = Metric_6_2_3; serializer = Metric_6_2_3_Serializer

class Metric_6_3_2_View(MetricView):
    model = Metric_6_3_2; serializer = Metric_6_3_2_Serializer

class Metric_6_3_2_DetailView(MetricDetailView):
    model = Metric_6_3_2; serializer = Metric_6_3_2_Serializer

class Metric_6_3_3_View(MetricView):
    model = Metric_6_3_3; serializer = Metric_6_3_3_Serializer

class Metric_6_3_3_DetailView(MetricDetailView):
    model = Metric_6_3_3; serializer = Metric_6_3_3_Serializer

class Metric_6_3_4_View(MetricView):
    model = Metric_6_3_4; serializer = Metric_6_3_4_Serializer

class Metric_6_3_4_DetailView(MetricDetailView):
    model = Metric_6_3_4; serializer = Metric_6_3_4_Serializer

class Metric_6_4_2_View(MetricView):
    model = Metric_6_4_2; serializer = Metric_6_4_2_Serializer

class Metric_6_4_2_DetailView(MetricDetailView):
    model = Metric_6_4_2; serializer = Metric_6_4_2_Serializer

class Metric_6_5_3_View(MetricView):
    model = Metric_6_5_3; serializer = Metric_6_5_3_Serializer

class Metric_6_5_3_DetailView(MetricDetailView):
    model = Metric_6_5_3; serializer = Metric_6_5_3_Serializer


# ── Documents ─────────────────────────────────────────────────────────────────

class DocumentUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        s = DocumentUploadSerializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors, status=400)
        metric_id = s.validated_data['metric_id']
        file      = s.validated_data['file']
        ext       = file.name.rsplit('.', 1)[-1].lower()
        doc = Document.objects.create(
            user=request.user,
            metric_id=metric_id,
            file=file,
            original_name=file.name,
            file_size=file.size,
            extension=ext,
        )
        return Response(DocumentSerializer(doc, context={'request': request}).data, status=201)


class DocumentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, doc_id):
        doc = get_object_or_404(Document, id=doc_id, user=request.user)
        doc.file.delete(save=False)
        doc.delete()
        return Response(status=204)


class DocumentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, metric_id):
        docs = Document.objects.filter(user=request.user, metric_id=metric_id)
        return Response(DocumentSerializer(docs, many=True, context={'request': request}).data)


# ── Settings ──────────────────────────────────────────────────────────────────

class InstitutionSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        obj, _ = InstitutionSettings.objects.get_or_create(user=request.user)
        return Response(InstitutionSettingsSerializer(obj).data)

    def post(self, request):
        obj, _ = InstitutionSettings.objects.get_or_create(user=request.user)
        s = InstitutionSettingsSerializer(obj, data=request.data, partial=True)
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response(s.errors, status=400)


# ── Completion summary ────────────────────────────────────────────────────────

class CompletionStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        completed = []
        for metric_id, (Model, _) in METRIC_REGISTRY.items():
            if Model.objects.filter(user=request.user).exists():
                completed.append(metric_id)
        return Response({
            'completed_metric_ids': completed,
            'total_completed': len(completed),
            'total_metrics': len(METRIC_REGISTRY),
            'total_documents': Document.objects.filter(user=request.user).count(),
        })