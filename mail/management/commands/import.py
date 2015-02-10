from django.core.management.base import BaseCommand, CommandError
import requests
from mail.models import models, Account, Alias
from mail.serializers import AccountSerializer, AliasSerializer

class Command(BaseCommand):
	args = '<url> [url ...]'
	help = 'Import Account and Alias data from HTTP hosted JSON files'

	def handle(self, *args, **options):
		datas = []
		for url in args:
			try:
				datas += [requests.get(url).json()]
			except Exception as e:
				print('failed to load: ' + url)
				print(str(e))
				return

		for data in datas:
			s = models.session()
			for domain in data.keys():
				with s.begin() as t:
					# account
					t.delete(s.query(models.account).filter(domain=domain))
					for a in data[domain].get('account', []):
						a['domain'] = domain
						acc = AccountSerializer(data=a)
						if acc.is_valid():
							t.add(Account(**acc.data))
					# alias
					t.delete(s.query(models.alias).filter(domain=domain))
					for a in data[domain].get('alias', []):
						a['domain'] = domain
						alias = AliasSerializer(data=a)
						if alias.is_valid():
							t.add(Alias(**alias.data))

