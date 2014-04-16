from rest_framework import serializers

class AccountSerializer(serializers.Serializer):
    id       = serializers.CharField(read_only = True)
    name     = serializers.RegexField(r'[^@]+')
    domain   = serializers.CharField()
    password = serializers.CharField(write_only = True)

class AccountPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()