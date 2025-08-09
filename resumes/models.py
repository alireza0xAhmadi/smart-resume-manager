from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from tinymce.models import HTMLField


class JobSource(models.Model):
    """منابع آگهی‌های استخدام"""
    name = models.CharField(max_length=100, verbose_name="نام منبع", unique=True)
    slug = models.SlugField(max_length=100, unique=True, verbose_name="شناسه URL")
    website_url = models.URLField(blank=True, verbose_name="آدرس وبسایت")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "منبع آگهی"
        verbose_name_plural = "منابع آگهی‌ها"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # ایجاد slug از نام فارسی
            base_slug = slugify(self.name.replace('ا', 'a').replace('ی', 'i').replace(' ', '-'))
            if not base_slug:  # اگر slug خالی شد از ID استفاده کن
                base_slug = f"source-{self.pk or 'new'}"
            self.slug = base_slug
        super().save(*args, **kwargs)


class PersonalInfo(models.Model):
    """اطلاعات شخصی"""
    MARITAL_STATUS_CHOICES = [
        ('single', 'مجرد'),
        ('married', 'متاهل'),
        ('divorced', 'مطلقه'),
        ('widowed', 'بیوه'),
    ]
    
    MILITARY_STATUS_CHOICES = [
        ('completed', 'پایان خدمت'),
        ('exempt', 'معافیت'),
        ('student_exempt', 'معافیت تحصیلی'),
        ('postponed', 'مهلت تحصیلی'),
        ('required', 'مشمول'),
        ('not_required', 'مشمول نمی‌باشد'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="نام کامل")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=20, verbose_name="تلفن")
    address = models.TextField(blank=True, verbose_name="آدرس")
    linkedin = models.URLField(blank=True, verbose_name="لینکدین")
    github = models.URLField(blank=True, verbose_name="گیت‌هاب")
    website = models.URLField(blank=True, verbose_name="وبسایت")
    summary = HTMLField(blank=True, verbose_name="خلاصه پیشفرض")
    
    # فیلدهای جدید
    marital_status = models.CharField(
        max_length=20, 
        choices=MARITAL_STATUS_CHOICES, 
        blank=True,
        verbose_name="وضعیت تاهل"
    )
    military_status = models.CharField(
        max_length=20, 
        choices=MILITARY_STATUS_CHOICES, 
        blank=True,
        verbose_name="وضعیت سربازی"
    )
    expected_salary = models.PositiveIntegerField(
        blank=True, 
        null=True,
        verbose_name="حقوق مورد انتظار (تومان)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "اطلاعات شخصی"
        verbose_name_plural = "اطلاعات شخصی"
    
    def __str__(self):
        return self.name


class Experience(models.Model):
    """سوابق کاری"""
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=200, verbose_name="شرکت")
    position = models.CharField(max_length=200, verbose_name="سمت")
    start_date = models.DateField(verbose_name="تاریخ شروع")
    end_date = models.DateField(blank=True, null=True, verbose_name="تاریخ پایان")
    is_current = models.BooleanField(default=False, verbose_name="شغل فعلی")
    description = HTMLField(verbose_name="توضیحات")
    
    class Meta:
        verbose_name = "سابقه کاری"
        verbose_name_plural = "سوابق کاری"
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.position} در {self.company}"
    
    def get_position_translation(self, language='fa'):
        """دریافت ترجمه سمت براساس زبان"""
        translation = self.translations.filter(language=language).first()
        if translation and translation.position:
            return translation.position
        return self.position
    
    def get_company_translation(self, language='fa'):
        """دریافت ترجمه شرکت براساس زبان"""
        translation = self.translations.filter(language=language).first()
        if translation and translation.company:
            return translation.company
        return self.company
    
    def get_description_translation(self, language='fa'):
        """دریافت ترجمه توضیحات براساس زبان"""
        translation = self.translations.filter(language=language).first()
        if translation and translation.description:
            return translation.description
        return self.description


