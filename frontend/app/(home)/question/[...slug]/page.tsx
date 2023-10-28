'use client'
import { AnswerCreateForm } from '@/features/AnswerCreateForm'
import { QuestionActionsMenu } from '@/features/QuestionActionsMenu'
import { QuestionItemRating } from '@/features/QuestionItemRating'
import { QuestionContent } from '@/shared/QuestionContent'
import { ChangeRating } from '@/shared/api/changeRating'
import { fetchMe, fetchQuestion } from '@/shared/api/fetchData'
import { IQuestion, IUser } from '@/types'
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
	const [questionData, setQuestionData] = useState<IQuestion | null>(null)
	const [profileData, setProfileData] = useState<IUser | null>(null)

	useEffect(() => {
		fetchQuestion({ id: id, setQuestionData: setQuestionData })
		fetchMe({ setProfileData: setProfileData })
	}, [])

	const handleQuestionRating = () => {}

	return (
		<Suspense fallback={<QuestionLoading />}>
			<Box sx={{ minHeight: '80vh' }}>
				{questionData && (
					<Paper sx={{ maxWidth: 1280 }}>
						<Box sx={{ px: 3, py: 2 }}>
							<Box sx={{ display: 'flex' }}>
								<Box sx={{ justifyContent: 'center' }}>
									<QuestionItemRating
										model='question'
										questionData={questionData}
										handleRating={handleQuestionRating}
										profileData={profileData}
									/>
								</Box>
								<Box sx={{ padding: 1.5 }}>
									<QuestionContent questionData={questionData} />
									<QuestionActionsMenu
										profileData={profileData}
										questionData={questionData}
									/>
								</Box>
							</Box>
						</Box>
						<Divider />
						{/* Ответы */}
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
								profileData={profileData}
								questionData={questionData}
								setQuestionData={setQuestionData}
							/>
							<AnswerList
								setQuestionData={setQuestionData}
								questionData={questionData}
							/>
						</Box>
					</Paper>
				)}
			</Box>
		</Suspense>
	)
}
