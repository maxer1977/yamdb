from django_filters import FilterSet, CharFilter, NumberFilter

from reviews.models import Title


class BackendFilterTitle(FilterSet):
    genre = CharFilter(field_name='genre',
                       lookup_expr='slug')
    category = CharFilter(field_name='category',
                          lookup_expr='slug')
    name = CharFilter(field_name='name')
    year = NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['name', 'year', 'genre', 'category']
