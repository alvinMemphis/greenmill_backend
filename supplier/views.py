from django.shortcuts import render
from .serializers import PackageSerializer,SupplierSerializer
from rest_framework import status, generics,viewsets
from supplier.models import Supplier
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from person.models import GreenUser

# Create your views here.
class PackageGreenCreate(generics.GenericAPIView):
    serializer_class = PackageSerializer
    permission_class = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PackageGreenUpdate(generics.GenericAPIView):
    serializer_class = PackageSerializer
    permission_class = [IsAuthenticated]


    def patch(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SupplierViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows suppliers to be viewed or edited.
    """
    queryset = GreenUser.objects.filter(user_type='supplier').all()
    serializer_class = SupplierSerializer



    def get_permissions(self):
        if self.action == 'create':

            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

