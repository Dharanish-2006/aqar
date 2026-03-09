from django.db import models
from django.contrib.auth.models import User
class InstitutionSettings(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE, related_name='institution_settings')
    college_name = models.CharField(max_length=255, default='Your Institution')
    aqar_year    = models.CharField(max_length=10, default='2023-24')
    updated_at   = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user.username} — {self.college_name}"
class Document(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    metric_id     = models.CharField(max_length=30)
    file          = models.FileField(upload_to='documents/%Y/%m/')
    original_name = models.CharField(max_length=255)
    file_size     = models.PositiveIntegerField(default=0)
    extension     = models.CharField(max_length=10)
    uploaded_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.metric_id} — {self.original_name}"


# c1
class Metric_1_1(models.Model):
    """1.1"""
    user                 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_1_1')
    program_code         = models.CharField(max_length=50, blank=True, default='')
    program_name         = models.CharField(max_length=255, blank=True, default='')
    course_code          = models.CharField(max_length=50, blank=True, default='')
    course_name          = models.CharField(max_length=255, blank=True, default='')
    year_of_introduction = models.CharField(max_length=10, blank=True, default='')

    class Meta:
        ordering = ['program_code']

    def __str__(self):
        return f"{self.user.username} | 1.1 | {self.course_code}"


class Metric_1_1_3(models.Model):
    """1.1.3"""
    user             = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_1_1_3')
    year             = models.CharField(max_length=10, blank=True, default='')
    teacher_name     = models.CharField(max_length=255, blank=True, default='')
    body_name        = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 1.1.3 | {self.teacher_name}"


class Metric_1_2_1(models.Model):
    """1.2.1"""
    user              = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_1_2_1')
    program_code      = models.CharField(max_length=50, blank=True, default='')
    program_name      = models.CharField(max_length=255, blank=True, default='')
    year_introduction = models.CharField(max_length=10, blank=True, default='')
    cbcs_status       = models.CharField(max_length=5, blank=True, default='')   # Yes/No
    cbcs_year         = models.CharField(max_length=10, blank=True, default='')
    document_link     = models.URLField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 1.2.1 | {self.program_name}"


class Metric_1_2_2_1_2_3(models.Model):
    """1.2.2 & 1.2.3"""
    user                     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_1_2_2')
    program_name             = models.CharField(max_length=255, blank=True, default='')
    course_code              = models.CharField(max_length=50, blank=True, default='')
    year_of_offering         = models.CharField(max_length=10, blank=True, default='')
    times_offered            = models.PositiveIntegerField(null=True, blank=True)
    duration                 = models.CharField(max_length=100, blank=True, default='')
    students_enrolled        = models.PositiveIntegerField(null=True, blank=True)
    students_completing      = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} | 1.2.2/3 | {self.program_name}"


class Metric_1_3_2(models.Model):
    """1.3.2"""
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_1_3_2')
    program_name   = models.CharField(max_length=255, blank=True, default='')
    program_code   = models.CharField(max_length=50, blank=True, default='')
    course_name    = models.CharField(max_length=255, blank=True, default='')
    course_code    = models.CharField(max_length=50, blank=True, default='')
    year_offering  = models.CharField(max_length=10, blank=True, default='')
    student_name   = models.CharField(max_length=255, blank=True, default='')
    document_link  = models.URLField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 1.3.2 | {self.course_name}"


class Metric_1_3_3(models.Model):
    """1.3.3"""
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_1_3_3')
    program_name   = models.CharField(max_length=255, blank=True, default='')
    program_code   = models.CharField(max_length=50, blank=True, default='')
    student_name   = models.CharField(max_length=255, blank=True, default='')
    document_link  = models.URLField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 1.3.3 | {self.student_name}"


# c2
class Metric_2_1(models.Model):
    """2.1"""
    user               = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_2_1')
    year_of_enrollment = models.CharField(max_length=10, blank=True, default='')
    student_name       = models.CharField(max_length=255, blank=True, default='')
    enrollment_number  = models.CharField(max_length=50, blank=True, default='')
    date_of_enrollment = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} | 2.1 | {self.student_name}"


class Metric_2_2(models.Model):
    """2.2"""
    user                  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_2_2')
    year                  = models.CharField(max_length=10, blank=True, default='')
    reserved_seats        = models.PositiveIntegerField(null=True, blank=True)
    document_link         = models.URLField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 2.2 | {self.year}"


