from rest_framework import filters

class AdvNetFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		filter_fields = getattr(view, 'filter_fields', None)

		if not filter_fields:
			return queryset

		for filter_field in filter_fields:
			v = request.query_params.get(filter_field, None)
			if v:
				queryset = queryset.filter(**{filter_field: v})

		return queryset
