'use client'
import { QuestionCard } from '@/features/QuestionCard'
import { CategoryContext } from '@/providers/CategoryProvider'
import { fetchQuestions } from '@/shared/api/fetchData'
import { FetchStatusType, IQuestion } from '@/types'

import { Error } from '@mui/icons-material'
import { Box, Skeleton, Typography } from '@mui/material'
import { useContext, useEffect, useState } from 'react'

export const QuestionList = () => {
	const [questions, setQuestions] = useState<IQuestion[]>([])
	const [listLoadingState, setListLoadingState] = useState<FetchStatusType>()
	const { category } = useContext(CategoryContext)

	const fetchQuestionList = async () => {
		setQuestions([])
		setListLoadingState('loading')
		try {
			const response = await fetchQuestions({ category: category })

			//if the response is array then it is the right result
			if (Array.isArray(response)) {
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

	//Handling response error
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
			{/* if there is data we show it, otherwise we show skeletons */}
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
