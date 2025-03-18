from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters


class BaseFilterViewSet(viewsets.GenericViewSet):
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filterset_fields = ()
    search_fields = ()
    ordering_fields = ()
