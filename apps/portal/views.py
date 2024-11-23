from rest_framework import viewsets

from apps.portal.models import Portal
from apps.portal.serializer import PortalSerializer


class PortalView(viewsets.ModelViewSet):
    queryset = Portal.objects.all()
    serializer_class = PortalSerializer
    lookup_field = 'id'
