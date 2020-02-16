# -*- coding: utf-8 -*-
from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(max_length=32, validators=[UniqueValidator(queryset=User.objects.all())])
    avatar_url = serializers.SerializerMethodField('get_avatar_url', read_only=True)
    password = serializers.CharField(min_length=6, max_length=100, write_only=True)
    full_name = serializers.SerializerMethodField('get_name', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'full_name', 'username', 'first_name', 'last_name', 'email', 'password', 'avatar_url')

    def create(self, validated_data):
        user = User(email=validated_data['email'],
                    username=validated_data['username'],
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name']
                    )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_avatar_url(self, obj):
        if obj.userprofile and obj.userprofile.avatar:
            return '%s%s%s' % (settings.SITE_URL, settings.MEDIA_URL, obj.userprofile.avatar)
        else:
            return '%s%s' % (settings.STATIC_URL, '/images/default_avatar.jpeg')

    def get_name(self, obj):
        return obj.get_full_name() or obj.username


class UserProfileAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avatar']

