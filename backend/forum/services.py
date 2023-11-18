from accounts.models import NewUser
from forum.models import Question
from forum.repository import QuestionRepository, ThemeTagRepository, AnswerRepository
from notifications.utils import notify


class QuestionService:
    question_repository = QuestionRepository
    tag_repository = ThemeTagRepository

    @classmethod
    def create_question(cls, user: NewUser, title: str, content: str, tags: list, images: list = None) -> Question:
        question = cls.question_repository.create_question(title=title, content=content, user=user)
        tags = cls.tag_repository.create_tags(tags=tags, user=user)

        if images:
            cls.question_repository.add_attachments(parent=question, attachments=images)

        cls.question_repository.add_tags(question=question, tags=tags)
        return question


class AnswerService:
    answer_repository = AnswerRepository

    @classmethod
    def create_answer(cls, question: Question, answer: str, images: list = None, user: NewUser = None):
        answer = cls.answer_repository.create_answer(question=question, answer=answer, user=user)

        if images:
            cls.answer_repository.add_attachments(parent=answer, attachments=images)

        notify(
            sender=user, receiver=question.user,
            text='ответил на ваш вопрос', action_obj=answer,
            target=question
        )

        return answer
