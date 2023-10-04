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
import { Comment as CommentComponent } from '../AddComment'
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
							display: 'inline-flex',
							flexDirection: 'column',
							alignItems: 'center',
							height: '100%',
						}}>
						<Avatar
							sx={{
								width: 32,
								height: 32,
								fontSize: 12,
								bgcolor: green[500],
								mb: 2,
								position: 'relative',
							}}
							aria-label='recipe'>
							Г
						</Avatar>
						<Divider
							sx={{ display: 'block', height: '100%' }}
							orientation='vertical'
						/>
					</Box>
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
					<Button size='small' variant='outlined'>
						Отметить решающим
					</Button>
				</Box>
				{isCommenting && <CommentComponent answerData={answerData} />}
				{answerData.comments.map((comment) => (
					<CommentCard comment={comment} />
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
									width: 24,
									height: 24,
									fontSize: 12,
									bgcolor: green[500],
									marginRight: 1,
								}}
								aria-label='recipe'>
								Г
							</Avatar>
						</Box>
						<Box sx={{ width: '100%' }}>
							<Box sx={{ display: 'flex' }}>
								<Typography sx={{ marginRight: 1 }} variant='caption'>
									{comment?.user?.username || 'Гость'}
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
