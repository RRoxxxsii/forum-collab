'use client'
import { IAnswer, IComment, IQuestion } from '@/types/types'
import {
	ArrowDownward,
	ArrowDownwardOutlined,
	ArrowUpward,
	ArrowUpwardOutlined,
	Comment,
	MoreHoriz,
} from '@mui/icons-material'
import {
	Avatar,
	Box,
	Button,
	Checkbox,
	Divider,
	FormControlLabel,
	IconButton,
	Typography,
} from '@mui/material'
import { green } from '@mui/material/colors'
import dayjs from 'dayjs'
import { useState } from 'react'
import { toast } from 'react-toastify'
import { AddComment } from '../AddComment'
export const AnswerList = ({ questionData }: { questionData: IQuestion }) => {
	return (
		<>
			{questionData.answers.map((answer) => (
				<AnswerCard key={answer.id} answerData={answer} />
			))}
		</>
	)
}

function AnswerCard({ answerData }: { answerData: IAnswer }) {
	const [isCommenting, setIsCommenting] = useState<boolean>(false)

	const handleSolved = async () => {
		const solveToast = toast.loading('Обработка ответа...')
		const response = await fetch('/api/forum/mark-answer-solving', {
			method: 'POST',
			body: JSON.stringify({
				question_answer_id: answerData.id,
			}),
		})

		const result = await response.json()

		if (!response.ok) {
			toast.update(solveToast, {
				render: result.error,
				type: 'error',
				isLoading: false,
				autoClose: 3000,
			})
			return null
		}

		answerData.is_solving = result.is_solving
		toast.update(solveToast, {
			render: result.message,
			type: 'success',
			isLoading: false,
			autoClose: 3000,
		})
	}

	return (
		<>
			<Box sx={{ px: 3, py: 2, width: '100%' }}>
				<Box
					sx={{
						display: 'flex',
						alignItems: 'flex-start',
						position: 'relative',
					}}>
					<Box
						sx={{
							display: 'flex',
							flexDirection: 'column',
							alignItems: 'center',
							height: '100%',
						}}>
						<Avatar
							sx={{
								width: 18,
								height: 18,
								fontSize: 12,
								bgcolor: green[500],
								marginRight: 1,
							}}
							aria-label='recipe'
							src={
								answerData?.user?.profile_image
									? answerData?.user?.profile_image
									: ''
							}>
							{!answerData?.user?.profile_image &&
								answerData?.user?.user_name[0]}
						</Avatar>
						<Divider orientation='vertical' flexItem />
					</Box>
					<Box sx={{ width: '100%' }}>
						<Box sx={{ display: 'flex', ml: 1 }}>
							<Typography sx={{ marginRight: 1 }} variant='caption'>
								{answerData?.user?.user_name || 'Гость'}
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
								justifyContent: 'space-between',
							}}>
							<Box sx={{ display: 'flex', alignItems: 'center' }}>
								<Checkbox
									icon={<ArrowUpwardOutlined />}
									checkedIcon={<ArrowUpward />}
									onClick={() => likeComment({ id: answerData.id })}
								/>
								{answerData.rating.like_amount -
									answerData.rating.dislike_amount}
								<Checkbox
									icon={<ArrowDownwardOutlined />}
									checkedIcon={<ArrowDownward />}
									onClick={() => dislikeComment({ id: answerData.id })}
								/>
								<FormControlLabel
									control={
										<IconButton
											onClick={() =>
												setIsCommenting((state) => (state = !state))
											}
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
							<Box sx={{ display: 'flex', alignItems: 'center' }}>
								<Button onClick={handleSolved} size='small' variant='outlined'>
									Отметить решающим
								</Button>
							</Box>
						</Box>
					</Box>
				</Box>
				{isCommenting && <AddComment answerData={answerData} />}
				{answerData.comments.map((comment) => (
					<CommentCard key={comment.id} comment={comment} />
				))}
			</Box>
		</>
	)
}

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

const CommentCard = ({ comment }: { comment: IComment }) => {
	return (
		<>
			<Box sx={{ display: 'flex' }}>
				<Box sx={{ px: 8, py: 1, width: '100%' }}>
					<Box
						sx={{
							display: 'flex',
							alignItems: 'flex-start',
							postion: 'relative',
						}}>
						<Box
							sx={{
								display: 'flex',
								flexDirection: 'column',
								height: '100%',
							}}>
							<Avatar
								sx={{
									width: 18,
									height: 18,
									fontSize: 12,
									bgcolor: green[500],
									marginRight: 1,
								}}
								aria-label='recipe'
								src={
									comment?.user?.profile_image
										? comment?.user?.profile_image
										: ''
								}>
								{comment?.user?.profile_image
									? ''
									: comment?.user?.user_name[0]}
							</Avatar>
						</Box>
						<Box sx={{ width: '100%' }}>
							<Box sx={{ display: 'flex' }}>
								<Typography sx={{ marginRight: 1 }} variant='caption'>
									{comment?.user?.user_name || 'Гость'}
								</Typography>
								<Typography sx={{ color: 'GrayText' }} variant='caption'>
									{dayjs(comment?.creation_date).format('DD-MM-YYYY')}
								</Typography>
							</Box>
							<Typography className='comment' sx={{}} variant='body1'>
								{comment.comment}
							</Typography>
							<Box
								sx={{
									display: 'flex',
									alignItems: 'center',
								}}>
								<FormControlLabel
									sx={{ fontSize: 10 }}
									control={
										<IconButton sx={{ ml: 0.5, mr: 0 }}>
											<Comment sx={{ width: 16 }} />
										</IconButton>
									}
									label='Ответить'
								/>
								<IconButton>
									<MoreHoriz sx={{ width: 12, height: 12 }} />
								</IconButton>
							</Box>
						</Box>
					</Box>
				</Box>
			</Box>
		</>
	)
}
