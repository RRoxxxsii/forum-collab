import { QuestionItemContent } from '@/entities/QuestionItemContent'
import { QuestionItemActions } from '@/features/QuestionItemActions'
import { QuestionItemWrapper } from '@/shared/QuestionItemWrapper'
import { IQuestionItem } from '@/types/types'

export const QuestionList = () => {
	const questions: IQuestionItem[] = [
		{
			id: '0',
			user: {
				id: '0',
				avatar: '',
				email: 'example@example.com',
				username: 'example',
			},
			chips: [
				{ key: 0, label: 'jquery' },
				{ key: 1, label: 'react' },
			],
			description: 'test description',
			title: 'test title',
		},
		{
			id: '1',
			user: {
				id: '1',
				avatar: '',
				email: 'example@example.com',
				username: 'example',
			},
			chips: [
				{ key: 0, label: 'laravel' },
				{ key: 1, label: 'php' },
				{ key: 1, label: 'js' },
			],
			description: 'test description',
			title: 'test title',
		},
	]

	return (
		<>
			{questions.map((question) => (
				<QuestionItemWrapper href={question.id} key={question.id}>
					<QuestionItemContent questionData={question} />
					<QuestionItemActions chips={question.chips} />
				</QuestionItemWrapper>
			))}
		</>
	)
}
