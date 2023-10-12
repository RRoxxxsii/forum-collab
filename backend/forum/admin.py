from django.contrib import admin

from .models import (AnswerComment, CommentRating, Question, QuestionAnswer,
                     QuestionAnswerImages, QuestionAnswerRating,
                     QuestionImages, QuestionRating, ThemeTag)

admin.site.register(ThemeTag)
admin.site.register(QuestionImages)
admin.site.register(QuestionAnswerImages)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['amount_of_complains', 'user', 'title']
    fields = ['user', 'title', 'content', 'tags', 'creation_date', 'is_solved',
              'rating__like_amount', 'rating__dislike_amount']

    @admin.display(ordering="-creation_date")
    def amount_of_complains(self, instance):
        return instance.rating.users_complained.count()


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ['amount_of_complains', 'user', 'answer']
    fields = ['question', 'user', 'answer', 'is_solving', 'creation_date',
              'rating__like_amount', 'rating__dislike_amount']

    @admin.display(ordering="-creation_date")
    def amount_of_complains(self, instance):
        return instance.rating.users_complained.count()


@admin.register(AnswerComment)
class AnswerCommentAdmin(admin.ModelAdmin):
    list_display = ['amount_of_complains', 'user', 'comment']

    @admin.display(ordering="-creation_date")
    def amount_of_complains(self, instance):
        return instance.rating.users_complained.count()


@admin.register(QuestionRating, QuestionAnswerRating, CommentRating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['amount_of_complains', 'entity', 'user_author']

    @admin.display(ordering='-creation_date')
    def entity(self, instance):
        if isinstance(instance, QuestionRating):
            return instance.question.title
        elif isinstance(instance, QuestionAnswerRating):
            return instance.answer
        elif isinstance(instance, CommentRating):
            return instance.comment

    @admin.display
    def user_author(self, instance):
        if isinstance(instance, QuestionRating):
            return instance.question.user
        elif isinstance(instance, QuestionAnswerRating):
            return instance.answer.user
        elif isinstance(instance, CommentRating):
            return instance.comment.user

    @admin.display
    def amount_of_complains(self, instance):
        return instance.users_complained.count()
