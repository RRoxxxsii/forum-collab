import punq
from forum import repository

container = punq.Container()
container.register(repository.AbstractLikeDislikeRepository, repository.LikeDislikeRepository)
container.register(repository.AbsractThemeTagRepository, repository.ThemeTagRepository)
container.register(repository.AbstractQuestionRepository, repository.QuestionRepository)
container.register(repository.AbstractAnswerRepository, repository.AnswerRepository)
container.register(repository.AbstractCommentRepository, repository.CommentRepository)
