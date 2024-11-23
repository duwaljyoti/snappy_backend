from rest_framework import serializers

from apps.portal.models import Portal


class PortalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Portal
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'portal-detail', 'lookup_field': 'id'}
        }


