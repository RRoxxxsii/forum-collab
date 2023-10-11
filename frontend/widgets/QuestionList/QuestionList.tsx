'use client'
import { QuestionItemContent } from '@/entities/QuestionItemContent'
import { QuestionItemActions } from '@/features/QuestionItemActions'
import { QuestionItemRating } from '@/features/QuestionItemRating/QuestionItemRating'
import { CategoryContext } from '@/providers/CategoryProvider'
import { BASE_URL } from '@/shared/constants'
import { transliterate } from '@/shared/transliterate'
import { IQuestion, ITag } from '@/types/types'
import { Box, Card, Skeleton } from '@mui/material'
import Link from 'next/link'
import { Suspense, useContext, useEffect, useState } from 'react'

export const QuestionList = () => {
	const [questions, setQuestions] = useState<IQuestion[]>([])
	const { category } = useContext(CategoryContext)

	const fetchQuestionList = async () => {
		setQuestions([])
		try {
			const response = await fetch(
				`${BASE_URL}/forum/questions/?limit=10&sort=${category}`
			)
			const questionsData = await response.json()

			setQuestions(questionsData)
		} catch (error) {
			console.log(error)
		}
	}

	useEffect(() => {
		fetchQuestionList()
	}, [category])

	return (
		<>
			{questions.length !== 0
				? questions.map((questionData: IQuestion) => (
						<QuestionCard key={questionData.id} questionData={questionData} />
				  ))
				: Array.from({ length: 10 }).map((_, index) => (
						<Skeleton
							sx={{ mb: 2, borderRadius: 1 }}
							variant='rectangular'
							width={'100%'}
							height={210}
							key={index}
						/>
				  ))}
		</>
	)
}

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

const QuestionCard = ({ questionData }: { questionData: IQuestion }) => {
	return (
		<Card
			key={questionData.id}
			sx={{
				width: 'clamp(300px, 100%, 1200px)',
				transition: 'border-color 0.3s ease-in-out',
				border: '1px solid transparent',
				'&:hover': { border: 1, transition: 0.3, borderColor: 'Highlight' },
				cursor: 'pointer',
				mb: 2,
				textDecoration: 'none',
				p: 0.8,
			}}>
			<Link
				href={`/question/${questionData.id}/${transliterate(
					questionData.title.replaceAll(/ /g, '_')
				)}/?tags=${questionData.tags.map((tag: ITag) => tag.tag_name)}`}
				className='flex hover:no-underline'>
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
