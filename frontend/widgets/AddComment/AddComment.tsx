'use client'
import { IAnswer, IUser } from '@/types/types'
import { TextareaAutosize } from '@mui/base/TextareaAutosize'
import { Box, Button, Typography } from '@mui/material'
import React from 'react'

export const AddComment = ({
	answerData,
	profileData,
}: {
	answerData: IAnswer
	profileData: IUser
}) => {
	const [commentContent, setCommentContent] = React.useState('')

	const handleComment = async () => {
		if (commentContent.length > 0 && commentContent.length < 320) {
			const response = await fetch('/api/forum/comment', {
				method: 'POST',
				body: JSON.stringify({
					user: profileData,
					comment: commentContent,
					question_answer: answerData.id,
				}),
			})

			if (!response.ok) {
				return
			}

			const data = await response.json()

			setCommentContent('')
			answerData.comments.push(data)
		}
	}
	return (
		<Box
			sx={{
				mb: 2,
				pl: 4,
				display: 'flex',
				flexDirection: 'column',
				maxWidth: 600,
			}}>
			<Typography variant='caption' color={'GrayText'}>
				Вы отвечаете пользователю {'@' + answerData?.user?.user_name ?? 'Гость'}
			</Typography>

			<TextareaAutosize
				minRows={2}
				onChange={(e) => setCommentContent(e.target.value)}
				className='textarea'
				maxLength={320}
			/>
			<Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
				<Button
					onClick={handleComment}
					variant='outlined'
					sx={{ mt: 1, maxWidth: 220 }}>
					Оставить комментарий
				</Button>
				<Typography
					sx={{ userSelect: 'none' }}
					color={'ButtonHighlight'}
					variant='caption'>
					{commentContent.length}/320
				</Typography>
			</Box>
		</Box>
	)
}
