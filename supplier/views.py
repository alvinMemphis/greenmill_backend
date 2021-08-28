from django.shortcuts import render
from .serializers import PackageSerializer
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


# Create your views here.
class PackageGreenCreate(generics.GenericAPIView):
    serializer_class = PackageSerializer
    permission_class = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)