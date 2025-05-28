from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Scholarship, Level, ScholarshipCategory, FieldOfStudy,
    FundType, SponsorType, LanguageRequirement, Country
)

class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship
        fields = '__all__'
        widgets = {
            'open_date': forms.DateInput(attrs={'type': 'date'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    form = ScholarshipForm
    filter_horizontal = (
        'levels',
        'field_of_study',
        'fund_type',
        'sponsor_type',
        'language_requirement',
        'scholarship_category'
    )      
    
    list_display = (
        'title',
        'country',
        'get_fields_of_study',
        'deadline',
        'open_date',
        'get_fund_types',
        'get_sponsor_types',
        'get_levels',
        'get_scholarship_category',
        'get_language_requirements',
        'is_featured',
        'get_image_preview',
        'get_application_link'
    )    
    
    list_filter = (
        'levels',
        'country',
        'field_of_study',
        'fund_type',
        'sponsor_type',
        'scholarship_category',
        'language_requirement',
        'is_featured',
        'deadline',
        'open_date'
    )
    
    search_fields = (
        'title',
        'description',
        'country',
        'field_of_study',
        'language_requirement'
    )
    
    readonly_fields = ('created_at', 'updated_at')    
    def get_scholarship_category(self, obj):
        return ", ".join([category.name for category in obj.scholarship_category.all()])
    get_scholarship_category.short_description = 'Categories'
    
    def get_fields_of_study(self, obj):
        return ", ".join([field.name for field in obj.field_of_study.all()])
    get_fields_of_study.short_description = 'Fields of Study'

    def get_levels(self, obj):
        return ", ".join([level.name for level in obj.levels.all()])
    get_levels.short_description = 'Levels'

    def get_fund_types(self, obj):
        return ", ".join([fund.name for fund in obj.fund_type.all()])
    get_fund_types.short_description = 'Fund Types'

    def get_sponsor_types(self, obj):
        return ", ".join([sponsor.name for sponsor in obj.sponsor_type.all()])
    get_sponsor_types.short_description = 'Sponsor Types'
    
    def get_language_requirements(self, obj):
        return ", ".join([lang.name for lang in obj.language_requirement.all()])
    get_language_requirements.short_description = 'Language Requirements'

    def get_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;"/>', obj.image)
        return "No image"
    get_image_preview.short_description = 'Image'
    
    def get_application_link(self, obj):
        if obj.application_url:
            return format_html('<a href="{}" target="_blank">Apply</a>', obj.application_url)
        return "No link"
    get_application_link.short_description = 'Application'

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ScholarshipCategory)
class ScholarshipCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(FieldOfStudy)
class FieldOfStudyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(FundType)
class FundTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(SponsorType)
class SponsorTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(LanguageRequirement)
class LanguageRequirementAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
