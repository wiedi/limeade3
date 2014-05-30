from django.core.management.base import BaseCommand, CommandError
import requests
from mail.models import models, Account, Alias

#from polls.models import Poll

class Command(BaseCommand):
	args = '<url> [url ...]'
	help = 'Import Account and Alias data from HTTP hosted JSON files'

	def handle(self, *args, **options):
		for url in args:
			data = requests.get(url).json()
			s = models.session()
			for domain in data.keys():
				with s.begin() as t:
					# account
					t.delete(s.query(models.account).filter(domain=domain))
					for a in data[domain].get('account', []):
						t.add(Account(name=a["name"], password=a["password"], domain=domain))
					# alias
					t.delete(s.query(models.alias).filter(domain=domain))
					for a in data[domain].get('alias', []):
						t.add(Alias(name=a["name"], to=a["to"], domain=domain))

