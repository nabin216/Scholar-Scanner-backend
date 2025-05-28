from django_filters import rest_framework as filters
from .models import Scholarship

class ScholarshipFilter(filters.FilterSet):
    levels = filters.CharFilter(field_name='levels__id')
    field_of_study = filters.CharFilter(field_name='field_of_study__id')
    fund_type = filters.CharFilter(field_name='fund_type__id')
    sponsor_type = filters.CharFilter(field_name='sponsor_type__id')
    scholarship_category = filters.CharFilter(field_name='scholarship_category__id')
    deadline_after = filters.DateFilter(field_name='deadline', lookup_expr='gte')
    deadline_before = filters.DateFilter(field_name='deadline', lookup_expr='lte')
    country = filters.CharFilter(field_name='country__name', lookup_expr='icontains')
    
    class Meta:
        model = Scholarship
        fields = {
            'is_featured': ['exact'],
        }
