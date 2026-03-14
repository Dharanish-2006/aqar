from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .models import *
from .serializers import *
from authentication.models import UserProfile



def get_profile(user):
    try:
        return user.profile
    except UserProfile.DoesNotExist:
        return None


def is_admin(user):
    p = get_profile(user)
    return p and p.role == 'admin'


def get_hod_department(user):
    p = get_profile(user)
    if p and p.role == 'hod' and p.department:
        return p.department
    return None


def is_submitted(department):
    try:
        return department.submission.is_submitted
    except SubmissionStatus.DoesNotExist:
        return False



METRIC_REGISTRY = {
    '1.1':   (Metric_1_1,               Metric_1_1_Serializer),
    '1.1.3': (Metric_1_1_3,             Metric_1_1_3_Serializer),
    '1.2.1': (Metric_1_2_1,             Metric_1_2_1_Serializer),
    '1.2.2': (Metric_1_2_2_1_2_3,       Metric_1_2_2_Serializer),
    '1.3.2': (Metric_1_3_2,             Metric_1_3_2_Serializer),
    '1.3.3': (Metric_1_3_3,             Metric_1_3_3_Serializer),
    '2.1':   (Metric_2_1,               Metric_2_1_Serializer),
    '2.2':   (Metric_2_2,               Metric_2_2_Serializer),
    '2.3':   (Metric_2_3,               Metric_2_3_Serializer),
    '2.1.1': (Metric_2_1_1,             Metric_2_1_1_Serializer),
    '2.1.2': (Metric_2_1_2,             Metric_2_1_2_Serializer),
    '2.4.1': (Metric_2_4_1_2_4_3,       Metric_2_4_1_Serializer),
    '2.6.3': (Metric_2_6_3,             Metric_2_6_3_Serializer),
    '2.4.2': (Metric_2_4_2_3_1_2_3_3_1, Metric_2_4_2_Serializer),
    '3.1':   (Metric_3_1,               Metric_3_1_Serializer),
    '3.2':   (Metric_3_2,               Metric_3_2_Serializer),
    '3.1.1': (Metric_3_1_1_3_1_3,       Metric_3_1_1_Serializer),
    '3.2.2': (Metric_3_2_2,             Metric_3_2_2_Serializer),
    '3.3.2': (Metric_3_3_2,             Metric_3_3_2_Serializer),
    '3.3.3': (Metric_3_3_3,             Metric_3_3_3_Serializer),
    '3.4.2': (Metric_3_4_2,             Metric_3_4_2_Serializer),
    '3.4.3': (Metric_3_4_3_3_4_4,       Metric_3_4_3_Serializer),
    '3.5.1': (Metric_3_5_1,             Metric_3_5_1_Serializer),
    '3.5.2': (Metric_3_5_2,             Metric_3_5_2_Serializer),
    '4.1.3': (Metric_4_1_3,             Metric_4_1_3_Serializer),
    '4.1.4': (Metric_4_1_4_4_4_1,       Metric_4_1_4_Serializer),
    '4.2.2': (Metric_4_2_2_4_2_3,       Metric_4_2_2_Serializer),
    '5.1.1': (Metric_5_1_1_5_1_2,       Metric_5_1_1_Serializer),
    '5.1.3': (Metric_5_1_3,             Metric_5_1_3_Serializer),
    '5.1.4': (Metric_5_1_4,             Metric_5_1_4_Serializer),
    '5.2.1': (Metric_5_2_1,             Metric_5_2_1_Serializer),
    '5.2.2': (Metric_5_2_2,             Metric_5_2_2_Serializer),
    '5.2.3': (Metric_5_2_3,             Metric_5_2_3_Serializer),
    '5.3.1': (Metric_5_3_1,             Metric_5_3_1_Serializer),
    '5.3.3': (Metric_5_3_3,             Metric_5_3_3_Serializer),
    '6.2.3': (Metric_6_2_3,             Metric_6_2_3_Serializer),
    '6.3.2': (Metric_6_3_2,             Metric_6_3_2_Serializer),
    '6.3.3': (Metric_6_3_3,             Metric_6_3_3_Serializer),
    '6.3.4': (Metric_6_3_4,             Metric_6_3_4_Serializer),
    '6.4.2': (Metric_6_4_2,             Metric_6_4_2_Serializer),
    '6.5.3': (Metric_6_5_3,             Metric_6_5_3_Serializer),
}



