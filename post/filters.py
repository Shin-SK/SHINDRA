# filters.py
import django_filters
from .models import Post

class PostFilter(django_filters.FilterSet):
    # カテゴリslug
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='iexact')
    # タグslug
    tag = django_filters.CharFilter(method='filter_by_tag')
    # フリーワード検索
    search = django_filters.CharFilter(method='filter_by_search')

    class Meta:
        model = Post
        fields = []  # ここはフィールド指定しなくてもOK、methodで書くパターン

    def filter_by_tag(self, queryset, name, value):
        # 例えば M2M の Tag で slug が value のもの
        return queryset.filter(tags__slug=value)

    def filter_by_search(self, queryset, name, value):
        # title や content に value が含まれるものを検索
        return queryset.filter(title__icontains=value) | queryset.filter(content__icontains=value)
