from django.shortcuts import render
from ..models import *
from django.http import JsonResponse 
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status 
from rest_framework.views import APIView 
from rest_framework import mixins, generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}  # new dictionary to store and return data (incl. token)
        if serializer.is_valid():
            account = serializer.save()  # data saved into an account variable for later access       
            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email
            token = Token.objects.get(user=account).key  
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)

class ProfileList(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.all()
    
