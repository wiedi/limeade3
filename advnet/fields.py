from stdnet import odm

from stdnet.utils import string_type, encoders

class CompositeSymbolField(odm.AtomField):
	type = 'composite'
	python_type = string_type
	charset = 'utf-8'

	def __init__(self, *fields, seperator = '', **kwargs):
		kwargs['primary_key'] = True
		super(CompositeSymbolField, self).__init__(**kwargs)
		self.seperator = seperator
		self.fields    = fields
		if len(self.fields) < 2:
			raise FieldError('At least tow fields are required by composite CompositeSymbolField')

	def get_encoder(self, params):
		return encoders.Default(self.charset)

	def to_python(self, value, backend=None):
		return self.encoder.loads(value)

	def get_value(self, instance, *bits):
		if bits:
			raise AttributeError
		values = tuple((getattr(instance, f.attname) for f in self.fields))
		return self.seperator.join(values)

	def register_with_model(self, name, model):
		fields = []
		for field in self.fields:
			if field not in model._meta.dfields:
				raise FieldError('Composite id field "%s" in in "%s" model.' % (field, model._meta))
			field = model._meta.dfields[field]
			if field.internal_type not in ('text', 'numeric'):
				raise FieldError('Composite id field "%s" not valid type.' % field)
			fields.append(field)
		self.fields = tuple(fields)
		return super(CompositeSymbolField, self).register_with_model(name, model)
	
	def scorefun(self, value):
		return 0


class SortableSymbolField(odm.SymbolField):
	def scorefun(self, value):
		return 0