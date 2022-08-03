from django_filters import rest_framework as filters
from reviews.models import Title


class TitlesFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    category = filters.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )
    genre = filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
<<<<<<< HEAD
        fields = ['name', 'year', 'genre', 'category']
=======
        fields = ['name', 'year', 'genre', 'category']
>>>>>>> 3ec51f96fec84ae23b5be1f6ba526b3b579c98bb
