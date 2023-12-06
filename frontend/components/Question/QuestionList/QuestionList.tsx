'use client'
import { QuestionCard } from '@/components/Question/QuestionCard'
import { useIntersectionObserver } from '@/lib/hooks/useIntersectionObserver'
import { CategoryContext } from '@/providers/CategoryProvider'
import { fetchQuestions } from '@/shared/api/fetchData'
import { FetchStatusType, IQuestion } from '@/types'

import { Error } from '@mui/icons-material'
import { Box, Skeleton, Typography } from '@mui/material'
import { useContext, useEffect, useRef, useState } from 'react'

export const QuestionList = () => {
	const [questions, setQuestions] = useState<IQuestion[]>([])
	const [pageIndex, setPageIndex] = useState(0)
	const [isLastPage, setIsLastPage] = useState(false)
	const [listLoadingState, setListLoadingState] = useState<FetchStatusType>()

	const { category } = useContext(CategoryContext)

	const fetchQuestionList = async ({
		page,
		action,
	}: {
		page: number
		action: 'change' | 'add'
	}) => {
		//reset the questions array on refetch
		if (isLastPage) return
		setListLoadingState('loading')
		try {
			const response: Awaited<IQuestion[] | string> =
				await fetchQuestions<IQuestion>({
					category: category,
					page: page,
				})
			if (response.length < 10) setIsLastPage(true)
			//if the response is array then it is the right result
			if (Array.isArray(response) && typeof response !== 'string') {
				if (action === 'add') setQuestions((prev) => [...prev, ...response])

				if (action === 'change') {
					setQuestions([])
					setQuestions(response)
				}
				setListLoadingState('success')
			} else {
				setListLoadingState('error')
			}
		} catch (error) {
			setListLoadingState('error')
		}
	}

	const bottom = useRef<null | any>(null)
	const entry = useIntersectionObserver(bottom, {
		threshold: 0,
		root: null,
		rootMargin: '0px',
	})
	const isVisible = !!entry?.isIntersecting

	useEffect(() => {
		setPageIndex((prev) => (prev += 1))
	}, [isVisible])

	useEffect(() => {
		fetchQuestionList({ page: pageIndex, action: 'add' })
	}, [pageIndex])

	useEffect(() => {
		fetchQuestionList({ page: 0, action: 'change' })
		setPageIndex(0)
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
					<QuestionCard
						isCard={true}
						key={questionData.id}
						questionData={questionData}
					/>
				))
			) : (
				<>
					{Array.from({ length: 10 }).map((_, index) => (
						<Skeleton
							key={index}
							sx={{ mb: 2, borderRadius: 1 }}
							variant='rectangular'
							width={'100%'}
							height={210}
						/>
					))}
				</>
			)}
			<div className='h-4' ref={bottom} />
		</>
	)
}
