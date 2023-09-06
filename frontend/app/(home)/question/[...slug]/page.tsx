'use client'
import { QuestionItemRating } from '@/features/QuestionItemRating'
import { BASE_URL } from '@/shared/constants'
import { IAnswer, IQuestion } from '@/types/types'
import { Bookmark, Edit, MoreHoriz, Share } from '@mui/icons-material'
import {
	Avatar,
	Box,
	Button,
	Divider,
	IconButton,
	Paper,
	Typography,
} from '@mui/material'
import { red } from '@mui/material/colors'
import dayjs from 'dayjs'
import { usePathname } from 'next/navigation'
import { useEffect, useState } from 'react'

export default function QuestionPage() {
	const pathname = usePathname()
	console.log(pathname)
	const id =
		pathname?.match(/\/question\/(\d+)/)[0].replace('/question/', '') ?? ''
	console.log(id)

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
				console.log(data)
			} else {
				console.log(`Failed to fetch data. Status: ${response.status}`)
			}
		} catch (error) {
			console.log(error)
		}
	}

	return (
		<Box sx={{ minHeight: '80vh' }}>
			{questionData && (
				<Paper sx={{ px: 3, py: 2, maxWidth: 1280 }}>
					<Box sx={{}}>
						<Box sx={{ display: 'flex' }}>
							<Box sx={{ justifyContent: 'center' }}>
								<QuestionItemRating rating={questionData?.rating} />
							</Box>
							<Box sx={{ padding: 1.5 }}>
								<Box sx={{ mb: 2, ml: 1 }}>
									<Box sx={{ display: 'flex' }}>
										<Avatar
											sx={{
												width: 18,
												height: 18,
												fontSize: 12,
												bgcolor: red[500],
												marginRight: 1,
											}}
											aria-label='recipe'>
											R
										</Avatar>
										<Typography sx={{ marginRight: 1 }} variant='caption'>
											{questionData?.user}
										</Typography>
										<Typography sx={{ color: 'GrayText' }} variant='caption'>
											{dayjs(questionData?.creation_date).format('DD-MM-YYYY')}
										</Typography>
									</Box>
									<Typography variant='h6'>{questionData?.title}</Typography>
									<Typography
										variant='body1'
										dangerouslySetInnerHTML={{
											__html: questionData?.content ?? 'error',
										}}
									/>
								</Box>
								<IconButton>
									<Edit />
								</IconButton>
								<IconButton>
									<Share />
								</IconButton>
								<IconButton>
									<Bookmark />
								</IconButton>
								<IconButton>
									<MoreHoriz />
								</IconButton>
							</Box>
						</Box>
					</Box>
					<Divider />
					<Typography
						variant='h6'
						sx={{ my: 2, display: 'flex', alignItems: 'center', mx: 1 }}>
						Ответы:
						<Typography
							className='rounded-full bg-neutral-700 h-5 w-5 flex items-center justify-center ml-4'
							sx={{ ml: 1 }}>
							{questionData.answers.length}
						</Typography>
					</Typography>
					<Box sx={{ display: 'flex', mb: 4 }}>
						{questionData.answers.map((answer) => (
							<AnswerItem key={answer.id} answerData={answer} />
						))}
					</Box>
				</Paper>
			)}
		</Box>
	)
}

function AnswerItem({ answerData }: { answerData: IAnswer }) {
	return (
		<>
			<Box
				className='bg-zinc-800 p-2 rounded-md'
				sx={{ px: 3, py: 1, width: '100%' }}>
				<Box sx={{ display: 'flex', alignItems: 'center' }}>
					<Box sx={{ justifyContent: 'center' }}>
						<QuestionItemRating rating={answerData?.rating} />
					</Box>
					<Box sx={{ width: '100%' }}>
						<Box sx={{ display: 'flex' }}>
							<Avatar
								sx={{
									width: 18,
									height: 18,
									fontSize: 12,
									bgcolor: red[500],
									marginRight: 1,
								}}
								aria-label='recipe'>
								R
							</Avatar>
							<Typography sx={{ marginRight: 1 }} variant='caption'>
								{answerData?.user}
							</Typography>
							<Typography sx={{ color: 'GrayText' }} variant='caption'>
								{dayjs(answerData?.creation_date).format('DD-MM-YYYY')}
							</Typography>
						</Box>
						<Typography variant='h6'>{answerData?.answer}</Typography>
					</Box>
					<Button variant='outlined'>Отметить ответ решающим</Button>
				</Box>
			</Box>
		</>
	)
}
