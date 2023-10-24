from django.contrib.postgres.search import (SearchHeadline, SearchQuery,
                                            SearchRank, SearchVector)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from forum.models import Question
from forum.serializers import ListQuestionSerializer


class SearchResultAPIView(ListAPIView):
    """
    Полнотекстовой поиск, реализующий GET-method через 'q'
    query-parameter.
    """
    permission_classes = [AllowAny]
    serializer_class = ListQuestionSerializer

    q = openapi.Parameter(name='sort', in_=openapi.IN_QUERY,
                          description="Поисковая строка",
                          type=openapi.TYPE_STRING, required=False)

    @swagger_auto_schema(manual_parameters=[q, ])
    def get_queryset(self):
        query = self.request.query_params.get('q')
        search_vector = (
                SearchVector('title', weight='A') +
                SearchVector('content', weight='B') +
                SearchVector('user__user_name', weight='D') +
                SearchVector('tags__tag_name', weight='C')
        )
        search_query = SearchQuery(query)
        search_headline = SearchHeadline('title', search_query)

        qs = (Question.objects.annotate(
            search=search_vector, rank=SearchRank(search_vector, search_query)
        ).annotate(
            headline=search_headline
        ).filter(
            search=search_query
        ).order_by('-rank'))[:10]

        return qs
