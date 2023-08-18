from typing import Iterator

from accounts.models import NewUser
from forum.models import ThemeTag


def create_return_tags(tags: list, user: NewUser) -> Iterator[int]:
    """
    Yields tags. If tag does not exist, create it marking the tag as
    user's non-relevant tag. Returns tag ID.
    """
    for tag in tags:

        tag, created = ThemeTag.objects.get_or_create(tag=tag, defaults={
            'is_user_tag': True,
            'is_relevant': False,
            'user': user
        })

        yield tag.id
