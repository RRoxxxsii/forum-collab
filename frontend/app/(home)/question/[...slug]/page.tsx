'use client'
import { QuestionItemRating } from '@/features/QuestionItemRating'
import { BASE_URL } from '@/shared/constants'
import { IAnswer, IQuestion } from '@/types/types'
import { TiptapEditor } from '@/widgets/TiptapEditor'
import {
	ArrowDownward,
	ArrowDownwardOutlined,
	ArrowUpward,
	ArrowUpwardOutlined,
	Bookmark,
	BookmarkOutlined,
	Comment,
	Edit,
	MoreHoriz,
	Report,
	Share,
	ShareOutlined,
} from '@mui/icons-material'
import {
	Avatar,
	Box,
	Button,
	Checkbox,
	Chip,
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
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useEffect, useState } from 'react'
import { Comment as CommentComponent } from '@/widgets/Comment'
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
	async function addAnswer() {
		try {
			const response = await fetch(`${BASE_URL}/forum/answer-question/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ question: id, answer: answerContent }),
			})
			if (response.ok) {
				const data = await response.json()
				fetchQuestion()
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
								<QuestionItemRating
									questionData={questionData}
									setDislike={dislikeQuestion}
									setLike={likeQuestion}
								/>
							</Box>
							<Box sx={{ padding: 1.5 }}>
								<Box sx={{ mb: 2, ml: 1 }}>
									<UserInformation questionData={questionData} />
									<Typography variant='h6'>{questionData?.title}</Typography>
									<Typography
										sx={{ mb: 2 }}
										variant='body1'
										dangerouslySetInnerHTML={{
											__html: questionData?.content ?? 'error',
										}}
									/>
									<Box>
										{questionData.tags.map((tag) => (
											<Chip label={tag.tag_name} />
										))}
									</Box>
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
									onClose={handleClose}>
									<MenuItem
										onClick={handleClose}
										sx={{ width: '100%', height: 36 }}>
										<Link href={`edit`} className='flex'>
											<Edit sx={{ mr: 1 }} />
											<Typography>Редактировать</Typography>
										</Link>
									</MenuItem>
									<MenuItem
										onClick={handleClose}
										sx={{ width: '100%', height: 36 }}>
										<Link href={`edit`} className='flex'>
											<Report sx={{ mr: 1 }} />
											<Typography>Пожаловаться</Typography>
										</Link>
									</MenuItem>
									<Divider />
									<MenuItem
										onClick={handleClose}
										sx={{ width: '100%', height: 36 }}>
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
					<Box sx={{ px: 3, py: 2, width: '100%', pb: 30 }}>
						<Typography
							variant='caption'
							color={'GrayText'}
							sx={{ display: 'flex', alignItems: 'center' }}>
							Ответить на вопрос как,
							<Typography variant='caption' sx={{ ml: 1 }} color={'lightblue'}>
								Гость
							</Typography>
						</Typography>
						<TiptapEditor
							type='answer'
							content={answerContent}
							setContent={setAnswerContent}
						/>
						<Button
							sx={{ mt: 1, mb: 3, width: 220, height: 50 }}
							variant='outlined'
							onClick={addAnswer}>
							Ответить
						</Button>
						{questionData.answers.map((answer) => (
							<AnswerItem key={answer.id} answerData={answer} />
						))}
					</Box>
				</Paper>
			)}
		</Box>
	)
}

const UserInformation = ({ questionData }: { questionData: IQuestion }) => {
	return (
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
				{questionData?.user?.username || 'Гость'}
			</Typography>
			<Typography sx={{ color: 'GrayText' }} variant='caption'>
				{dayjs(questionData?.creation_date).format('DD-MM-YYYY')}
			</Typography>
		</Box>
	)
}

function AnswerItem({ answerData }: { answerData: IAnswer }) {
	const likeComment = async ({ id }: { id: number }) => {
		try {
			const response = await fetch(`/api/forum/like`, {
				body: JSON.stringify({ id: id, model: 'answer' }),
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
			})
			if (response.ok) {
				const data = await response.json()
				console.log(data)
				return
			}
			return null
		} catch (error) {
			console.log(error)
		}
	}
	const dislikeComment = async ({ id }: { id: number }) => {
		try {
			const response = await fetch(`/api/forum/dislike`, {
				body: JSON.stringify({ id: id, model: 'answer' }),
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
			})
			if (response.ok) {
				const data = await response.json()
				console.log(data)
				return
			}
			return null
		} catch (error) {
			console.log(error)
		}
	}

	const [isCommenting, setIsCommenting] = useState<boolean>(false)

	return (
		<>
			<Box
				className='bg-zinc-800 p-2 rounded-md'
				sx={{ px: 3, py: 2, width: '100%', mb: 2 }}>
				<Box sx={{ display: 'flex', alignItems: 'flex-start' }}>
					<Avatar
						sx={{
							width: 32,
							height: 32,
							fontSize: 12,
							bgcolor: red[500],
							marginRight: 1,
						}}
						aria-label='recipe'>
						R
					</Avatar>
					<Box sx={{ width: '100%' }}>
						<Box sx={{ display: 'flex', ml: 1 }}>
							<Typography sx={{ marginRight: 1 }} variant='caption'>
								{answerData?.user?.username || 'Гость'}
							</Typography>
							<Typography sx={{ color: 'GrayText' }} variant='caption'>
								{dayjs(answerData?.creation_date).format('DD-MM-YYYY')}
							</Typography>
						</Box>
						<Typography
							className='comment'
							sx={{ ml: 1 }}
							dangerouslySetInnerHTML={{ __html: answerData?.answer }}
							variant='body1'
						/>
						<Box
							sx={{
								display: 'flex',
								alignItems: 'center',
							}}>
							<Checkbox
								icon={<ArrowUpwardOutlined />}
								checkedIcon={<ArrowUpward />}
								onClick={() => likeComment({ id: answerData.id })}
							/>
							{answerData.rating.like_amount - answerData.rating.dislike_amount}
							<Checkbox
								icon={<ArrowDownwardOutlined />}
								checkedIcon={<ArrowDownward />}
								onClick={() => dislikeComment({ id: answerData.id })}
							/>
							<FormControlLabel
								control={
									<IconButton
										onClick={() => setIsCommenting((state) => (state = !state))}
										sx={{ ml: 1, mr: 0.5 }}>
										<Comment />
									</IconButton>
								}
								label='Ответить'
							/>
							<IconButton>
								<MoreHoriz sx={{ width: 16, height: 16 }} />
							</IconButton>
						</Box>
					</Box>
					<Button variant='outlined'>Отметить ответ решающим</Button>
				</Box>
			</Box>
			{isCommenting && <CommentComponent answerData={answerData} />}
		</>
	)
}
