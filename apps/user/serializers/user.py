from django.contrib.auth.models import User
from rest_framework import serializers

from apps.user.models import UserPortal
from apps.portal import *
from apps.portal.models import Portal


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'password', 'email', 'is_staff']


class UserPortalSerializer(serializers.ModelSerializer):
    portal = serializers.HyperlinkedRelatedField(
        view_name='portal-detail',
        queryset=Portal.objects.all(),
        lookup_field='id'
    )

    class Meta:
        model = UserPortal
        fields = ['user', 'portal', 'created_at', 'updated_at']
