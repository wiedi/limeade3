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



class MailAliasViewSet(viewsets.ViewSet):
	def list(self, request):
		pass

	def create(self, request):
		pass

	def retrieve(self, request, pk=None):
		pass
		
	def update(self, request, pk=None):
		pass

	def destroy(self, request, pk=None):
		pass
