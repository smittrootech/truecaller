from rest_framework import serializers
from user.models import User
from django.conf import settings
from .models import Contacts,SpamCounter
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['first_name','last_name','contact_numbers',"is_spam"]

    def create(self, validated_data):
        # print(self.context.get("request").user.mobile_number)
        mobile_number=User.objects.get(mobile_number=self.context.get("request").user.mobile_number)
        validated_data['mobile_number']=mobile_number
        try:
            return super().create(validated_data)

        except IntegrityError as error:
            raise ValidationError('Unique constraint failure')

class SpanCounterSerializer(serializers.ModelSerializer):
    is_spam=serializers.BooleanField(read_only=True)
    class Meta:
        model = SpamCounter
        fields = ['contact_num','is_spam']
