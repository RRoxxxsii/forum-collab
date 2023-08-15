import { QuestionItemContent } from '@/entities/QuestionItemContent'
import { QuestionItemActions } from '@/features/QuestionItemActions'
import { QuestionItemRating } from '@/features/QuestionItemRating/QuestionItemRating'
import { QuestionItemWrapper } from '@/shared/QuestionItemWrapper'
import { IQuestionItem } from '@/types/types'
import { Box } from '@mui/material'

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
				<QuestionItemWrapper href={`question/${question.id}`} key={question.id}>
					<QuestionItemRating />
					<Box sx={{ width: '100%', ml: 1 }}>
						<QuestionItemContent questionData={question} />
						<QuestionItemActions chips={question.chips} />
					</Box>
				</QuestionItemWrapper>
			))}
		</>
	)
}
