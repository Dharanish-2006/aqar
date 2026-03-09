from rest_framework import serializers
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


# ── Shared ────────────────────────────────────────────────────────────────────

class DocumentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model  = Document
        fields = ['id', 'metric_id', 'original_name', 'file_size', 'extension', 'uploaded_at', 'url']
        read_only_fields = fields

    def get_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class DocumentUploadSerializer(serializers.Serializer):
    metric_id = serializers.CharField(max_length=30)
    file      = serializers.FileField()

    def validate_file(self, value):
        ALLOWED = ['pdf', 'docx', 'xlsx', 'jpg', 'jpeg', 'png']
        MAX     = 10 * 1024 * 1024
        ext     = value.name.rsplit('.', 1)[-1].lower() if '.' in value.name else ''
        if ext not in ALLOWED:
            raise serializers.ValidationError(f"'.{ext}' not allowed. Use PDF, DOCX, XLSX or image.")
        if value.size > MAX:
            raise serializers.ValidationError("File exceeds 10 MB limit.")
        return value


class InstitutionSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model  = InstitutionSettings
        fields = ['college_name', 'aqar_year', 'updated_at']
        read_only_fields = ['updated_at']


# ── Criterion 1 ───────────────────────────────────────────────────────────────

class Metric_1_1_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_1_1
        fields = ['id', 'program_code', 'program_name', 'course_code',
                  'course_name', 'year_of_introduction']


class Metric_1_1_3_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_1_1_3
        fields = ['id', 'year', 'teacher_name', 'body_name']


class Metric_1_2_1_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_1_2_1
        fields = ['id', 'program_code', 'program_name', 'year_introduction',
                  'cbcs_status', 'cbcs_year', 'document_link']


class Metric_1_2_2_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_1_2_2_1_2_3
        fields = ['id', 'program_name', 'course_code', 'year_of_offering',
                  'times_offered', 'duration', 'students_enrolled', 'students_completing']


class Metric_1_3_2_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_1_3_2
        fields = ['id', 'program_name', 'program_code', 'course_name',
                  'course_code', 'year_offering', 'student_name', 'document_link']


class Metric_1_3_3_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_1_3_3
        fields = ['id', 'program_name', 'program_code', 'student_name', 'document_link']


# ── Criterion 2 ───────────────────────────────────────────────────────────────

class Metric_2_1_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_2_1
        fields = ['id', 'year_of_enrollment', 'student_name',
                  'enrollment_number', 'date_of_enrollment']


class Metric_2_2_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_2_2
        fields = ['id', 'year', 'reserved_seats', 'document_link']


class Metric_2_3_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_2_3
        fields = ['id', 'year_of_passing', 'student_name', 'enrollment_number']


class Metric_2_1_1_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_2_1_1
        fields = ['id', 'program_name', 'program_code', 'sanctioned_seats', 'students_admitted']


class Metric_2_1_2_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_2_1_2
        fields = [
            'id', 'year',
            'earmarked_sc', 'earmarked_st', 'earmarked_obc', 'earmarked_gen', 'earmarked_others',
            'admitted_sc',  'admitted_st',  'admitted_obc',  'admitted_gen',  'admitted_others',
        ]


class Metric_2_4_1_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_2_4_1_2_4_3
        fields = ['id', 'teacher_name', 'pan', 'designation', 'year_of_appointment',
                  'nature_of_appointment', 'department', 'years_of_experience', 'still_serving']


class Metric_2_6_3_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_2_6_3
        fields = ['id', 'year', 'program_code', 'program_name',
                  'students_appeared', 'students_passed']


# ── Criterion 3 ───────────────────────────────────────────────────────────────

class Metric_3_1_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_3_1
        fields = ['id', 'teacher_name', 'id_number', 'email', 'gender',
                  'designation', 'date_of_joining', 'sanctioned_posts']


class Metric_3_2_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_3_2
        fields = ['id', 'year', 'sanctioned_posts', 'document_link']


class Metric_2_4_2_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_2_4_2_3_1_2_3_3_1
        fields = ['id', 'teacher_name', 'qualification', 'qualification_year',
                  'is_research_guide', 'recognition_year', 'still_serving',
                  'scholar_name', 'scholar_reg_year', 'thesis_title']


class Metric_3_1_1_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_3_1_1_3_1_3
        fields = ['id', 'project_name', 'pi_name', 'pi_department', 'year_of_award',
                  'amount_sanctioned', 'duration', 'funding_agency', 'agency_type']


class Metric_3_2_2_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_3_2_2
        fields = ['id', 'year', 'seminar_name', 'participants', 'date_from_to', 'activity_link']


