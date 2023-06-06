from django.shortcuts import render
from rest_framework import generics, permissions,status
from  .serializers import UserDetailSerializer,SpanCounterSerializer
from user.serializers import UserSerializer
from .models import Contacts,SpamCounter,UserbasedSpamList
from user.models import User
from rest_framework.response import Response
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from rest_framework.views import APIView
from django.db import transaction
import base64

# Create your views here.


class ContactCreate(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserDetailSerializer

class ContactDetail(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        queryset = Contacts.objects.filter(mobile_number=self.request.user.mobile_number)
        return queryset


class CheckContactDetail(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
        
    def get_queryset(self):
        query_param = self.request.query_params.get('number')
        if query_param:
            self.serializer_class= UserSerializer
            queryset = User.objects.filter(mobile_number__contains=query_param)
            if not queryset or [i.first_name for i in queryset][0]=='' :
                queryset = Contacts.objects.filter(contact_numbers__contains=query_param).order_by('mobile_number__created_at')[:1]
                self.serializer_class= UserDetailSerializer
        return queryset
    
class SpamCounterView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = SpamCounter.objects.all()
    serializer_class = SpanCounterSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        contact_num = request.data.get('contact_num')
        is_spam = request.data.get('is_spam')

        if contact_num is None:
            return Response({"detail": "Contact number is required."}, status=status.HTTP_400_BAD_REQUEST)

        spam_counter, created = SpamCounter.objects.get_or_create(contact_num=contact_num)
        _mobile_number = User.objects.get(mobile_number=self.request.user.mobile_number)
        _contact_number= contact_num
        contact,created=UserbasedSpamList.objects.get_or_create(mobile_number=_mobile_number,contact_number=_contact_number)
        if is_spam and created:
            spam_counter.spam += 1
            spam_counter.save()
        else:
            return Response({"detail": "Number is already spammed by you."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(spam_counter)
        return Response(serializer.data, status=status.HTTP_200_OK)