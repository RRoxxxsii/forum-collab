'use client'
import { BASE_URL } from '@/shared/constants'
import { IAnswer, IQuestion } from '@/types/types'
import {
	ArrowUpwardOutlined,
	ArrowUpward,
	ArrowDownwardOutlined,
	ArrowDownward,
	MoreHoriz,
	Comment,
} from '@mui/icons-material'
import {
	Box,
	Avatar,
	Typography,
	Checkbox,
	FormControlLabel,
	IconButton,
	Button,
} from '@mui/material'
import { red } from '@mui/material/colors'
import dayjs from 'dayjs'
import React, { useEffect, useState } from 'react'
import { Comment as CommentComponent } from '../Comment'
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
