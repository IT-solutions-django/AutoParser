import django_filters
from itertools import chain
from .models import AucCarsJapan, AucCarsChina, AucCarsKorea
from .serializers import AucCarsSerializer


class AucCarsFilter(django_filters.FilterSet):
    year = django_filters.RangeFilter()
    price = django_filters.RangeFilter()
    brand = django_filters.CharFilter(lookup_expr="icontains")
    country = django_filters.CharFilter(method="filter_by_country")

    def filter_by_country(self, queryset, name, value):
        country_map = {
            "japan": AucCarsJapan,
            "china": AucCarsChina,
            "korea": AucCarsKorea,
        }
        model = country_map.get(value.lower())
        if model:
            return queryset.filter(id__in=model.objects.values_list("id", flat=True))
        return queryset

    class Meta:
        model = AucCarsJapan 
        fields = ["year", "price", "brand", "country"]