'use client'
import { AnswerCreateForm } from '@/features/AnswerCreateForm'
import { QuestionActionsMenu } from '@/features/QuestionActionsMenu'
import { QuestionItemRating } from '@/features/QuestionItemRating'
import { QuestionContent } from '@/shared/QuestionContent'
import { IQuestion, IUser } from '@/types/types'
import { AnswerList } from '@/widgets/AnswerList'
import { Box, Divider, Paper, Typography } from '@mui/material'
import { usePathname } from 'next/navigation'
import { Suspense, useEffect, useState } from 'react'
import QuestionLoading from './loading'

export default function QuestionPage() {
	const pathname = usePathname()

	const id = (pathname?.match(/\/question\/(\d+)/)?.[0] || '').replace(
		'/question/',
		''
	)

	const dislikeQuestion = async ({ id }: { id: number }) => {
		try {
			const response = await fetch(`/api/forum/dislike`, {
				method: 'POST',
				body: JSON.stringify({ id: id, model: 'question' }),
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
				method: 'POST',
				body: JSON.stringify({ id: id, model: 'question' }),
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
	const [profileData, setProfileData] = useState<IUser | null>(null)

	useEffect(() => {
		fetchQuestion()
		fetchUser()
	}, [])

	async function fetchQuestion() {
		try {
			const response = await fetch(`/api/forum/questions`, {
				method: 'POST',
				body: JSON.stringify({ page_id: id }),
				headers: {
					'Content-Type': 'application/json',
				},
			})

			const result = await response.json()
			if (!response.ok) {
				throw new Error(result)
			}

			setQuestionData(result)
		} catch (error) {
			console.log(error)
		}
	}

	async function fetchUser() {
		try {
			const response = await fetch(`/api/account/me/`)

			const result = await response.json()
			if (!response.ok) {
				throw new Error(result)
			}

			setProfileData(result)
		} catch (error) {
			console.log(error)
		}
	}

	return (
		<Suspense fallback={<QuestionLoading />}>
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
							<AnswerCreateForm
								questionData={questionData}
								setQuestionData={setQuestionData}
								pageId={id}
							/>
							<AnswerList questionData={questionData} />
						</Box>
					</Paper>
				)}
			</Box>
		</Suspense>
	)
}
