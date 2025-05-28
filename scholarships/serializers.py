from rest_framework import serializers
from .models import (
    Scholarship, Level, ScholarshipCategory, FieldOfStudy,
    FundType, SponsorType, LanguageRequirement, Country
)

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'name']

class ScholarshipCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScholarshipCategory
        fields = ['id', 'name']

class FieldOfStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOfStudy
        fields = ['id', 'name']

class FundTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundType
        fields = ['id', 'name']

class SponsorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsorType
        fields = ['id', 'name']

class LanguageRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageRequirement
        fields = ['id', 'name']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']

class ScholarshipSerializer(serializers.ModelSerializer):
    levels = LevelSerializer(many=True, read_only=True)
    scholarship_category = ScholarshipCategorySerializer(many=True, read_only=True)
    field_of_study = FieldOfStudySerializer(many=True, read_only=True)
    fund_type = FundTypeSerializer(many=True, read_only=True)
    sponsor_type = SponsorTypeSerializer(many=True, read_only=True)
    language_requirement = LanguageRequirementSerializer(many=True, read_only=True)
    country_detail = CountrySerializer(source='country', read_only=True)
    country_name = serializers.CharField(source='country.name', read_only=True)

    class Meta:
        model = Scholarship
        fields = '__all__'
