'use client'
import { QuestionItemRating } from '@/features/QuestionItemRating'
import { BASE_URL } from '@/shared/constants'
import { IAnswer, IQuestion } from '@/types/types'
import { TiptapEditor } from '@/widgets/TiptapEditor'
import {
	Bookmark,
	BookmarkOutlined,
	Edit,
	EditOutlined,
	MoreHoriz,
	Report,
	ReportOutlined,
	Share,
	ShareOutlined,
} from '@mui/icons-material'
import {
	Avatar,
	Box,
	Button,
	Checkbox,
	Divider,
	FormControlLabel,
	IconButton,
	Menu,
	MenuItem,
	Paper,
	Typography,
} from '@mui/material'
import { red } from '@mui/material/colors'
import dayjs from 'dayjs'
import { usePathname } from 'next/navigation'
import { useEffect, useState } from 'react'

export default function QuestionPage() {
	const pathname = usePathname()

	const id =
		pathname.match(/\/question\/(\d+)/)[0]?.replace('/question/', '') ?? ''

	const [questionData, setQuestionData] = useState<IQuestion | null>(null)

	const [answerContent, setAnswerContent] = useState<string>('')

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

	const [moreButtonEl, setmoreButtonEl] = useState<HTMLElement | null>(null)
	const moreDropdownOpen = Boolean(moreButtonEl)
	const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
		setmoreButtonEl(event.currentTarget)
	}
	const handleClose = () => {
		setmoreButtonEl(null)
	}

	return (
		<Box sx={{ minHeight: '80vh' }}>
			{questionData && (
				<Paper sx={{ maxWidth: 1280 }}>
					<Box sx={{ px: 3, py: 2 }}>
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
								<FormControlLabel
									control={
										<Checkbox
											icon={<ShareOutlined />}
											checkedIcon={<Share />}
										/>
									}
									label='Поделиться'
								/>
								<FormControlLabel
									control={
										<Checkbox
											icon={<BookmarkOutlined />}
											checkedIcon={<Bookmark />}
										/>
									}
									label='Избранное'
								/>
								<IconButton
									id='more'
									aria-controls={moreDropdownOpen ? 'more options' : undefined}
									aria-haspopup='true'
									aria-expanded={moreDropdownOpen ? 'true' : undefined}
									onClick={handleClick}>
									<MoreHoriz />
								</IconButton>
								<Menu
									id='more options'
									anchorEl={moreButtonEl}
									open={moreDropdownOpen}
									onClose={handleClose}
									MenuListProps={{
										'aria-labelledby': 'basic-button',
									}}>
									<MenuItem onClick={handleClose}>
										<FormControlLabel
											control={
												<Checkbox
													icon={<EditOutlined />}
													checkedIcon={<Edit />}
												/>
											}
											label='Редактировать'
										/>
									</MenuItem>
									<MenuItem onClick={handleClose}>
										<FormControlLabel
											control={
												<Checkbox
													icon={<ReportOutlined />}
													checkedIcon={<Report />}
												/>
											}
											label='Пожаловаться'
										/>
									</MenuItem>
									<Divider />
									<MenuItem onClick={handleClose}>
										<FormControlLabel
											control={<Checkbox />}
											label='Включить уведомления'
										/>
									</MenuItem>
								</Menu>
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
					<Box sx={{ px: 3, py: 2, width: '100%' }}>
						<Typography
							variant='caption'
							color={'GrayText'}
							sx={{ display: 'flex', alignItems: 'center' }}>
							Ответить на вопрос как,
							<Typography variant='caption' sx={{ ml: 1 }} color={'lightblue'}>
								usename
							</Typography>
						</Typography>
						<TiptapEditor
							height={120}
							content={answerContent}
							setContent={setAnswerContent}
						/>
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