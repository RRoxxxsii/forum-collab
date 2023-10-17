'use client'
import { QuestionItemContent } from '@/entities/QuestionItemContent'
import { QuestionItemActions } from '@/features/QuestionItemActions'
import { QuestionItemRating } from '@/features/QuestionItemRating/QuestionItemRating'
import { CategoryContext } from '@/providers/CategoryProvider'
import { UserDetailsContext } from '@/providers/UserDetailsProvider'
import { Dislike, Like } from '@/shared/api/changeRating'
import { fetchQuestions } from '@/shared/api/fetchData'
import { transliterate } from '@/shared/transliterate'
import { IQuestion, ITag } from '@/types/types'
import { Error } from '@mui/icons-material'
import { Box, Card, Skeleton, Typography } from '@mui/material'
import Link from 'next/link'
import { useContext, useEffect, useState } from 'react'

export const QuestionList = () => {
	const [questions, setQuestions] = useState<IQuestion[]>([])
	const [listLoadingState, setListLoadingState] = useState<
		'loading' | 'success' | 'error'
	>()
	const { category } = useContext(CategoryContext)

	const fetchQuestionList = async () => {
		setQuestions([])
		setListLoadingState('loading')
		try {
			const response = await fetchQuestions({ category: category })

			if ('id' in response) {
				setQuestions(response)
				setListLoadingState('success')
			} else {
				setListLoadingState('error')
			}
		} catch (error) {
			setListLoadingState('error')
		}
	}

	useEffect(() => {
		fetchQuestionList()
	}, [category])

	if (listLoadingState === 'error') {
		return (
			<>
				<Typography sx={{ fontSize: 24, textAlign: 'center' }}>
					При получении списка вопросов возникла ошибка. Попробуйте попытку
					позже
				</Typography>
				<Box sx={{ width: '100%', display: 'flex', justifyContent: 'center' }}>
					<Error sx={{ width: 36, height: 36 }} />
				</Box>
			</>
		)
	}

	return (
		<>
			{questions.length !== 0 ? (
				questions.map((questionData: IQuestion) => (
					<QuestionCard key={questionData.id} questionData={questionData} />
				))
			) : (
				<>
					{Array.from({ length: 10 }).map((_, index) => (
						<Skeleton
							sx={{ mb: 2, borderRadius: 1 }}
							variant='rectangular'
							width={'100%'}
							height={210}
							key={index}
						/>
					))}
				</>
			)}
		</>
	)
}

const QuestionCard = ({ questionData }: { questionData: IQuestion }) => {
	const { userDetails } = useContext(UserDetailsContext)

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
					model='question'
					questionData={questionData}
					profileData={userDetails}
					setDislike={() => Dislike({ id: questionData.id, model: 'question' })}
					setLike={() => Like({ id: questionData.id, model: 'question' })}
				/>
				<Box sx={{ width: '100%', ml: 1 }}>
					<QuestionItemContent questionData={questionData} />
					<QuestionItemActions questionData={questionData} />
				</Box>
			</Link>
		</Card>
	)
}
