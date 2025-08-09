from django import forms
from .models import Resume
from datetime import datetime, timedelta

class ResumeSearchForm(forms.Form):
    """فرم جستجو در رزومه‌ها"""
    
    DATE_CHOICES = [
        ('', 'همه'),
        ('1', '۱ روز گذشته'),
        ('2', '۲ روز گذشته'), 
        ('3', '۳ روز گذشته'),
        ('7', '۱ هفته گذشته'),
        ('30', '۱ ماه گذشته'),
        ('custom', 'تاریخ دلخواه'),
    ]
    
    # جستجوی نام شرکت
    company_search = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'جستجو در نام شرکت...',
        }),
        label="نام شرکت"
    )
    
    # فیلتر دسته‌بندی شغلی
    job_category = forms.ChoiceField(
        required=False,
        choices=[('', 'همه دسته‌ها')] + Resume.JOB_CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label="دسته‌بندی شغلی"
    )
    
    # فیلتر نوع قرارداد
    contract_type = forms.ChoiceField(
        required=False,
        choices=[('', 'همه نوع‌ها')] + Resume.CONTRACT_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label="نوع قرارداد"
    )
    
    # فیلتر زبان رزومه
    language = forms.ChoiceField(
        required=False,
        choices=[('', 'همه زبان‌ها')] + Resume.LANGUAGE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label="زبان رزومه"
    )
    
    # فیلتر تاریخ
    date_filter = forms.ChoiceField(
        required=False,
        choices=DATE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'date_filter'
        }),
        label="فیلتر تاریخ"
    )
    
    # تاریخ شروع (برای تاریخ دلخواه)
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'date_from'
        }),
        label="از تاریخ"
    )
    
    # تاریخ پایان (برای تاریخ دلخواه)  
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'date_to'
        }),
        label="تا تاریخ"
    )
    
    def get_date_range(self):
        """محاسبه بازه تاریخ براساس انتخاب کاربر"""
        date_filter = self.cleaned_data.get('date_filter')
        date_from = self.cleaned_data.get('date_from')
        date_to = self.cleaned_data.get('date_to')
        
        if not date_filter:
            return None, None
            
        if date_filter == 'custom':
            return date_from, date_to
        
        try:
            days = int(date_filter)
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            return start_date, end_date
        except (ValueError, TypeError):
            return None, None