class Metric_3_3_2_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_3_3_2
        fields = ['id', 'paper_title', 'authors', 'department',
                  'journal_name', 'year', 'issn', 'ugc_link']


class Metric_3_3_3_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_3_3_3
        # affiliating_institute exists in models.py but not in naacData columns —
        # included here so data is not lost if entered via admin
        fields = ['id', 'sl_no', 'teacher_name', 'book_chapter_title', 'paper_title',
                  'proceedings_title', 'conference_name', 'national_international',
                  'year_of_publication', 'isbn_issn', 'affiliating_institute', 'publisher']


class Metric_3_4_2_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_3_4_2
        fields = ['id', 'activity_name', 'award_name', 'awarding_body', 'year_of_award']


class Metric_3_4_3_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_3_4_3_3_4_4
        fields = ['id', 'activity_name', 'organising_agency', 'scheme_name',
                  'year', 'students_participated']


class Metric_3_5_1_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_3_5_1
        fields = ['id', 'sl_no', 'activity_title', 'collaborating_agency',
                  'participant_name', 'year', 'duration', 'nature_of_activity', 'document_link']


class Metric_3_5_2_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_3_5_2
        fields = ['id', 'organisation', 'institution_industry', 'year_of_signing',
                  'duration', 'activities_under_mou', 'participants_count']


# ── Criterion 4 ───────────────────────────────────────────────────────────────

class Metric_4_1_3_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_4_1_3
        fields = ['id', 'room_name', 'ict_type', 'photo_link']


class Metric_4_1_4_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_4_1_4_4_4_1
        fields = ['id', 'year', 'budget_allocated', 'expenditure_augmentation',
                  'total_expenditure_ex_salary', 'maintenance_academic', 'maintenance_physical']


class Metric_4_2_2_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_4_2_2_4_2_3
        fields = ['id', 'library_resource', 'membership_details',
                  'expenditure_ejournals_ebooks', 'expenditure_other_eresources',
                  'total_library_expenditure', 'document_link']


# ── Criterion 5 ───────────────────────────────────────────────────────────────

class Metric_5_1_1_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_5_1_1_5_1_2
        fields = ['id', 'year', 'scheme_name', 'govt_students_count', 'govt_amount',
                  'institution_students_count', 'institution_amount', 'document_link']


class Metric_5_1_3_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_5_1_3
        fields = ['id', 'program_name', 'date_implemented', 'students_enrolled', 'agency_name']


class Metric_5_1_4_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_5_1_4
        fields = ['id', 'year', 'competitive_exam_activity', 'competitive_exam_students',
                  'career_counselling_activity', 'career_counselling_students',
                  'students_placed_campus', 'document_link']


class Metric_5_2_1_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_5_2_1
        fields = ['id', 'year', 'student_name', 'program_graduated', 'employer_name', 'pay_package']


class Metric_5_2_2_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_5_2_2
        fields = ['id', 'student_name', 'program_graduated', 'institution_joined', 'program_admitted']


class Metric_5_2_3_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_5_2_3
        fields = ['id', 'year', 'roll_number', 'student_name',
                  'net', 'slet', 'gate', 'gmat', 'cat', 'gre', 'jam',
                  'ielts', 'toefl', 'civil_services', 'state_govt_exams', 'other_exams']


class Metric_5_3_1_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_5_3_1
        fields = ['id', 'year', 'award_name', 'team_or_individual',
                  'level', 'sports_or_cultural', 'student_name']


class Metric_5_3_3_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_5_3_3
        fields = ['id', 'event_date', 'event_name', 'student_name']


# ── Criterion 6 ───────────────────────────────────────────────────────────────

class Metric_6_2_3_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_6_2_3
        fields = ['id', 'area', 'vendor_details', 'year_implemented']


class Metric_6_3_2_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_6_3_2
        fields = ['id', 'year', 'teacher_name', 'conference_name', 'professional_body', 'amount']


class Metric_6_3_3_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_6_3_3
        fields = ['id', 'dates', 'teaching_program_title',
                  'nonteaching_program_title', 'participants_count']


class Metric_6_3_4_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_6_3_4
        fields = ['id', 'teacher_name', 'program_title', 'duration']


class Metric_6_4_2_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_6_4_2
        fields = ['id', 'year', 'agency_name', 'purpose', 'amount', 'audit_link']


class Metric_6_5_3_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Metric_6_5_3
        fields = ['id', 'year', 'conferences_seminars', 'aaa_followup', 'nirf_participation',
                  'iso_certification', 'nba_certification', 'collaborative_quality', 'orientation_program']