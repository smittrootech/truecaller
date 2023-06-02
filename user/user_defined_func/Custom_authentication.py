from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField



class CustomeAuthentication(serializers.Serializer):
    mobile_number = PhoneNumberField(
        label=_("mobile_numer"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        mobile_number = attrs.get('mobile_number')
        password = attrs.get('password')
        print(mobile_number,password)
        if mobile_number and password:
            user = authenticate(username=mobile_number, password=password)
            print(user)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs