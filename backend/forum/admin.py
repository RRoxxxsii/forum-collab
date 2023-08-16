from django.contrib import admin

from .models import (AnswerComment, Question, QuestionAnswer,
                     QuestionAnswerRating, QuestionRating, ThemeTag)

admin.site.register(Question)
admin.site.register(QuestionAnswer)
admin.site.register(QuestionRating)
admin.site.register(QuestionAnswerRating)
admin.site.register(AnswerComment)
admin.site.register(ThemeTag)