class Education(models.Model):
    """تحصیلات"""
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=200, verbose_name="مدرک")
    field = models.CharField(max_length=200, verbose_name="رشته")
    university = models.CharField(max_length=200, verbose_name="دانشگاه")
    start_date = models.DateField(verbose_name="تاریخ شروع")
    end_date = models.DateField(blank=True, null=True, verbose_name="تاریخ پایان")
    is_current = models.BooleanField(default=False, verbose_name="در حال تحصیل")
    gpa = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        blank=True, 
        null=True,
        verbose_name="معدل"
    )
    
    class Meta:
        verbose_name = "تحصیلات"
        verbose_name_plural = "تحصیلات"
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.degree} - {self.field}"
    
    def get_degree_translation(self, language='fa'):
        """دریافت ترجمه مدرک براساس زبان"""
        translation = self.translations.filter(language=language).first()
        if translation and translation.degree:
            return translation.degree
        return self.degree
    
    def get_field_translation(self, language='fa'):
        """دریافت ترجمه رشته براساس زبان"""
        translation = self.translations.filter(language=language).first()
        if translation and translation.field:
            return translation.field
        return self.field
    
    def get_university_translation(self, language='fa'):
        """دریافت ترجمه دانشگاه براساس زبان"""
        translation = self.translations.filter(language=language).first()
        if translation and translation.university:
            return translation.university
        return self.university


class Skill(models.Model):
    """مهارت‌ها"""
    CATEGORY_CHOICES = [
        ('programming', 'برنامه‌نویسی'),
        ('web_frontend', 'فرانت‌اند وب'),
        ('web_backend', 'بک‌اند وب'),
        ('database', 'پایگاه داده'),
        ('mobile', 'موبایل'),
        ('devops', 'DevOps'),
        ('cms', 'سیستم مدیریت محتوا'),
        ('framework', 'فریم‌ورک'),
        ('library', 'کتابخانه'),
        ('soft_skills', 'مهارت‌های نرم'),
        ('other', 'سایر'),
    ]
    
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100, verbose_name="نام مهارت")
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='other',
        verbose_name="دسته‌بندی"
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    
    class Meta:
        verbose_name = "مهارت"
        verbose_name_plural = "مهارت‌ها"
        ordering = ['category', 'name']
    
    def __str__(self):
        return self.name
    
    def get_translation(self, language='fa'):
        """دریافت ترجمه مهارت براساس زبان"""
        translation = self.translations.filter(language=language).first()
        if translation:
            return translation.name
        # اگر ترجمه یافت نشد، نام اصلی برگردانده می‌شود
        return self.name


class Resume(models.Model):
    """رزومه‌های ایجاد شده"""
    JOB_CATEGORY_CHOICES = [
        ('php_laravel', 'PHP / Laravel Developer'),
        ('python_django', 'Python / Django Developer'),
        ('wordpress', 'WordPress Developer'),
        ('frontend', 'Frontend Developer'),
        ('fullstack', 'Full-stack Developer'),
        ('mobile', 'Mobile Developer'),
        ('devops', 'DevOps Engineer'),
        ('data_science', 'Data Science'),
        ('ui_ux', 'UI/UX Designer'),
        ('project_manager', 'Project Manager'),
        ('other', 'سایر'),
    ]
    
    CONTRACT_TYPE_CHOICES = [
        ('full_time', 'تمام وقت'),
        ('part_time', 'پاره وقت'),
        ('remote', 'دورکاری'),
    ]
    
    LANGUAGE_CHOICES = [
        ('fa', 'فارسی'),
        ('en', 'انگلیسی'),
        ('de', 'آلمانی'),
        ('fr', 'فرانسوی'),
        ('ar', 'عربی'),
    ]
    
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=200, verbose_name="عنوان رزومه")
    company_name = models.CharField(max_length=200, verbose_name="نام شرکت")
    job_title = models.CharField(max_length=200, verbose_name="عنوان شغلی")
    job_category = models.CharField(
        max_length=30,
        choices=JOB_CATEGORY_CHOICES,
        default='other',
        verbose_name="دسته‌بندی شغلی"
    )
    contract_type = models.CharField(
        max_length=20,
        choices=CONTRACT_TYPE_CHOICES,
        default='full_time',
        verbose_name="نوع قرارداد"
    )
    language = models.CharField(
        max_length=5,
        choices=LANGUAGE_CHOICES,
        default='fa',
        verbose_name="زبان رزومه"
    )
    
    # فیلتر کردن مهارت‌ها، سوابق و تحصیلات براساس فیلد is_active و نیاز شغل
    selected_experiences = models.ManyToManyField(Experience, through='ResumeExperience', blank=True, verbose_name="سوابق انتخابی")
    selected_educations = models.ManyToManyField(Education, through='ResumeEducation', blank=True, verbose_name="تحصیلات انتخابی")
    selected_skills = models.ManyToManyField(
        Skill, 
        blank=True, 
        verbose_name="مهارت‌های انتخابی",
        limit_choices_to={'is_active': True}
    )
    
    custom_summary = HTMLField(blank=True, verbose_name="خلاصه سفارشی")
    target_salary = models.PositiveIntegerField(
        blank=True, 
        null=True,
        verbose_name="حقوق مورد انتظار برای این موقعیت (تومان)"
    )
    company_match_reason = models.TextField(
        blank=True,
        verbose_name="چرا این رزومه برای این شرکت مناسب است؟",
        help_text="توضیح دهید که چرا شما برای این شرکت مفید هستید و این رزومه را متناسب با نیازهای آنها طراحی کرده‌اید"
    )
    copied_from = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="کپی شده از",
        help_text="رزومه‌ای که این رزومه از آن کپی شده"
    )
    
    # فیلدهای مربوط به منبع آگهی و اطلاعات تکمیلی
    job_source = models.ForeignKey(
        JobSource,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="منبع آگهی",
        help_text="منبعی که آگهی استخدام را در آن دیده‌اید"
    )
    job_ad_url = models.URLField(
        blank=True,
        verbose_name="آدرس کامل صفحه آگهی",
        help_text="لینک مستقیم صفحه آگهی استخدام"
    )
    company_notes = models.TextField(
        blank=True,
        verbose_name="یادداشت‌های شرکت",
        help_text="توضیحات و یادداشت‌های شخصی درباره این شرکت"
    )
    job_ad_full_text = HTMLField(
        blank=True,
        verbose_name="متن کامل آگهی شرکت",
        help_text="متن کامل آگهی استخدام برای مراجعه و بایگانی شخصی"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "رزومه"
        verbose_name_plural = "رزومه‌ها"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_job_category_display()}"
    
    def get_relevant_skills(self):
        """بازگرداندن مهارت‌های مرتبط با دسته‌بندی شغلی"""
        if not self.personal_info_id:
            return Skill.objects.none()
            
        # نقشه‌برداری دسته‌بندی شغلی به دسته‌بندی مهارت‌ها
        category_mapping = {
            'php_laravel': ['programming', 'web_backend', 'framework', 'database'],
            'python_django': ['programming', 'web_backend', 'framework', 'database'],
            'wordpress': ['cms', 'web_frontend', 'web_backend', 'programming'],
            'frontend': ['web_frontend', 'library', 'framework'],
            'fullstack': ['web_frontend', 'web_backend', 'database', 'framework'],
            'mobile': ['mobile', 'programming'],
            'devops': ['devops', 'database'],
        }
        
        relevant_categories = category_mapping.get(self.job_category, [])
        
        return self.personal_info.skills.filter(
            is_active=True,
            category__in=relevant_categories
        ) if relevant_categories else self.personal_info.skills.filter(is_active=True)
    
    def get_ordered_experiences(self):
        """دریافت سوابق کاری با ترتیب صحیح"""
        return [
            re.experience for re in 
            ResumeExperience.objects.filter(resume=self).order_by('order')
        ]
    
    def get_ordered_educations(self):
        """دریافت تحصیلات با ترتیب صحیح"""
        return [
            re.education for re in 
            ResumeEducation.objects.filter(resume=self).order_by('order')
        ]
    
    def copy_resume(self, new_title, new_company_name, new_job_title=None, new_job_category=None, new_contract_type=None):
        """کپی کردن رزومه با عنوان و نام شرکت جدید"""
        # محفوظ کردن روابط many-to-many با ترتیب‌بندی قبل از کپی
        experience_orders = {
            re.experience.id: re.order 
            for re in ResumeExperience.objects.filter(resume=self)
        }
        education_orders = {
            re.education.id: re.order 
            for re in ResumeEducation.objects.filter(resume=self)
        }
        selected_skills = list(self.selected_skills.all())
        
        # کپی کردن رزومه
        new_resume = Resume.objects.create(
            personal_info=self.personal_info,
            title=new_title,
            company_name=new_company_name,
            job_title=new_job_title or self.job_title,
            job_category=new_job_category or self.job_category,
            contract_type=new_contract_type or self.contract_type,
            language=self.language,
            custom_summary=self.custom_summary,
            target_salary=self.target_salary,
            company_match_reason="",  # خالی برای تکمیل توسط کاربر
            copied_from=self
        )
        
        # اضافه کردن سوابق کاری با حفظ ترتیب
        for exp_id, order in experience_orders.items():
            ResumeExperience.objects.create(
                resume=new_resume,
                experience_id=exp_id,
                order=order
            )
        
        # اضافه کردن تحصیلات با حفظ ترتیب
        for edu_id, order in education_orders.items():
            ResumeEducation.objects.create(
                resume=new_resume,
                education_id=edu_id,
                order=order
            )
        
        # اضافه کردن مهارت‌ها (بدون تغییر)
        new_resume.selected_skills.set(selected_skills)
        
        return new_resume