class MetricView(APIView):
    permission_classes = [IsAuthenticated]
    model      = None
    serializer = None

    def _get_dept(self, request):
        dept = get_hod_department(request.user)
        if not dept:
            return None, Response({'error': 'No department assigned'}, status=403)
        return dept, None

    def get(self, request):
        dept, err = self._get_dept(request)
        if err: return err
        qs = self.model.objects.filter(department=dept)
        return Response(self.serializer(qs, many=True).data)

    def post(self, request):
        dept, err = self._get_dept(request)
        if err: return err
        if is_submitted(dept):
            return Response({'error': 'Data is locked — already submitted to admin.'}, status=403)
        if 'rows' in request.data:
            return self._bulk_replace(request, dept)
        s = self.serializer(data=request.data)
        if s.is_valid():
            s.save(department=dept)
            return Response(s.data, status=201)
        return Response(s.errors, status=400)

    def _bulk_replace(self, request, dept):
        rows = request.data.get('rows', [])
        if not isinstance(rows, list):
            return Response({'error': 'rows must be an array'}, status=400)
        self.model.objects.filter(department=dept).delete()
        created, errors = [], []
        for i, row in enumerate(rows):
            row_data = {k: v for k, v in row.items() if k != '_id'}
            s = self.serializer(data=row_data)
            if s.is_valid():
                obj = s.save(department=dept)
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
        dept = get_hod_department(request.user)
        admin = is_admin(request.user)
        if not dept and not admin:
            return Response({'error': 'Forbidden'}, status=403)
        if dept and is_submitted(dept):
            return Response({'error': 'Data is locked — already submitted.'}, status=403)
        filter_kwargs = {'pk': pk}
        if dept:
            filter_kwargs['department'] = dept
        obj = get_object_or_404(self.model, **filter_kwargs)
        s = self.serializer(obj, data=request.data, partial=True)
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response(s.errors, status=400)

    def delete(self, request, pk):
        dept = get_hod_department(request.user)
        admin = is_admin(request.user)
        if not dept and not admin:
            return Response({'error': 'Forbidden'}, status=403)
        if dept and is_submitted(dept):
            return Response({'error': 'Data is locked — already submitted.'}, status=403)
        filter_kwargs = {'pk': pk}
        if dept:
            filter_kwargs['department'] = dept
        obj = get_object_or_404(self.model, **filter_kwargs)
        obj.delete()
        return Response(status=204)



class AllResponsesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dept = get_hod_department(request.user)
        if not dept:
            return Response({'error': 'No department assigned'}, status=403)
        result = {}
        for metric_id, (Model, Ser) in METRIC_REGISTRY.items():
            qs = Model.objects.filter(department=dept)
            result[metric_id] = Ser(qs, many=True).data
        return Response(result)



