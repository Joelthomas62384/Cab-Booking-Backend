from rest_framework.views import APIView
from . serializers import *
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework.generics import CreateAPIView,ListCreateAPIView
from django.shortcuts import get_object_or_404






class CabView(APIView):

    def get(self, request):
        approved_str = request.query_params.get('approved', 'false').lower()
        approved = approved_str in ['true', '1', 'yes']  
        
        cabs = Cab.objects.filter(approved=approved, busy=False)
        
        serializer = CabSerializer(cabs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user

        data = request.data

        serializer = CabSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    