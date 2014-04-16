from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from stdnet.utils.exceptions import ObjectNotFound
from .serializers import *
from .models import models

class MailAccountViewSet(viewsets.ViewSet):
	def get_object(self, pk):
		try:
			return models.account.get(id=pk)
		except ObjectNotFound:
			raise Http404
		
	def list(self, request):
		serializer = AccountSerializer(models.account.all(), many=True)
		return Response(serializer.data)

	def create(self, request):
		serializer = AccountSerializer(data=request.DATA)
		if serializer.is_valid():
			account = models.account.new(**serializer.data)
			account.set_password(serializer.data['password'])
			account.save()
			return Response(AccountSerializer(account).data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def retrieve(self, request, pk=None):
		account = self.get_object(pk)
		return Response(AccountSerializer(account).data)

	@action()
	def set_password(self, request, pk=None):
		account = self.get_object(pk)
		serializer = AccountPasswordSerializer(data=request.DATA)
		if serializer.is_valid():
			account.set_password(serializer.data['password'])
			account.save()
			return Response({'status': 'password set'})
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def destroy(self, request, pk=None):
		account = self.get_object(pk)
		account.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)



class MailAliasViewSet(viewsets.ViewSet):
	def get_object(self, pk):
		try:
			return models.alias.get(id=pk)
		except ObjectNotFound:
			raise Http404
		
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
