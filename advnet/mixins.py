from django.http import Http404
from stdnet.utils.exceptions import ObjectNotFound
from .filter import AdvNetFilter

class AdvNetMixin(object):
	filter_backends  = (AdvNetFilter,)
	lookup_field     = 'id'
	
	def get_object(self):
		lookup = self.kwargs.get(self.lookup_field, None)
		try:
			return self.model.get(**{self.lookup_field: lookup})
		except ObjectNotFound:
			raise Http404

	def get_queryset(self):
		return self.model.query()