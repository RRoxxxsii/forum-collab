'use client'
import { IQuestion } from '@/types/types'
import { TextareaAutosize } from '@mui/base/TextareaAutosize'
import { Box, Button, Typography } from '@mui/material'
import React from 'react'

export const Reply = ({ answerData }: { answerData: IQuestion }) => {
	const [replyContent, setReplyContent] = React.useState('')
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
				Вы отвечаете пользователю {'@' + answerData?.user?.username || 'Гость'}
			</Typography>
			<TextareaAutosize />
			<Button variant='outlined' sx={{ mt: 1, maxWidth: 220 }}>
				Оставить комментарий
			</Button>
		</Box>
	)
}
