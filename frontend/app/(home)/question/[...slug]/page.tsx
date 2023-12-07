'use client'
import { AnswerCreateForm } from '@/components/Answer/AnswerCreateForm'
import { AnswerList } from '@/components/Answer/AnswerList'
import {
	QuestionCardContent,
	QuestionCardMenu,
	QuestionCardRating,
} from '@/components/Question/QuestionCard/models'

import { QuestionCardTags } from '@/components/Question/QuestionCard/models/QuestionCardTags'
import { UserDeviceContext } from '@/providers/UserDeviceProvider'
import { PageWrapper } from '@/shared/PageWrapper/PageWrapper'
import { ChangeRating } from '@/shared/api/changeRating'
import { fetchMe, fetchQuestion } from '@/shared/api/fetchData'
import { IChangeRating, IQuestion, IUser } from '@/types'
import { Box, Divider, Paper, Skeleton, Typography } from '@mui/material'
import { usePathname } from 'next/navigation'
import { useContext, useEffect, useState } from 'react'

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
	}, [id])

	const handleQuestionRating = ({
		model,
		id,
		action,
		checked,
	}: IChangeRating) => {
		ChangeRating({ action: action, checked: checked, id: id, model: model })
	}

	const { userDevice } = useContext(UserDeviceContext)

	return (
		<PageWrapper>
			{questionData ? (
				<Paper sx={{ maxWidth: 1280 }}>
					<Box sx={{ px: userDevice === 'desktop' ? 3 : 1, py: 2 }}>
						<Box sx={{ display: 'flex' }}>
							<Box sx={{ justifyContent: 'center' }}>
								<QuestionCardRating
									model='question'
									questionData={questionData}
									handleRating={handleQuestionRating}
									profileData={profileData}
								/>
							</Box>
							<Box sx={{ padding: 1.5 }}>
								<QuestionCardContent questionData={questionData} />
								<QuestionCardTags questionData={questionData} />
								<QuestionCardMenu
									isCard={false}
									profileData={profileData}
									questionData={questionData}
								/>
							</Box>
						</Box>
					</Box>
					<Divider />
					<Typography
						variant='h6'
						sx={{
							px: userDevice === 'desktop' ? 3 : 1,
							py: 1,
							display: 'flex',
							alignItems: 'center',
						}}>
						Ответы:
						<Typography
							className='rounded-full bg-neutral-700 h-5 w-5 flex items-center justify-center ml-4'
							sx={{ ml: 1 }}>
							{questionData.answers.length}
						</Typography>
					</Typography>
					<Box
						sx={{
							px: userDevice === 'desktop' ? 3 : 1,
							py: 2,
							width: '100%',
							pb: 30,
						}}>
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
			) : (
				<>
					<Skeleton
						sx={{ mb: 1, maxWidth: '1280px' }}
						variant='rectangular'
						width={'100%'}
						height={380}
					/>
					<Skeleton
						variant='rectangular'
						sx={{ maxWidth: '1280px' }}
						width={'100%'}
						height={'100vh'}
					/>
				</>
			)}
		</PageWrapper>
	)
}