class SubmitView(APIView):
    """HOD submits all data — locks editing."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        dept = get_hod_department(request.user)
        if not dept:
            return Response({'error': 'No department assigned'}, status=403)
        status_obj, _ = SubmissionStatus.objects.get_or_create(department=dept)
        if status_obj.is_submitted:
            return Response({'error': 'Already submitted'}, status=400)
        status_obj.is_submitted = True
        status_obj.submitted_at = timezone.now()
        status_obj.save()
        return Response({'message': 'Data submitted successfully', 'submitted_at': status_obj.submitted_at})


class SubmissionStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dept = get_hod_department(request.user)
        if not dept:
            # Admin — return all depts submission status
            if is_admin(request.user):
                from .models import Department
                depts = Department.objects.all()
                result = []
                for d in depts:
                    try:
                        sub = d.submission
                        submitted = sub.is_submitted
                        submitted_at = sub.submitted_at
                    except SubmissionStatus.DoesNotExist:
                        submitted = False
                        submitted_at = None
                    result.append({
                        'department_id': d.id,
                        'department': str(d),
                        'is_submitted': submitted,
                        'submitted_at': submitted_at,
                    })
                return Response(result)
            return Response({'error': 'No department assigned'}, status=403)
        try:
            sub = dept.submission
            return Response(SubmissionStatusSerializer(sub).data)
        except SubmissionStatus.DoesNotExist:
            return Response({'is_submitted': False, 'submitted_at': None})



class AdminOnly(APIView):
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        resp = super().dispatch(request, *args, **kwargs)
        return resp

    def check_admin(self, request):
        if not is_admin(request.user):
            return Response({'error': 'Admin access required'}, status=403)
        return None


class DepartmentListView(AdminOnly):
    def get(self, request):
        err = self.check_admin(request)
        if err: return err
        depts = Department.objects.all()
        return Response(DepartmentSerializer(depts, many=True).data)

    def post(self, request):
        err = self.check_admin(request)
        if err: return err
        s = DepartmentSerializer(data=request.data)
        if s.is_valid():
            dept = s.save()
            SubmissionStatus.objects.get_or_create(department=dept)
            return Response(DepartmentSerializer(dept).data, status=201)
        return Response(s.errors, status=400)


class DepartmentDetailView(AdminOnly):
    def get(self, request, pk):
        err = self.check_admin(request)
        if err: return err
        dept = get_object_or_404(Department, pk=pk)
        return Response(DepartmentDetailSerializer(dept).data)

    def put(self, request, pk):
        err = self.check_admin(request)
        if err: return err
        dept = get_object_or_404(Department, pk=pk)
        s = DepartmentSerializer(dept, data=request.data, partial=True)
        if s.is_valid():
            s.save()
            return Response(DepartmentSerializer(dept).data)
        return Response(s.errors, status=400)

    def delete(self, request, pk):
        err = self.check_admin(request)
        if err: return err
        dept = get_object_or_404(Department, pk=pk)
        try:
            from authentication.models import UserProfile
            import traceback
            UserProfile.objects.filter(department=dept).update(department=None)

            Department.objects.filter(pk=pk).update(hod=None)
            dept.refresh_from_db()

            dept.delete()

            return Response(status=204)

        except Exception as e:
            import traceback as tb_module
            return Response(
                {'error': str(e), 'traceback': tb_module.format_exc()},
                status=500
            )

class HODCreateView(AdminOnly):
    """Admin creates a HOD account and links it to a department."""

    def post(self, request):
        err = self.check_admin(request)
        if err: return err

        username    = request.data.get('username')
        password    = request.data.get('password')
        email       = request.data.get('email', '')
        dept_id     = request.data.get('department_id')

        if not all([username, password, dept_id]):
            return Response({'error': 'username, password, and department_id are required'}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=400)

        dept = get_object_or_404(Department, pk=dept_id)

        # Prevent two HODs for the same department
        if UserProfile.objects.filter(department=dept).exists():
            return Response({'error': 'This department already has a HOD account'}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        profile = UserProfile.objects.create(user=user, role='hod', department=dept)
        dept.hod = user
        dept.save()

        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'department': str(dept),
            'department_id': dept.id,
        }, status=201)

    def get(self, request):
        """List all HOD accounts."""
        err = self.check_admin(request)
        if err: return err
        profiles = UserProfile.objects.filter(role='hod').select_related('user', 'department')
        data = [{
            'id': p.user.id,
            'username': p.user.username,
            'email': p.user.email,
            'department': str(p.department) if p.department else None,
            'department_id': p.department.id if p.department else None,
        } for p in profiles]
        return Response(data)


class HODDeleteView(AdminOnly):
    def delete(self, request, pk):
        err = self.check_admin(request)
        if err: return err
        user = get_object_or_404(User, pk=pk)
        try:
            profile = user.profile
            if profile.role != 'hod':
                return Response({'error': 'User is not a HOD'}, status=400)
            if profile.department:
                profile.department.hod = None
                profile.department.save()
        except UserProfile.DoesNotExist:
            pass
        user.delete()
        return Response(status=204)


# ── Admin: Read/Edit any department's metric data ─────────────────────────────

class AdminDepartmentResponsesView(AdminOnly):
    """GET all 41 metrics for a specific department."""

    def get(self, request, dept_id):
        err = self.check_admin(request)
        if err: return err
        dept = get_object_or_404(Department, pk=dept_id)
        result = {}
        for metric_id, (Model, Ser) in METRIC_REGISTRY.items():
            qs = Model.objects.filter(department=dept)
            result[metric_id] = Ser(qs, many=True).data
        return Response(result)


class AdminMetricSaveView(AdminOnly):
    """POST bulk rows for a specific department's metric (admin can always edit)."""

    def post(self, request, dept_id, metric_slug):
        err = self.check_admin(request)
        if err: return err
        dept = get_object_or_404(Department, pk=dept_id)
        metric_id = metric_slug.replace('-', '.')
        if metric_id not in METRIC_REGISTRY:
            return Response({'error': 'Unknown metric'}, status=404)
        Model, Ser = METRIC_REGISTRY[metric_id]
        rows = request.data.get('rows', [])
        Model.objects.filter(department=dept).delete()
        created, errors = [], []
        for i, row in enumerate(rows):
            row_data = {k: v for k, v in row.items() if k != '_id'}
            s = Ser(data=row_data)
            if s.is_valid():
                obj = s.save(department=dept)
                created.append(Ser(obj).data)
            else:
                errors.append({'row': i, 'errors': s.errors})
        if errors:
            return Response({'created': created, 'errors': errors}, status=207)
        return Response(created, status=201)


