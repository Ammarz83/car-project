from rest_framework.viewsets import ModelViewSet, GenericViewSet   
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)   

from .models import (
    Brand,
    Car,
)
from .permissions import (
    IsOwner
)

from .serializers import (
    BrandCreateSerializer, 
    BrandListSerializer, 
    BrandRetrieveSerializer,
    
    CarCreateSerializer, 
    CarListSerializer, 
    CarUpdateSerializer, 
    CarRetrieveSerializer,

)

class BrandViewSet(ModelViewSet):      
    queryset = Brand.objects.all()
    serializer_class = BrandCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return BrandCreateSerializer
        elif self.action == 'list':
            return BrandListSerializer
        elif self.action == 'retrieve':
            return BrandRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'list': 
            self.permission_classes = [AllowAny]
        elif self.action == 'retrieve': 
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update']: 
            self.permission_classes = [IsAdminUser]
        elif self.action == 'destroy': 
            self.permission_classes = [IsOwner]
        return super().get_permissions()
    

class CarViewSet(ModelViewSet):      # CRUD - Create, Retrieve, Update, Delete, 
    queryset = Car.objects.all()
    serializer_class = CarCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CarCreateSerializer
        elif self.action == 'list':
            return CarListSerializer
        elif self.action in ['update', 'partial_update']:
            return CarUpdateSerializer
        elif self.action == 'retrieve':
            return CarRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'list': 
            self.permission_classes = [AllowAny]
        elif self.action == 'retrieve': 
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update']: 
            self.permission_classes = [IsAdminUser]
        elif self.action == 'destroy': 
            self.permission_classes = [IsOwner]
        return super().get_permissions()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        brand_id = request.query_params.get('brand_id')
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