class Metric_2_3(models.Model):
    """2.3"""
    user              = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_2_3')
    year_of_passing   = models.CharField(max_length=10, blank=True, default='')
    student_name      = models.CharField(max_length=255, blank=True, default='')
    enrollment_number = models.CharField(max_length=50, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 2.3 | {self.student_name}"


class Metric_2_1_1(models.Model):
    """2.1.1"""
    user               = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_2_1_1')
    program_name       = models.CharField(max_length=255, blank=True, default='')
    program_code       = models.CharField(max_length=50, blank=True, default='')
    sanctioned_seats   = models.PositiveIntegerField(null=True, blank=True)
    students_admitted  = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} | 2.1.1 | {self.program_name}"


class Metric_2_1_2(models.Model):
    """2.1.2"""
    user                     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_2_1_2')
    year                     = models.CharField(max_length=10, blank=True, default='')
    earmarked_sc             = models.PositiveIntegerField(null=True, blank=True)
    earmarked_st             = models.PositiveIntegerField(null=True, blank=True)
    earmarked_obc            = models.PositiveIntegerField(null=True, blank=True)
    earmarked_gen            = models.PositiveIntegerField(null=True, blank=True)
    earmarked_others         = models.PositiveIntegerField(null=True, blank=True)
    admitted_sc              = models.PositiveIntegerField(null=True, blank=True)
    admitted_st              = models.PositiveIntegerField(null=True, blank=True)
    admitted_obc             = models.PositiveIntegerField(null=True, blank=True)
    admitted_gen             = models.PositiveIntegerField(null=True, blank=True)
    admitted_others          = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} | 2.1.2 | {self.year}"


class Metric_2_4_1_2_4_3(models.Model):
    """2.4.1 & 2.4.3"""
    user                    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_2_4_1')
    teacher_name            = models.CharField(max_length=255, blank=True, default='')
    pan                     = models.CharField(max_length=20, blank=True, default='')
    designation             = models.CharField(max_length=100, blank=True, default='')
    year_of_appointment     = models.CharField(max_length=10, blank=True, default='')
    nature_of_appointment   = models.CharField(max_length=100, blank=True, default='')
    department              = models.CharField(max_length=100, blank=True, default='')
    years_of_experience     = models.PositiveIntegerField(null=True, blank=True)
    still_serving           = models.CharField(max_length=10, blank=True, default='')  # Yes / last year

    def __str__(self):
        return f"{self.user.username} | 2.4.1/3 | {self.teacher_name}"


class Metric_2_6_3(models.Model):
    """2.6.3"""
    user                      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_2_6_3')
    year                      = models.CharField(max_length=10, blank=True, default='')
    program_code              = models.CharField(max_length=50, blank=True, default='')
    program_name              = models.CharField(max_length=255, blank=True, default='')
    students_appeared         = models.PositiveIntegerField(null=True, blank=True)
    students_passed           = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} | 2.6.3 | {self.program_name} {self.year}"
# c3
class Metric_3_1(models.Model):
    """3.1"""
    user               = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_3_1')
    teacher_name       = models.CharField(max_length=255, blank=True, default='')
    id_number          = models.CharField(max_length=50, blank=True, default='')
    email              = models.EmailField(blank=True, default='')
    gender             = models.CharField(max_length=10, blank=True, default='')
    designation        = models.CharField(max_length=100, blank=True, default='')
    date_of_joining    = models.DateField(null=True, blank=True)
    sanctioned_posts   = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} | 3.1 | {self.teacher_name}"


class Metric_3_2(models.Model):
    """3.2"""
    user                  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_3_2')
    year                  = models.CharField(max_length=10, blank=True, default='')
    sanctioned_posts      = models.PositiveIntegerField(null=True, blank=True)
    document_link         = models.URLField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 3.2 | {self.year}"


class Metric_2_4_2_3_1_2_3_3_1(models.Model):
    """2.4.2, 3.1.2 & 3.3.1"""
    user                  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_2_4_2')
    teacher_name          = models.CharField(max_length=255, blank=True, default='')
    qualification         = models.CharField(max_length=100, blank=True, default='')
    qualification_year    = models.CharField(max_length=10, blank=True, default='')
    is_research_guide     = models.CharField(max_length=5, blank=True, default='') # Y/N
    recognition_year      = models.CharField(max_length=10, blank=True, default='')
    still_serving         = models.CharField(max_length=10, blank=True, default='')
    scholar_name          = models.CharField(max_length=255, blank=True, default='')
    scholar_reg_year      = models.CharField(max_length=10, blank=True, default='')
    thesis_title          = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 2.4.2/3.1.2/3.3.1 | {self.teacher_name}"


