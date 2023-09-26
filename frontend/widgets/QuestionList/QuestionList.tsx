'use client'
import { QuestionItemContent } from '@/entities/QuestionItemContent'
import { QuestionItemActions } from '@/features/QuestionItemActions'
import { QuestionItemRating } from '@/features/QuestionItemRating/QuestionItemRating'
import { QuestionItemWrapper } from '@/shared/QuestionItemWrapper'
import { BASE_URL } from '@/shared/constants'
import { IQuestion, ITag } from '@/types/types'
import { Box } from '@mui/material'
import { useEffect, useState } from 'react'

export const QuestionList = () => {
	const [questions, setQuestions] = useState<IQuestion[]>([])

	const fetchQuestionList = async () => {
		try {
			const response = await fetch(`${BASE_URL}/forum/questions/`)
			const questionsData = await response.json()

			setQuestions(questionsData)
		} catch (error) {
			console.log(error)
		}
	}

	useEffect(() => {
		fetchQuestionList()
	}, [])

	return (
		<>
			{questions.reverse().map((question: IQuestion) => (
				<QuestionItemWrapper
					href={`/question/${question.id}/${
						question.title
					}/?tags=${question.tags.map((tag: ITag) => tag.tag_name)}`}
					key={question.id}>
					<QuestionItemRating rating={question.rating} />
					<Box sx={{ width: '100%', ml: 1 }}>
						<QuestionItemContent questionData={question} />
						<QuestionItemActions questionData={question} />
					</Box>
				</QuestionItemWrapper>
			))}
		</>
	)
}
