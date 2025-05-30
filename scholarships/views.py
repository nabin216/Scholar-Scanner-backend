from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Scholarship, Level, ScholarshipCategory, FieldOfStudy, 
    FundType, SponsorType, Country
)
from .serializers import (
    ScholarshipSerializer, LevelSerializer, ScholarshipCategorySerializer,
    FieldOfStudySerializer, FundTypeSerializer, SponsorTypeSerializer, CountrySerializer
)
from .filters import ScholarshipFilter

class ScholarshipViewSet(viewsets.ModelViewSet):
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ScholarshipFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'deadline']

    @action(detail=False, methods=['get'], url_path='filter-options')
    def filter_options(self, request):
        """Return all available filter options"""
        data = {
            'countries': CountrySerializer(Country.objects.all(), many=True).data,
            'levels': LevelSerializer(Level.objects.all(), many=True).data,
            'fields_of_study': FieldOfStudySerializer(FieldOfStudy.objects.all(), many=True).data,
            'fund_types': FundTypeSerializer(FundType.objects.all(), many=True).data,
            'categories': ScholarshipCategorySerializer(ScholarshipCategory.objects.all(), many=True).data,
        }
        return Response(data)

# Create your views here.
