import { IAnswer, IModelType } from '@/types'
import { CommentCard } from '../CommentCard'

export const CommentList = ({
	answerData,
	handleDelete,
}: {
	answerData: IAnswer
	handleDelete?: ({ id, model }: { id: number; model: IModelType }) => void
}) => {
	return answerData.comments.map((comment) => (
		<CommentCard
			key={comment.id + comment.creation_date}
			comment={comment}
			answerData={answerData}
			handleDelete={handleDelete}
		/>
	))
}