class Metric_3_1_1_3_1_3(models.Model):
    """3.1.1 & 3.1.3"""
    user              = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_3_1_1')
    project_name      = models.CharField(max_length=255, blank=True, default='')
    pi_name           = models.CharField(max_length=255, blank=True, default='')
    pi_department     = models.CharField(max_length=100, blank=True, default='')
    year_of_award     = models.CharField(max_length=10, blank=True, default='')
    amount_sanctioned = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    duration          = models.CharField(max_length=50, blank=True, default='')
    funding_agency    = models.CharField(max_length=255, blank=True, default='')
    agency_type       = models.CharField(max_length=50, blank=True, default='')   # Government / Non-Government

    def __str__(self):
        return f"{self.user.username} | 3.1.1/3 | {self.project_name}"


class Metric_3_2_2(models.Model):
    """3.2.2"""
    user             = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_3_2_2')
    year             = models.CharField(max_length=10, blank=True, default='')
    seminar_name     = models.CharField(max_length=255, blank=True, default='')
    participants     = models.PositiveIntegerField(null=True, blank=True)
    date_from_to     = models.CharField(max_length=50, blank=True, default='')
    activity_link    = models.URLField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 3.2.2 | {self.seminar_name}"


class Metric_3_3_2(models.Model):
    """3.3.2"""
    user             = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_3_3_2')
    paper_title      = models.CharField(max_length=500, blank=True, default='')
    authors          = models.TextField(blank=True, default='')
    department       = models.CharField(max_length=100, blank=True, default='')
    journal_name     = models.CharField(max_length=255, blank=True, default='')
    year             = models.CharField(max_length=10, blank=True, default='')
    issn             = models.CharField(max_length=20, blank=True, default='')
    ugc_link         = models.URLField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 3.3.2 | {self.paper_title[:60]}"


class Metric_3_3_3(models.Model):
    """3.3.3"""
    user                   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_3_3_3')
    sl_no                  = models.PositiveIntegerField(null=True, blank=True)
    teacher_name           = models.CharField(max_length=255, blank=True, default='')
    book_chapter_title     = models.CharField(max_length=500, blank=True, default='')
    paper_title            = models.CharField(max_length=500, blank=True, default='')
    proceedings_title      = models.CharField(max_length=500, blank=True, default='')
    conference_name        = models.CharField(max_length=255, blank=True, default='')
    national_international = models.CharField(max_length=20, blank=True, default='')
    year_of_publication    = models.CharField(max_length=10, blank=True, default='')
    isbn_issn              = models.CharField(max_length=30, blank=True, default='')
    affiliating_institute  = models.CharField(max_length=255, blank=True, default='')
    publisher              = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 3.3.3 | {self.teacher_name}"


class Metric_3_4_2(models.Model):
    """3.4.2"""
    user               = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_3_4_2')
    activity_name      = models.CharField(max_length=255, blank=True, default='')
    award_name         = models.CharField(max_length=255, blank=True, default='')
    awarding_body      = models.CharField(max_length=255, blank=True, default='')
    year_of_award      = models.CharField(max_length=10, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 3.4.2 | {self.award_name}"


class Metric_3_4_3_3_4_4(models.Model):
    """3.4.3 & 3.4.4"""
    user                   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_3_4_3')
    activity_name          = models.CharField(max_length=255, blank=True, default='')
    organising_agency      = models.CharField(max_length=255, blank=True, default='')
    scheme_name            = models.CharField(max_length=255, blank=True, default='')
    year                   = models.CharField(max_length=10, blank=True, default='')
    students_participated  = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} | 3.4.3/4 | {self.activity_name}"


class Metric_3_5_1(models.Model):
    """3.5.1"""
    user               = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_3_5_1')
    sl_no              = models.PositiveIntegerField(null=True, blank=True)
    activity_title     = models.CharField(max_length=255, blank=True, default='')
    collaborating_agency = models.TextField(blank=True, default='')
    participant_name   = models.CharField(max_length=255, blank=True, default='')
    year               = models.CharField(max_length=10, blank=True, default='')
    duration           = models.CharField(max_length=50, blank=True, default='')
    nature_of_activity = models.CharField(max_length=100, blank=True, default='')
    document_link      = models.URLField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 3.5.1 | {self.activity_title}"


