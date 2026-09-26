from rest_framework import serializers


class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    message = serializers.CharField(max_length=2000)
