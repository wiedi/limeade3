from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from advnet.mixins import AdvNetMixin
from .serializers import *
from .models import models

class MailAccountViewSet(
		AdvNetMixin,
		mixins.ListModelMixin,
		mixins.RetrieveModelMixin,
		mixins.DestroyModelMixin,
		viewsets.GenericViewSet
	):

	serializer_class = AccountSerializer
	filter_fields    = ('domain',)
	model            = models.account

	def create(self, request):
		serializer = AccountSerializer(data=request.DATA)
		if serializer.is_valid():
			account = models.account.new(**serializer.data)
			account.set_password(serializer.data['password'])
			account.save()
			return Response(AccountSerializer(account).data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@action()
	def set_password(self, request, id=None):
		account = self.get_object()
		serializer = AccountPasswordSerializer(data=request.DATA)
		if serializer.is_valid():
			account.set_password(serializer.data['password'])
			account.save()
			return Response({'status': 'password set'})
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@action()
	def set_spoofing_whitelist(self, request, id=None):
		account = self.get_object()
		serializer = AccountUpdateSpoofingWhitelistSerializer(data=request.DATA)
		if serializer.is_valid():
			account.spoofing_whitelist = serializer.data['spoofing_whitelist']
			account.save()
			return Response({'status': 'spoofing_whitelist set'})
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@action()
	def disable_submission(self, request, id=None):
		account = self.get_object()
		account.submission_disabled = True
		account.save()
		return Response({'status': 'submission disabled'})

	@action()
	def enable_submission(self, request, id=None):
		account = self.get_object()
		account.submission_disabled = False
		account.save()
		return Response({'status': 'submission enabled'})

	@action()
	def enable_subaddress(self, request, id=None):
		account = self.get_object()
		account.subaddress_extension = True
		account.save()
		return Response({'status': 'subaddress extension mode enabled'})

	@action()
	def disable_subaddress(self, request, id=None):
		account = self.get_object()
		account.subaddress_extension = False
		account.save()
		return Response({'status': 'subaddress extension mode disabled'})


class MailAliasViewSet(
		AdvNetMixin,
		mixins.ListModelMixin,
		mixins.RetrieveModelMixin,
		mixins.DestroyModelMixin,
		viewsets.GenericViewSet
	):

	serializer_class = AliasSerializer
	filter_fields    = ('domain',)
	model            = models.alias

	def create(self, request):
		serializer = AliasSerializer(data=request.DATA)
		if serializer.is_valid():
			alias = models.alias.new(**serializer.data)
			alias.save()
			return Response(AliasSerializer(alias).data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def update(self, request, id=None):
		alias = self.get_object()
		serializer = AliasUpdateSerializer(data=request.DATA)
		if serializer.is_valid():
			alias.to = serializer.data['to']
			alias.save()
			return Response(AliasSerializer(alias).data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
