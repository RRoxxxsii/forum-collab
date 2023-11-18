from forum.models import Question
from forum.repository import QuestionRepository, ThemeTagRepository


class QuestionService:
    question_repository = QuestionRepository
    tag_repository = ThemeTagRepository

    @classmethod
    def create_question(cls, user, title, content, tags, images) -> Question:
        question = cls.question_repository.create_question(title=title, content=content, user=user)
        tags = cls.tag_repository.create_tags(tags=tags, user=user)

        if images:
            cls.question_repository.add_attachments(parent=question, attachments=images)

        cls.question_repository.add_tags(question=question, tags=tags)
        return question