class AdminUnlockView(AdminOnly):
    """Admin can unlock a submitted department (reopen for editing)."""

    def post(self, request, dept_id):
        err = self.check_admin(request)
        if err: return err
        dept = get_object_or_404(Department, pk=dept_id)
        try:
            sub = dept.submission
            sub.is_submitted = False
            sub.submitted_at = None
            sub.save()
        except SubmissionStatus.DoesNotExist:
            pass
        return Response({'message': 'Department unlocked for editing'})
class DocumentUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        dept = get_hod_department(request.user)
        if not dept:
            return Response({'error': 'No department assigned'}, status=403)
        if is_submitted(dept):
            return Response({'error': 'Data is locked — already submitted.'}, status=403)
        s = DocumentUploadSerializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors, status=400)
        metric_id = s.validated_data['metric_id']
        file      = s.validated_data['file']
        ext       = file.name.rsplit('.', 1)[-1].lower()
        doc = Document.objects.create(
            department=dept,
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
        dept = get_hod_department(request.user)
        admin = is_admin(request.user)
        if not dept and not admin:
            return Response({'error': 'Forbidden'}, status=403)
        if dept and is_submitted(dept):
            return Response({'error': 'Data is locked.'}, status=403)
        filter_kwargs = {'id': doc_id}
        if dept:
            filter_kwargs['department'] = dept
        doc = get_object_or_404(Document, **filter_kwargs)
        doc.file.delete(save=False)
        doc.delete()
        return Response(status=204)
class DocumentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, metric_id):
        dept = get_hod_department(request.user)
        if not dept:
            return Response({'error': 'No department assigned'}, status=403)
        docs = Document.objects.filter(department=dept, metric_id=metric_id)
        return Response(DocumentSerializer(docs, many=True, context={'request': request}).data)
class InstitutionSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        target_user = request.user
        if not is_admin(request.user):
            from django.contrib.auth.models import User as DjUser
            admin_profiles = UserProfile.objects.filter(role='admin')
            if admin_profiles.exists():
                target_user = admin_profiles.first().user
        obj, _ = InstitutionSettings.objects.get_or_create(user=target_user)
        return Response(InstitutionSettingsSerializer(obj).data)

    def post(self, request):
        if not is_admin(request.user):
            return Response({'error': 'Only admin can update settings'}, status=403)
        obj, _ = InstitutionSettings.objects.get_or_create(user=request.user)
        s = InstitutionSettingsSerializer(obj, data=request.data, partial=True)
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response(s.errors, status=400)
class CompletionStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dept = get_hod_department(request.user)
        if not dept:
            return Response({'error': 'No department assigned'}, status=403)
        completed = []
        for metric_id, (Model, _) in METRIC_REGISTRY.items():
            if Model.objects.filter(department=dept).exists():
                completed.append(metric_id)
        return Response({
            'completed_metric_ids': completed,
            'total_completed': len(completed),
            'total_metrics': len(METRIC_REGISTRY),
            'total_documents': Document.objects.filter(department=dept).count(),
        })
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

class Metric_2_4_2_View(MetricView):
    model = Metric_2_4_2_3_1_2_3_3_1; serializer = Metric_2_4_2_Serializer
class Metric_2_4_2_DetailView(MetricDetailView):
    model = Metric_2_4_2_3_1_2_3_3_1; serializer = Metric_2_4_2_Serializer

class Metric_3_1_View(MetricView):
    model = Metric_3_1; serializer = Metric_3_1_Serializer
class Metric_3_1_DetailView(MetricDetailView):
    model = Metric_3_1; serializer = Metric_3_1_Serializer

class Metric_3_2_View(MetricView):
    model = Metric_3_2; serializer = Metric_3_2_Serializer
class Metric_3_2_DetailView(MetricDetailView):
    model = Metric_3_2; serializer = Metric_3_2_Serializer

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