class Metric_3_5_2(models.Model):
    """3.5.2"""
    user                        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_3_5_2')
    organisation                = models.CharField(max_length=255, blank=True, default='')
    institution_industry        = models.CharField(max_length=255, blank=True, default='')
    year_of_signing             = models.CharField(max_length=10, blank=True, default='')
    duration                    = models.CharField(max_length=50, blank=True, default='')
    activities_under_mou        = models.TextField(blank=True, default='')
    participants_count          = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} | 3.5.2 | {self.organisation}"


# c4
class Metric_4_1_3(models.Model):
    """4.1.3"""
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_4_1_3')
    room_name      = models.CharField(max_length=255, blank=True, default='')
    ict_type       = models.CharField(max_length=255, blank=True, default='')
    photo_link     = models.URLField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 4.1.3 | {self.room_name}"


class Metric_4_1_4_4_4_1(models.Model):
    """4.1.4 & 4.4.1"""
    user                         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_4_1_4')
    year                         = models.CharField(max_length=10, blank=True, default='')
    budget_allocated             = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    expenditure_augmentation     = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_expenditure_ex_salary  = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    maintenance_academic         = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    maintenance_physical         = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} | 4.1.4/4.4.1 | {self.year}"


class Metric_4_2_2_4_2_3(models.Model):
    """4.2.2 & 4.2.3"""
    user                         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_4_2_2')
    library_resource             = models.CharField(max_length=100, blank=True, default='')  # Books, e-journals, etc.
    membership_details           = models.TextField(blank=True, default='')
    expenditure_ejournals_ebooks = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    expenditure_other_eresources = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_library_expenditure    = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    document_link                = models.URLField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 4.2.2/3 | {self.library_resource}"
# c5
class Metric_5_1_1_5_1_2(models.Model):
    """5.1.1 & 5.1.2"""
    user                       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_5_1_1')
    year                       = models.CharField(max_length=10, blank=True, default='')
    scheme_name                = models.CharField(max_length=255, blank=True, default='')
    govt_students_count        = models.PositiveIntegerField(null=True, blank=True)
    govt_amount                = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    institution_students_count = models.PositiveIntegerField(null=True, blank=True)
    institution_amount         = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    document_link              = models.URLField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 5.1.1/2 | {self.scheme_name} {self.year}"


class Metric_5_1_3(models.Model):
    """5.1.3"""
    user              = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_5_1_3')
    program_name      = models.CharField(max_length=255, blank=True, default='')
    date_implemented  = models.DateField(null=True, blank=True)
    students_enrolled = models.PositiveIntegerField(null=True, blank=True)
    agency_name       = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 5.1.3 | {self.program_name}"


class Metric_5_1_4(models.Model):
    """5.1.4"""
    user                             = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_5_1_4')
    year                             = models.CharField(max_length=10, blank=True, default='')
    competitive_exam_activity        = models.CharField(max_length=255, blank=True, default='')
    competitive_exam_students        = models.PositiveIntegerField(null=True, blank=True)
    career_counselling_activity      = models.CharField(max_length=255, blank=True, default='')
    career_counselling_students      = models.PositiveIntegerField(null=True, blank=True)
    students_placed_campus           = models.PositiveIntegerField(null=True, blank=True)
    document_link                    = models.URLField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 5.1.4 | {self.year}"


class Metric_5_2_1(models.Model):
    """5.2.1"""
    user              = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_5_2_1')
    year              = models.CharField(max_length=10, blank=True, default='')
    student_name      = models.CharField(max_length=255, blank=True, default='')
    program_graduated = models.CharField(max_length=255, blank=True, default='')
    employer_name     = models.CharField(max_length=255, blank=True, default='')
    pay_package       = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 5.2.1 | {self.student_name}"


class Metric_5_2_2(models.Model):
    """5.2.2"""
    user               = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_5_2_2')
    student_name       = models.CharField(max_length=255, blank=True, default='')
    program_graduated  = models.CharField(max_length=255, blank=True, default='')
    institution_joined = models.CharField(max_length=255, blank=True, default='')
    program_admitted   = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 5.2.2 | {self.student_name}"


