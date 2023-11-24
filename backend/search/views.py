from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from forum.serializers import ListQuestionSerializer
from search.querysets import SearchQueryset


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
        return SearchQueryset.make_suggestions(self.request.query_params.get('q'))
