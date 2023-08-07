import django.utils.datetime_safe
import django_filters
from django.forms import DateTimeInput
from django_filters import FilterSet, ModelMultipleChoiceFilter, IsoDateTimeFilter
from .models import Post,Category


class PostFilter(FilterSet):
    category = ModelMultipleChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Category',
    )
    fields = {'title'}
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок',
        )

    date = django_filters.IsoDateTimeFilter(
        field_name='addTime',
        lookup_expr='gt',
        label='Дата создания',
        widget=DateTimeInput(
            format='%Y-%m-%d',
            attrs={'type': 'datetime-local'}
        ),
    )






        #     'date' = DateFilter(
        #     field_name='addTime',
        #     lookup_expr='gt',
        #     label='Creation date',
        #     widget=DateInput(
        #         attrs={'type': 'date'}
        #     ),
        # ),
        # }






