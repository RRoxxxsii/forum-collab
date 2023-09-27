'use client'
import { QuestionItemContent } from '@/entities/QuestionItemContent'
import { QuestionItemActions } from '@/features/QuestionItemActions'
import { QuestionItemRating } from '@/features/QuestionItemRating/QuestionItemRating'
import { BASE_URL } from '@/shared/constants'
import { IQuestion, ITag } from '@/types/types'
import { Box, Card, Link } from '@mui/material'
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
			{questions.reverse().map((questionData: IQuestion) => (
				<QuestionCard questionData={questionData} />
			))}
		</>
	)
}

const QuestionCard = ({ questionData }: { questionData: IQuestion }) => {
	const dislikeQuestion = async ({ id }: { id: number }) => {
		try {
			const response = await fetch(`/api/forum/dislike`, {
				body: JSON.stringify({ id: id, model: 'question' }),
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
			})
			const data = await response.json()

			if (!response.ok) {
				throw new Error(data)
			}

			return data
		} catch (error) {
			console.log(error)
		}
	}

	const likeQuestion = async ({ id }: { id: number }) => {
		try {
			const response = await fetch(`/api/forum/like`, {
				body: JSON.stringify({ id: id, model: 'question' }),
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
			})

			const data = await response.json()

			if (!response.ok) {
				throw new Error(data)
			}

			return data
		} catch (error) {
			console.log(error)
		}
	}

	return (
		<Card
			key={questionData.id}
			sx={{
				width: 'clamp(300px, 100%, 1200px)',
				transition: 'border-color 0.3s ease-in-out',
				border: '1px solid transparent',
				'&:hover': { border: 1, transition: 0.3, borderColor: 'teal' },
				cursor: 'pointer',
				mb: 2,
				p: 0.8,
			}}>
			<Link
				href={`/question/${questionData.id}/${
					questionData.title
				}/?tags=${questionData.tags.map((tag: ITag) => tag.tag_name)}`}
				className='flex'>
				<QuestionItemRating
					questionData={questionData}
					setDislike={dislikeQuestion}
					setLike={likeQuestion}
				/>
				<Box sx={{ width: '100%', ml: 1 }}>
					<QuestionItemContent questionData={questionData} />
					<QuestionItemActions questionData={questionData} />
				</Box>
			</Link>
		</Card>
	)
}
