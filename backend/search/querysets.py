from django.contrib.postgres.search import (SearchHeadline, SearchQuery,
                                            SearchRank, SearchVector)
from django.db.models import QuerySet

from forum.models import Question


class SearchQueryset:

    @staticmethod
    def make_suggestions(query: str) -> QuerySet:
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
