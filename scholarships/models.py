from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']

class Level(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class ScholarshipCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class FundType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Fund Types"

class SponsorType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Sponsor Types"

class LanguageRequirement(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Language Requirements"

class FieldOfStudy(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Fields of Study"

class Scholarship(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField()
    levels = models.ManyToManyField(Level, related_name='scholarships')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='scholarships')
    field_of_study = models.ManyToManyField(FieldOfStudy, related_name='scholarships')
    deadline = models.DateField()
    open_date = models.DateField(null=True, blank=True)
    fund_type = models.ManyToManyField(FundType, related_name='scholarships')
    sponsor_type = models.ManyToManyField(SponsorType, related_name='scholarships')
    language_requirement = models.ManyToManyField(LanguageRequirement, related_name='scholarships', blank=True)
    image = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    scholarship_category = models.ManyToManyField(ScholarshipCategory, related_name='scholarships')
    application_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
