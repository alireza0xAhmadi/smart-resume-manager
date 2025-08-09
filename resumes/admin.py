from django.contrib import admin
from django import forms
from tinymce.widgets import TinyMCE
from .models import (
    PersonalInfo, Experience, Education, Skill, Resume, JobSource,
    SkillTranslation, ExperienceTranslation, EducationTranslation,
    ResumeExperience, ResumeEducation
)


class ExperienceForm(forms.ModelForm):
    description = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 8}),
        required=False,
        label="توضیحات"
    )
    
    class Meta:
        model = Experience
        fields = '__all__'


class ExperienceInline(admin.TabularInline):
    model = Experience
    form = ExperienceForm
    extra = 1


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


class SkillTranslationInline(admin.TabularInline):
    model = SkillTranslation
    extra = 1
    fields = ['language', 'name']


class ExperienceTranslationInline(admin.TabularInline):
    model = ExperienceTranslation
    extra = 1
    fields = ['language', 'position', 'company', 'description']


class EducationTranslationInline(admin.TabularInline):
    model = EducationTranslation
    extra = 1
    fields = ['language', 'degree', 'field', 'university']


class ResumeExperienceInline(admin.TabularInline):
    model = ResumeExperience
    extra = 0
    fields = ['experience', 'order']
    verbose_name = "سابقه کاری"
    verbose_name_plural = "سوابق کاری رزومه"
    ordering = ['order']


class ResumeEducationInline(admin.TabularInline):
    model = ResumeEducation
    extra = 0
    fields = ['education', 'order']
    verbose_name = "تحصیلات"
    verbose_name_plural = "تحصیلات رزومه"
    ordering = ['order']



class PersonalInfoForm(forms.ModelForm):
    summary = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 8}),
        required=False,
        label="خلاصه پیشفرض"
    )
    
    class Meta:
        model = PersonalInfo
        fields = '__all__'


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    form = PersonalInfoForm
    list_display = ['name', 'email', 'phone', 'marital_status', 'military_status', 'expected_salary', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['marital_status', 'military_status', 'created_at']
    inlines = [ExperienceInline, EducationInline, SkillInline]
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'email', 'phone', 'address')
        }),
        ('شبکه‌های اجتماعی', {
            'fields': ('linkedin', 'github', 'website')
        }),
        ('اطلاعات تکمیلی', {
            'fields': ('marital_status', 'military_status', 'expected_salary')
        }),
        ('خلاصه', {
            'fields': ('summary',)
        }),
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    form = ExperienceForm
    list_display = ['position', 'company', 'personal_info', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'start_date', 'company']
    search_fields = ['position', 'company', 'personal_info__name']
    inlines = [ExperienceTranslationInline]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'field', 'university', 'personal_info', 'start_date', 'end_date', 'gpa']
    list_filter = ['is_current', 'start_date', 'university']
    search_fields = ['degree', 'field', 'university', 'personal_info__name']
    inlines = [EducationTranslationInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'personal_info', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'personal_info__name']
    list_editable = ['is_active']
    inlines = [SkillTranslationInline]


@admin.register(JobSource)
class JobSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'slug', 'is_active')
        }),
        ('جزئیات', {
            'fields': ('website_url', 'description')
        }),
    )


class ResumeForm(forms.ModelForm):
    custom_summary = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 10}),
        required=False,
        label="خلاصه سفارشی"
    )
    job_ad_full_text = forms.CharField(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 15}),
        required=False,
        label="متن کامل آگهی شرکت"
    )
    target_salary = forms.CharField(
        widget=forms.TextInput(attrs={'style': 'width: 300px;'}),
        required=False,
        label="حقوق مورد انتظار برای این موقعیت (تومان)"
    )
    
    class Meta:
        model = Resume
        fields = '__all__'


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    form = ResumeForm
    list_display = ['title', 'company_name', 'job_category', 'contract_type', 'language', 'job_source', 'personal_info', 'target_salary', 'created_at']
    list_filter = ['created_at', 'job_category', 'contract_type', 'language', 'job_source', 'company_name']
    search_fields = ['title', 'company_name', 'job_title', 'personal_info__name']
    filter_horizontal = ['selected_skills']
    inlines = [ResumeExperienceInline, ResumeEducationInline]
    
    fieldsets = (
        ('اطلاعات کلی', {
            'fields': ('personal_info', 'title', 'company_name', 'job_title', 'job_category', 'contract_type', 'language')
        }),
        ('منبع آگهی', {
            'fields': ('job_source', 'job_ad_url', 'company_notes', 'job_ad_full_text'),
        }),
        ('تنظیمات مالی', {
            'fields': ('target_salary',),
            'description': 'حقوق مورد انتظار برای این موقعیت شغلی را مشخص کنید.'
        }),
        ('انتخاب مهارت‌ها', {
            'fields': ('selected_skills',),
            'description': 'مهارت‌هایی را که در این رزومه نمایش داده شوند انتخاب کنید.'
        }),
        ('محتوای سفارشی', {
            'fields': ('custom_summary', 'company_match_reason'),
            'description': 'محتوای اختصاصی برای این رزومه و دلیل انطباق با شرکت.'
        }),
        ('اطلاعات سیستم', {
            'fields': ('copied_from',),
            'classes': ('collapse',),
        }),
    )


# Translation admin classes
@admin.register(SkillTranslation)
class SkillTranslationAdmin(admin.ModelAdmin):
    list_display = ['skill', 'language', 'name']
    list_filter = ['language']
    search_fields = ['skill__name', 'name']


@admin.register(ExperienceTranslation)
class ExperienceTranslationAdmin(admin.ModelAdmin):
    list_display = ['experience', 'language', 'position', 'company']
    list_filter = ['language']
    search_fields = ['experience__position', 'position', 'company']


@admin.register(EducationTranslation)
class EducationTranslationAdmin(admin.ModelAdmin):
    list_display = ['education', 'language', 'degree', 'field']
    list_filter = ['language']
    search_fields = ['education__degree', 'degree', 'field']


@admin.register(ResumeExperience)
class ResumeExperienceAdmin(admin.ModelAdmin):
    list_display = ['resume', 'experience', 'order']
    list_filter = ['resume__job_category', 'experience__company']
    search_fields = ['resume__title', 'experience__position', 'experience__company']
    list_editable = ['order']
    ordering = ['resume', 'order']


@admin.register(ResumeEducation)
class ResumeEducationAdmin(admin.ModelAdmin):
    list_display = ['resume', 'education', 'order']
    list_filter = ['resume__job_category', 'education__university']
    search_fields = ['resume__title', 'education__degree', 'education__university']
    list_editable = ['order']
    ordering = ['resume', 'order']
