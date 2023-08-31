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
				{ is_relevant: false, is_user_tag: true, tag: 'js', use_count: '224' },
				{
					is_relevant: true,
					is_user_tag: false,
					tag: 'html',
					use_count: '123',
				},
				{
					is_relevant: true,
					is_user_tag: false,
					tag: 'css',
					use_count: '12124',
				},
				{
					is_relevant: true,
					is_user_tag: false,
					tag: 'react',
					use_count: '21',
				},
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
				{
					is_relevant: true,
					is_user_tag: false,
					tag: 'php',
					use_count: '123',
				},
				{
					is_relevant: true,
					is_user_tag: false,
					tag: 'laravel',
					use_count: '12124',
				},
				{
					is_relevant: true,
					is_user_tag: false,
					tag: 'vue',
					use_count: '21',
				},
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
