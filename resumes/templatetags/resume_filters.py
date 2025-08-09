from django import template
from django.utils import timezone
from datetime import datetime, timedelta
import locale
import jdatetime

register = template.Library()

def gregorian_to_jalali(g_y, g_m, g_d):
    """تبدیل تاریخ میلادی به شمسی"""
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    
    if g_m > 2:
        jy = 0
    else:
        jy = 1
    
    gy2 = (g_m > 2) and (g_y + 1) or g_y
    days = 365 * g_y + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) - 80 + g_d + g_d_m[g_m - 1]
    jy += 33 * (days // 12053)
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    
    if days > 365:
        jy += (days - 1) // 365
        days = (days - 1) % 365
    
    if days < 186:
        jm = 1 + days // 31
        jd = 1 + (days % 31)
    else:
        jm = 7 + (days - 186) // 30
        jd = 1 + ((days - 186) % 30)
    
    return jy, jm, jd

@register.filter
def persian_date(value, format_str='Y/m/d'):
    """
    تبدیل تاریخ میلادی به شمسی با استفاده از jdatetime
    فرمت‌های پشتیبانی شده: Y/m/d, Y-m-d, d/m/Y, d F Y
    """
    if not value:
        return ""
    
    try:
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                try:
                    value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return value
        
        # تبدیل به تاریخ اگر datetime است
        if hasattr(value, 'date'):
            date_obj = value.date()
        else:
            date_obj = value
        
        # تبدیل به jdatetime
        j_date = jdatetime.date.fromgregorian(date=date_obj)
        
        # تبدیل اعداد انگلیسی به فارسی
        persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        english_digits = '0123456789'
        
        def to_persian_digits(text):
            for i, eng in enumerate(english_digits):
                text = text.replace(eng, persian_digits[i])
            return text
        
        # فرمت کردن براساس درخواست
        if format_str == 'Y/m/d':
            result = j_date.strftime('%Y/%m/%d')
        elif format_str == 'Y/m':
            result = j_date.strftime('%Y/%m')
        elif format_str == 'Y-m-d':
            result = j_date.strftime('%Y-%m-%d')
        elif format_str == 'd/m/Y':
            result = j_date.strftime('%d/%m/%Y')
        elif format_str == 'd F Y':
            # استفاده از نام ماه فارسی
            result = j_date.strftime('%d %B %Y')
        else:
            result = j_date.strftime('%Y/%m/%d')
        
        # تبدیل به اعداد فارسی
        return to_persian_digits(result)
        
    except (ValueError, TypeError, AttributeError):
        return str(value)

@register.filter
def format_salary(value):
    """
    فرمت کردن حقوق به صورت خوانا
    مثال: 45000000 -> ۴۵ میلیون تومان
    """
    if not value:
        return ""
    
    try:
        # تبدیل به عدد
        amount = int(value)
        
        # تبدیل اعداد انگلیسی به فارسی
        persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        english_digits = '0123456789'
        
        def to_persian_digits(text):
            for i, eng in enumerate(english_digits):
                text = text.replace(eng, persian_digits[i])
            return text
        
        # فرمت کردن بر اساس مقدار
        if amount >= 1000000000:  # میلیارد
            formatted = f"{amount / 1000000000:.1f}".rstrip('0').rstrip('.')
            unit = "میلیارد"
        elif amount >= 1000000:  # میلیون
            formatted = f"{amount / 1000000:.1f}".rstrip('0').rstrip('.')
            unit = "میلیون"
        elif amount >= 1000:  # هزار
            formatted = f"{amount / 1000:.1f}".rstrip('0').rstrip('.')
            unit = "هزار"
        else:
            formatted = str(amount)
            unit = ""
        
        # تبدیل به اعداد فارسی
        formatted = to_persian_digits(formatted)
        
        # ساخت متن نهایی
        if unit:
            return f"{formatted} {unit} تومان"
        else:
            return f"{formatted} تومان"
            
    except (ValueError, TypeError):
        return str(value)

@register.filter
def days_ago(value):
    """
    محاسبه تعداد روزهای گذشته از یک تاریخ
    """
    if not value:
        return ""
    
    try:
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d')
        
        now = timezone.now()
        if hasattr(value, 'date'):
            value = value.date()
        if hasattr(now, 'date'):
            now = now.date()
        
        diff = now - value
        days = diff.days
        
        # تبدیل به فارسی
        persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        english_digits = '0123456789'
        
        days_str = str(days)
        for i, eng in enumerate(english_digits):
            days_str = days_str.replace(eng, persian_digits[i])
        
        if days == 0:
            return "امروز"
        elif days == 1:
            return "دیروز"
        elif days < 7:
            return f"{days_str} روز پیش"
        elif days < 30:
            weeks = days // 7
            weeks_str = str(weeks)
            for i, eng in enumerate(english_digits):
                weeks_str = weeks_str.replace(eng, persian_digits[i])
            return f"{weeks_str} هفته پیش"
        elif days < 365:
            months = days // 30
            months_str = str(months)
            for i, eng in enumerate(english_digits):
                months_str = months_str.replace(eng, persian_digits[i])
            return f"{months_str} ماه پیش"
        else:
            years = days // 365
            years_str = str(years)
            for i, eng in enumerate(english_digits):
                years_str = years_str.replace(eng, persian_digits[i])
            return f"{years_str} سال پیش"
            
    except (ValueError, TypeError):
        return str(value)


@register.filter
def skill_translation(skill, language):
    """دریافت ترجمه مهارت براساس زبان"""
    if not skill:
        return ""
    return skill.get_translation(language)


@register.filter
def experience_position_translation(experience, language):
    """دریافت ترجمه سمت سابقه کاری"""
    if not experience:
        return ""
    return experience.get_position_translation(language)


@register.filter
def experience_company_translation(experience, language):
    """دریافت ترجمه شرکت سابقه کاری"""
    if not experience:
        return ""
    return experience.get_company_translation(language)


@register.filter
def experience_description_translation(experience, language):
    """دریافت ترجمه توضیحات سابقه کاری"""
    if not experience:
        return ""
    return experience.get_description_translation(language)


@register.filter
def education_degree_translation(education, language):
    """دریافت ترجمه مدرک تحصیلی"""
    if not education:
        return ""
    return education.get_degree_translation(language)


@register.filter
def education_field_translation(education, language):
    """دریافت ترجمه رشته تحصیلی"""
    if not education:
        return ""
    return education.get_field_translation(language)


@register.filter
def education_university_translation(education, language):
    """دریافت ترجمه دانشگاه"""
    if not education:
        return ""
    return education.get_university_translation(language)