class Metric_5_2_3(models.Model):
    """5.2.3"""
    user                      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_5_2_3')
    year                      = models.CharField(max_length=10, blank=True, default='')
    roll_number               = models.CharField(max_length=50, blank=True, default='')
    student_name              = models.CharField(max_length=255, blank=True, default='')
    net                       = models.PositiveIntegerField(null=True, blank=True)
    slet                      = models.PositiveIntegerField(null=True, blank=True)
    gate                      = models.PositiveIntegerField(null=True, blank=True)
    gmat                      = models.PositiveIntegerField(null=True, blank=True)
    cat                       = models.PositiveIntegerField(null=True, blank=True)
    gre                       = models.PositiveIntegerField(null=True, blank=True)
    jam                       = models.PositiveIntegerField(null=True, blank=True)
    ielts                     = models.PositiveIntegerField(null=True, blank=True)
    toefl                     = models.PositiveIntegerField(null=True, blank=True)
    civil_services            = models.PositiveIntegerField(null=True, blank=True)
    state_govt_exams          = models.PositiveIntegerField(null=True, blank=True)
    other_exams               = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} | 5.2.3 | {self.student_name}"


class Metric_5_3_1(models.Model):
    """5.3.1"""
    user                       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_5_3_1')
    year                       = models.CharField(max_length=10, blank=True, default='')
    award_name                 = models.CharField(max_length=255, blank=True, default='')
    team_or_individual         = models.CharField(max_length=20, blank=True, default='')
    level                      = models.CharField(max_length=50, blank=True, default='')   # University/State/National/International
    sports_or_cultural         = models.CharField(max_length=20, blank=True, default='')
    student_name               = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 5.3.1 | {self.student_name}"


class Metric_5_3_3(models.Model):
    """5.3.3"""
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_5_3_3')
    event_date      = models.DateField(null=True, blank=True)
    event_name      = models.CharField(max_length=255, blank=True, default='')
    student_name    = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 5.3.3 | {self.event_name}"
# c z6
class Metric_6_2_3(models.Model):
    """6.2.3"""
    user              = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_6_2_3')
    area              = models.CharField(
        max_length=50,
        choices=[
            ('Administration', 'Administration'),
            ('Finance and Accounts', 'Finance and Accounts'),
            ('Student Admission and Support', 'Student Admission and Support'),
            ('Examination', 'Examination'),
        ],
        blank=True, default=''
    )
    vendor_details    = models.TextField(blank=True, default='')
    year_implemented  = models.CharField(max_length=10, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 6.2.3 | {self.area}"


class Metric_6_3_2(models.Model):
    """6.3.2"""
    user              = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_6_3_2')
    year              = models.CharField(max_length=10, blank=True, default='')
    teacher_name      = models.CharField(max_length=255, blank=True, default='')
    conference_name   = models.CharField(max_length=255, blank=True, default='')
    professional_body = models.CharField(max_length=255, blank=True, default='')
    amount            = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} | 6.3.2 | {self.teacher_name}"


class Metric_6_3_3(models.Model):
    """6.3.3"""
    user                        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_6_3_3')
    dates                       = models.CharField(max_length=50, blank=True, default='')
    teaching_program_title      = models.CharField(max_length=255, blank=True, default='')
    nonteaching_program_title   = models.CharField(max_length=255, blank=True, default='')
    participants_count          = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} | 6.3.3 | {self.teaching_program_title}"


class Metric_6_3_4(models.Model):
    """6.3.4 – Teachers attending FDP (online/face-to-face)"""
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_6_3_4')
    teacher_name  = models.CharField(max_length=255, blank=True, default='')
    program_title = models.CharField(max_length=255, blank=True, default='')
    duration      = models.CharField(max_length=50, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 6.3.4 | {self.teacher_name}"
class Metric_6_4_2(models.Model):
    """6.4.2"""
    user             = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_6_4_2')
    year             = models.CharField(max_length=10, blank=True, default='')
    agency_name      = models.CharField(max_length=255, blank=True, default='')
    purpose          = models.TextField(blank=True, default='')
    amount           = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    audit_link       = models.URLField(max_length=500, blank=True, default='')

    def __str__(self):
        return f"{self.user.username} | 6.4.2 | {self.agency_name}"
class Metric_6_5_3(models.Model):
    """6.5.3"""
    user                          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metric_6_5_3')
    year                          = models.CharField(max_length=10, blank=True, default='')
    conferences_seminars          = models.TextField(blank=True, default='')
    aaa_followup                  = models.TextField(blank=True, default='')
    nirf_participation            = models.TextField(blank=True, default='')
    iso_certification             = models.TextField(blank=True, default='')
    nba_certification             = models.TextField(blank=True, default='')
    collaborative_quality         = models.TextField(blank=True, default='')
    orientation_program           = models.TextField(blank=True, default='')
    def __str__(self):
        return f"{self.user.username} | 6.5.3 | {self.year}"