'use client'
import { AnswerCreateForm } from '@/features/AnswerCreateForm'
import { QuestionActionsMenu } from '@/features/QuestionActionsMenu'
import { QuestionItemRating } from '@/features/QuestionItemRating'
import { QuestionContent } from '@/shared/QuestionContent'
import { BASE_URL } from '@/shared/constants'
import { IQuestion } from '@/types/types'
import { AnswerList } from '@/widgets/AnswerList'
import { Box, Divider, Paper, Typography } from '@mui/material'
import { usePathname } from 'next/navigation'
import { useEffect, useState } from 'react'
export default function QuestionPage() {
	const pathname = usePathname()

	const id = (pathname?.match(/\/question\/(\d+)/)?.[0] || '').replace(
		'/question/',
		''
	)

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

	const [questionData, setQuestionData] = useState<IQuestion | null>(null)

	useEffect(() => {
		fetchQuestion()
	}, [])

	async function fetchQuestion() {
		try {
			const response = await fetch(`${BASE_URL}/forum/questions/${id}/`)
			if (response.ok) {
				const data = await response.json()
				setQuestionData(data)
			} else {
			}
		} catch (error) {}
	}

	return (
		<Box sx={{ minHeight: '80vh' }}>
			{questionData && (
				<Paper sx={{ maxWidth: 1280 }}>
					<Box sx={{ px: 3, py: 2 }}>
						<Box sx={{ display: 'flex' }}>
							<Box sx={{ justifyContent: 'center' }}>
								<QuestionItemRating
									questionData={questionData}
									setDislike={dislikeQuestion}
									setLike={likeQuestion}
								/>
							</Box>
							<Box sx={{ padding: 1.5 }}>
								<QuestionContent questionData={questionData} />
								<QuestionActionsMenu />
							</Box>
						</Box>
					</Box>
					<Divider />
					<Typography
						variant='h6'
						sx={{ px: 3, py: 1, display: 'flex', alignItems: 'center' }}>
						Ответы:
						<Typography
							className='rounded-full bg-neutral-700 h-5 w-5 flex items-center justify-center ml-4'
							sx={{ ml: 1 }}>
							{questionData.answers.length}
						</Typography>
					</Typography>
					<Box sx={{ px: 3, py: 2, width: '100%', pb: 30 }}>
						<AnswerCreateForm pageId={id} />
						<AnswerList questionData={questionData} />
					</Box>
				</Paper>
			)}
		</Box>
	)
}
