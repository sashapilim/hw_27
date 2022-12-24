from django.db.models import Count
from rest_framework import serializers

from users.models import User, Location


class UserListSerializer(serializers.ModelSerializer):
    total_ads = serializers.IntegerField()
    location = serializers.SlugRelatedField(
        many=True,
        queryset=Location.objects.values('name'),
        slug_field='name'
    )

    class Meta:
        model = User
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        many=True,
        queryset=Location.objects.values('name'),
        slug_field='name'
    )

    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(required=False,
        many=True,
        queryset=Location.objects.values('name'),
        slug_field='name'
    )

    def is_valid(self, *, raise_exception=False):
        self._location = self.initial_data.pop('location', [])
        return super().is_valid(raise_exception=raise_exception)


    def create(self, validated_data):
        new_user=User.objects.create(**validated_data)
        for loc in self._location:
            locations, _ = Location.objects.get_or_create(name=loc)
            new_user.location.add(locations)
        return new_user

    class Meta:
        model = User
        exclude = ['password']


class UserUpdateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        many=True,
        queryset=Location.objects.values('name'),
        slug_field='name'
    )

    def is_valid(self, *, raise_exception=False):
        self._location = self.initial_data.pop('location', [])
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        user = super().save(**kwargs)
        for loc in self._location:
            locations, _ = Location.objects.get_or_create(name=loc)
            user.location.add(locations)
        return user

    class Meta:
        model = User
        exclude = ['password']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'