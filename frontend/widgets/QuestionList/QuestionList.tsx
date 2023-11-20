'use client'
import { QuestionCard } from '@/features/QuestionCard'
import { CategoryContext } from '@/providers/CategoryProvider'
import { fetchQuestions } from '@/shared/api/fetchData'
import { FetchStatusType, IQuestion } from '@/types'

import { Error } from '@mui/icons-material'
import { Box, Skeleton, Typography } from '@mui/material'
import { useContext, useEffect, useRef, useState } from 'react'

export const QuestionList = () => {
	const [questions, setQuestions] = useState<IQuestion[]>([])
	const [listLoadingState, setListLoadingState] = useState<FetchStatusType>()
	const { category } = useContext(CategoryContext)

	const fetchQuestionList = async ({ page }: { page: number }) => {
		//reset the questions array on refetch
		setListLoadingState('loading')
		const pageNumber = page * 10
		try {
			const response = await fetchQuestions({
				category: category,
				limit: pageNumber,
			})

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

	const bottom = useRef<null | any>(null)

	useEffect(() => {
		fetchQuestionList({ page: 1 })
	}, [category])

	const [pageIndex, setPageIndex] = useState(1)

	useEffect(() => {
		const observer = new IntersectionObserver(() => {
			setPageIndex((pageIndex) => (pageIndex += 1))
			fetchQuestionList({ page: pageIndex })
		})
		observer.observe(bottom.current)
		return () => {
			if (bottom.current) {
				observer.unobserve(bottom.current)
			}
		}
	}, [bottom])

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
			<div className='h-4' ref={bottom} />
		</>
	)
}
