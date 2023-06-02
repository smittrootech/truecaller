from rest_framework import serializers
from .models import User

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    full_name= serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('mobile_number', "full_name","is_spam")
    def get_full_name(self,object):
        return object.first_name + ' ' +object.last_name

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('mobile_number', 'first_name','last_name','password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password=validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