class SkillTranslation(models.Model):
    """ترجمه مهارت‌ها به زبان‌های مختلف"""
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='translations')
    language = models.CharField(
        max_length=5,
        choices=Resume.LANGUAGE_CHOICES,
        verbose_name="زبان"
    )
    name = models.CharField(max_length=100, verbose_name="نام ترجمه شده")
    
    class Meta:
        verbose_name = "ترجمه مهارت"
        verbose_name_plural = "ترجمه‌های مهارت"
        unique_together = ['skill', 'language']
    
    def __str__(self):
        return f"{self.skill.name} - {self.get_language_display()}: {self.name}"


class ExperienceTranslation(models.Model):
    """ترجمه سوابق کاری به زبان‌های مختلف"""
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='translations')
    language = models.CharField(
        max_length=5,
        choices=Resume.LANGUAGE_CHOICES,
        verbose_name="زبان"
    )
    position = models.CharField(max_length=200, blank=True, verbose_name="سمت ترجمه شده")
    company = models.CharField(max_length=200, blank=True, verbose_name="شرکت ترجمه شده")
    description = models.TextField(blank=True, verbose_name="توضیحات ترجمه شده")
    
    class Meta:
        verbose_name = "ترجمه سابقه کاری"
        verbose_name_plural = "ترجمه‌های سوابق کاری"
        unique_together = ['experience', 'language']
    
    def __str__(self):
        return f"{self.experience.position} - {self.get_language_display()}"


class EducationTranslation(models.Model):
    """ترجمه تحصیلات به زبان‌های مختلف"""
    education = models.ForeignKey(Education, on_delete=models.CASCADE, related_name='translations')
    language = models.CharField(
        max_length=5,
        choices=Resume.LANGUAGE_CHOICES,
        verbose_name="زبان"
    )
    degree = models.CharField(max_length=200, blank=True, verbose_name="مدرک ترجمه شده")
    field = models.CharField(max_length=200, blank=True, verbose_name="رشته ترجمه شده")
    university = models.CharField(max_length=200, blank=True, verbose_name="دانشگاه ترجمه شده")
    
    class Meta:
        verbose_name = "ترجمه تحصیلات"
        verbose_name_plural = "ترجمه‌های تحصیلات"
        unique_together = ['education', 'language']
    
    def __str__(self):
        return f"{self.education.degree} - {self.get_language_display()}"


class ResumeExperience(models.Model):
    """جدول واسط برای تنظیم ترتیب سوابق کاری در رزومه"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    
    class Meta:
        verbose_name = "سابقه کاری رزومه"
        verbose_name_plural = "سوابق کاری رزومه"
        ordering = ['order']
        unique_together = ['resume', 'experience']
    
    def __str__(self):
        return f"{self.resume.title} - {self.experience.position}"


class ResumeEducation(models.Model):
    """جدول واسط برای تنظیم ترتیب تحصیلات در رزومه"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    education = models.ForeignKey(Education, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    
    class Meta:
        verbose_name = "تحصیلات رزومه"
        verbose_name_plural = "تحصیلات رزومه"
        ordering = ['order']
        unique_together = ['resume', 'education']
    
    def __str__(self):
        return f"{self.resume.title} - {self.education.degree}"


