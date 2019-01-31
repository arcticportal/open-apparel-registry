from rest_framework.serializers import (CharField, ModelSerializer)
from api.models import FacilityList, Facility, User


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        exclude = ()

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class FacilityListSerializer(ModelSerializer):
    class Meta:
        model = FacilityList
        fields = ('id', 'name', 'description', 'file_name', 'is_active',
                  'is_public')


class FacilitySerializer(ModelSerializer):
    class Meta:
        model = Facility
        fields = ('id', 'name', 'address', 'country_code', 'location')
