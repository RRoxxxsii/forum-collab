import { QuestionItemContent } from '@/entities/QuestionItemContent'
import { QuestionItemActions } from '@/features/QuestionItemActions/QuestionItemActions'
import { QuestionItemWrapper } from '@/shared/QuestionItemWrapper'

interface IUser {
	avatar: string
	username: string
	email: string
}

export interface IChip {
	key: number
	label: string
}

export interface IQuestionItem {
	id: string | number
	user: IUser
	title: string
	description: string
	chips: IChip[]
}

export const QuestionList = () => {
	const questions: IQuestionItem[] = [
		{
			id: 0,
			user: { avatar: '', email: 'example@example.com', username: 'example' },
			chips: [
				{ key: 0, label: 'jquery' },
				{ key: 1, label: 'react' },
			],
			description: 'test description',
			title: 'test title',
		},
		{
			id: 1,
			user: { avatar: '', email: 'example@example.com', username: 'example' },
			chips: [
				{ key: 0, label: 'laravel' },
				{ key: 1, label: 'php' },
				{ key: 1, label: 'js' },
			],
			description: 'test description',
			title: 'test title',
		},
		{
			id: 2,
			user: { avatar: '', email: 'example@example.com', username: 'example' },
			chips: [{ key: 0, label: 'html' }],
			description: 'test description',
			title: 'test title',
		},
	]

	return (
		<>
			{questions.map((question) => (
				<QuestionItemWrapper key={question.id}>
					<QuestionItemContent questionData={question} />
					<QuestionItemActions chips={question.chips} />
				</QuestionItemWrapper>
			))}
		</>
	)
}
