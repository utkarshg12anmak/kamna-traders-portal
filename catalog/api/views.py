from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from catalog.models import Item, Brand, Category, UOM, TaxRate
from .serializers import ItemSerializer

class IsAuthenticatedRead(permissions.IsAuthenticated):
    pass

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().select_related('brand','category','uom','tax_rate')
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedRead]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status','brand','category','uom']
    search_fields = ['name','sku']
    ordering = ['-updated_at']

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def active_choices(request):
    return Response({
        'brands': list(Brand.objects.filter(is_active=True, deleted_at__isnull=True).values('id','name')),
        'categories': list(Category.objects.filter(is_active=True, deleted_at__isnull=True).values('id','name','parent_id')),
        'uoms': list(UOM.objects.filter(is_active=True, deleted_at__isnull=True).values('id','code','name')),
        'tax_rates': list(TaxRate.objects.filter(is_active=True, deleted_at__isnull=True).values('id','title','rate')),
    })
