import django_filters
from django.db.models import Count, QuerySet
from django.http import HttpRequest

from .models import Post


class PostSearchFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    publisher = django_filters.CharFilter(lookup_expr="username__icontains")

    class Meta:
        model = Post
        fields = ("title", "publisher")

class PostOrderingFilter:
    @classmethod
    def filter(cls, queryset: QuerySet, value: str) -> QuerySet:
        order = cls.get_ordering(value)

        if order in Post.get_fields_name():
            if order in Post.get_related_fields_name():
                value = value + "_count"
                annotate_dict = {order + "_count": Count(order)}
                queryset = queryset.alias(**annotate_dict)

            queryset = queryset.order_by(value)

        return queryset

    @staticmethod
    def get_ordering(name: str) -> str:
        desc = name.startswith("-")
        name = name[1:] if desc else name
        return name

def post_queryset(request: HttpRequest, queryset: QuerySet) -> QuerySet:
    order = request.GET.get("ordering")

    if request.GET.get("search") is not None:
        queryset = PostSearchFilter(request.GET, queryset).qs

    if order is not None:
        queryset = PostOrderingFilter.filter(queryset, order)

    return queryset
    