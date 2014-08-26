from rest_framework import serializers

class AccountSerializer(serializers.Serializer):
	id		 = serializers.CharField(read_only = True)
	name	 = serializers.RegexField(r'[^@]+')
	domain	 = serializers.CharField()
	password = serializers.CharField()

	submission_disabled = serializers.BooleanField(default=False)
	spoofing_whitelist  = serializers.CharField(default='', required=False)

class AccountPasswordSerializer(serializers.Serializer):
	password = serializers.CharField()

class AccountUpdateSpoofingWhitelistSerializer(serializers.Serializer):
	spoofing_whitelist  = serializers.CharField(default='', required=False)

class AliasSerializer(serializers.Serializer):
	id		 = serializers.CharField(read_only = True)
	name	 = serializers.RegexField(r'[^@]+')
	domain	 = serializers.CharField()
	to		 = serializers.CharField()

class AliasUpdateSerializer(serializers.Serializer):
	to		 = serializers.CharField()