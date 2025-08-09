from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template
from django.http import FileResponse
from django.contrib import messages
from django.db.models import Q
import io
from .models import PersonalInfo, Resume, JobSource
from .forms import ResumeSearchForm

def home(request):
    return render(request, 'home.html')

def health_check(request):
    return HttpResponse("System is healthy!", content_type="text/plain")

def resume_list(request):
    """نمایش لیست رزومه‌ها با قابلیت جستجو"""
    form = ResumeSearchForm(request.GET or None)
    resumes = Resume.objects.all().order_by('-created_at')
    
    if form.is_valid():
        # جستجوی نام شرکت
        company_search = form.cleaned_data.get('company_search')
        if company_search:
            resumes = resumes.filter(
                Q(company_name__icontains=company_search) |
                Q(title__icontains=company_search)
            )
        
        # فیلتر دسته‌بندی شغلی
        job_category = form.cleaned_data.get('job_category')
        if job_category:
            resumes = resumes.filter(job_category=job_category)
        
        # فیلتر نوع قرارداد
        contract_type = form.cleaned_data.get('contract_type')
        if contract_type:
            resumes = resumes.filter(contract_type=contract_type)
        
        # فیلتر زبان رزومه
        language = form.cleaned_data.get('language')
        if language:
            resumes = resumes.filter(language=language)
        
        # فیلتر تاریخ
        date_from, date_to = form.get_date_range()
        if date_from and date_to:
            resumes = resumes.filter(
                created_at__date__gte=date_from,
                created_at__date__lte=date_to
            )
        elif date_from:
            resumes = resumes.filter(created_at__date__gte=date_from)
        elif date_to:
            resumes = resumes.filter(created_at__date__lte=date_to)
    
    context = {
        'resumes': resumes,
        'form': form,
        'total_count': resumes.count(),
        'all_count': Resume.objects.count()
    }
    
    return render(request, 'resumes/list.html', context)

def resume_create(request):
    """ایجاد رزومه جدید"""
    if request.method == 'POST':
        try:
            # دریافت داده‌ها از فرم
            personal_info_id = request.POST.get('personal_info')
            title = request.POST.get('title')
            company_name = request.POST.get('company_name')
            job_title = request.POST.get('job_title')
            job_category = request.POST.get('job_category')
            contract_type = request.POST.get('contract_type')
            language = request.POST.get('language')
            target_salary = request.POST.get('target_salary')
            job_source_id = request.POST.get('job_source')
            job_ad_url = request.POST.get('job_ad_url')
            custom_summary = request.POST.get('custom_summary')
            company_match_reason = request.POST.get('company_match_reason')
            company_notes = request.POST.get('company_notes')
            
            # بررسی فیلدهای اجباری
            if not all([personal_info_id, title, company_name, job_title]):
                messages.error(request, 'لطفاً تمام فیلدهای اجباری را تکمیل کنید.')
            else:
                # ایجاد رزومه جدید
                personal_info = get_object_or_404(PersonalInfo, id=personal_info_id)
                job_source = None
                if job_source_id:
                    job_source = JobSource.objects.get(id=job_source_id)
                
                resume = Resume.objects.create(
                    personal_info=personal_info,
                    title=title,
                    company_name=company_name,
                    job_title=job_title,
                    job_category=job_category,
                    contract_type=contract_type,
                    language=language or 'fa',
                    target_salary=int(target_salary) if target_salary else None,
                    job_source=job_source,
                    job_ad_url=job_ad_url,
                    custom_summary=custom_summary,
                    company_match_reason=company_match_reason,
                    company_notes=company_notes
                )
                
                messages.success(request, f'رزومه "{title}" با موفقیت ایجاد شد!')
                return redirect('resume_detail', resume_id=resume.id)
                
        except Exception as e:
            messages.error(request, f'خطا در ایجاد رزومه: {str(e)}')
    
    personal_infos = PersonalInfo.objects.all()
    job_sources = JobSource.objects.filter(is_active=True)
    context = {
        'personal_infos': personal_infos,
        'job_sources': job_sources,
        'job_categories': Resume.JOB_CATEGORY_CHOICES,
        'contract_types': Resume.CONTRACT_TYPE_CHOICES,
        'languages': Resume.LANGUAGE_CHOICES
    }
    return render(request, 'resumes/create.html', context)

def resume_detail(request, resume_id):
    """نمایش جزئیات رزومه"""
    resume = get_object_or_404(Resume, id=resume_id)
    return render(request, 'resumes/detail.html', {'resume': resume})

def resume_pdf(request, resume_id):
    """نمایش رزومه در قالب قابل چاپ"""
    resume = get_object_or_404(Resume, id=resume_id)
    
    # فعلاً فقط تمپلیت HTML برای چاپ نمایش می‌دهیم
    # کاربر می‌تواند از مرورگر PDF بگیرد (Ctrl+P)
    return render(request, 'resumes/pdf_template.html', {'resume': resume})

def resume_copy(request, resume_id):
    """کپی کردن رزومه موجود"""
    original_resume = get_object_or_404(Resume, id=resume_id)
    
    if request.method == 'POST':
        new_title = request.POST.get('title')
        new_company_name = request.POST.get('company_name')
        new_job_title = request.POST.get('job_title')
        new_job_category = request.POST.get('job_category')
        new_contract_type = request.POST.get('contract_type')
        
        if new_title and new_company_name:
            try:
                new_resume = original_resume.copy_resume(
                    new_title=new_title,
                    new_company_name=new_company_name,
                    new_job_title=new_job_title,
                    new_job_category=new_job_category,
                    new_contract_type=new_contract_type
                )
                messages.success(request, f'رزومه "{new_title}" با موفقیت کپی شد!')
                return redirect('resume_detail', resume_id=new_resume.id)
            except Exception as e:
                messages.error(request, f'خطا در کپی کردن رزومه: {str(e)}')
        else:
            messages.error(request, 'لطفاً عنوان رزومه و نام شرکت را وارد کنید.')
    
    job_sources = JobSource.objects.filter(is_active=True)
    return render(request, 'resumes/copy.html', {
        'original_resume': original_resume,
        'job_categories': Resume.JOB_CATEGORY_CHOICES,
        'contract_types': Resume.CONTRACT_TYPE_CHOICES,
        'languages': Resume.LANGUAGE_CHOICES,
        'job_sources': job_sources
    })
